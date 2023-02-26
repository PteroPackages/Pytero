from typing import Any, Optional
from .types import _Http


__all__ = ('File', 'Directory')


class File:
    def __init__(
        self,
        http: _Http,
        identifier: str,
        root: str,
        data: dict[str, Any]
    ) -> None:
        self._http = http
        self.identifier = identifier
        self.__name: str = data['name']
        if root != '/':
            root += '/'

        self.__path: str = root + data['name']
        self.mode: str = data['mode']
        self.mode_bits: int = int(data['mode_bits'])
        self.size: int = int(data['size'])
        self.is_file: bool = data['is_file']
        self.is_symlink: bool = data['is_symlink']
        self.mimetype: str = data['mimetype']
        self.created_at: str = data['created_at']
        self.modified_at: Optional[str] = data.get('modified_at')

    def __repr__(self) -> str:
        return f'<File name={self.name} path={self.__path}>'

    def __str__(self) -> str:
        return self.__name

    @property
    def name(self) -> str:
        return self.__name

    @property
    def path(self) -> str:
        return self.__path

    @property
    def root(self) -> str:
        root = '/'.join(self.path.split('/')[:-1])
        if root == '':
            return '/'

        return root

    async def get_contents(self) -> str:
        return await self._http.get(
            f'/servers/{self.identifier}/files/contents?file={self.__path}',
            ctype='text/plain')

    async def get_download_url(self) -> str:
        data = await self._http.get(
            f'/servers/{self.identifier}/files/download?file={self.__path}')

        return data['attributes']['url']

    async def download_to(self, dest: str, /) -> None:
        file = open(dest, 'xb')
        url = await self.get_download_url()

        # TODO: resolve this
        dl = await self._http._raw('GET', url, ctype='text/plain')
        file.write(bytes(dl, 'utf-8'))
        file.close()

    async def rename(self, name: str, /) -> None:
        await self._http.put(
            f'/servers/{self.identifier}/files/rename',
            {
                'root': self.root,
                'files': [{
                    'from': self.__name,
                    'to': name
                }]
            })

        self.__name = name

    async def copy_to(self, location: str, /) -> None:
        await self._http.post(f'/servers/{self.identifier}/files/copy',
                              {'location': location})

    async def write(self, data: str, /) -> None:
        await self._http.post(
            f'/servers/{self.identifier}/files/write?file={self.__path}',
            ctype='text/plain',
            body=bytes(data, 'utf-8'))

    async def compress(self):
        data = await self._http.post(
            f'/servers/{self.identifier}/files/compress',
            {'root': self.root, 'files': [self.__name]})

        return File(self._http, self.identifier, self.__path,
                    data['attributes'])

    async def decompress(self) -> None:
        await self._http.post(f'/servers/{self.identifier}/files/decompress',
                              {'root': self.root, 'file': self.__name})

    async def delete(self) -> None:
        await self._http.post(f'/servers/{self.identifier}/files/delete',
                              {'root': self.root, 'files': [self.__name]})


class Directory:
    def __init__(self, http: _Http, identifier: str, path: str) -> None:
        self._http = http
        self.identifier = identifier
        self.__path = path

    def __repr__(self) -> str:
        return f'<Directory path={self.__path}>'

    def __str__(self) -> str:
        return self.__path

    @property
    def path(self) -> str:
        return self.__path

    async def get_files(self) -> list[File]:
        data = await self._http.get(
            f'/servers/{self.identifier}/files/list?directory={self.__path}')

        res: list[File] = []

        for datum in data['data']:
            if datum['attributes']['mimetype'] == 'inode/directory':
                continue

            res.append(File(
                self._http,
                self.identifier,
                self.__path,
                datum['attributes']))

        return res

    async def get_directories(self):
        data = await self._http.get(
            f'/servers/{self.identifier}/files/list?directory={self.__path}')

        res: list[Directory] = []

        for datum in data['data']:
            if datum['attributes']['mimetype'] == 'inode/directory':
                path = self._clean(self.__path + datum['attributes']['name'])
                res.append(Directory(self._http, self.identifier, path))

        return res

    def _clean(self, path: str, /) -> str:
        if 'home/directory' in path:
            path = path.replace('home/directory', '')

        return '/' + path.replace('\\', '/').removeprefix('/').removesuffix('/')  # noqa: E501

    def into_dir(self, _dir: str, /):
        path = self._clean(self.__path + _dir)
        return Directory(self._http, self.identifier, path)

    def back_dir(self, _dir: str, /):
        path = self._clean(self.__path + _dir)
        if '..' in path:
            path = path.split('..')[0]

        return Directory(self._http, self.identifier, path)

    async def rename_all(self, files: list[dict[str, str]]) -> None:
        parsed = list(filter(lambda d: 'from' in d and 'to' in d, files))
        if len(parsed) == 0:
            raise SyntaxError('no files with from and to keys found')

        await self._http.post(f'/servers/{self.identifier}/files/rename',
                              {'root': self.__path, 'files': files})

    async def create_dir(self, name: str, /):
        await self._http.post(
            f'/servers/{self.identifier}/files/create-folder',
            {'root': self.__path, 'name': name})

        return Directory(self._http, self.identifier,
                         self._clean(self.__path + name))

    async def delete_dir(self, name: str, /) -> None:
        await self._http.post(f'/servers/{self.identifier}/files/delete',
                              {'root': self.__path, 'files': [name]})

    async def delete_all(self, files: list[dict[str, str]], /) -> None:
        parsed = list(filter(lambda d: 'from' in d and 'to' in d, files))
        if len(parsed) == 0:
            raise SyntaxError('no files with from and to keys found')

        await self._http.post(f'/servers/{self.identifier}/files/delete',
                              {'root': self.__path, 'files': files})

    async def delete(self) -> None:
        await self.delete_dir(self.__path)

    async def pull_file(
        self,
        url: str,
        *,
        directory: str = None,
        filename: str = None,
        use_header: bool = False,
        foreground: bool = False
    ) -> None:
        if directory is None:
            directory = self.__path

        await self._http.post(
            f'/servers/{self.identifier}/files/pull',
            {
                'url': url,
                'directory': directory,
                'filename': filename,
                'use_header': use_header,
                'foreground': foreground
            })

    async def get_upload_url(self) -> str:
        data = await self._http.get(f'/servers/{self.identifier}/files/upload')
        return data['attributes']['url']
