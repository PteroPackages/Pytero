from typing import Optional
from .types import _Http


class File:
    def __init__(
        self,
        http: _Http,
        identifier: str,
        root: str,
        data: dict[str,]
    ) -> None:
        self._http = http
        self.identifier = identifier
        self.__name: str = data['name']
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
        return '<File name=%s path=%s>' % (self.__name, self.__path)
    
    def __str__(self) -> str:
        return self.__name
    
    @property
    def name(self) -> str:
        return self.__name
    
    @property
    def path(self) -> str:
        return self.__path


class Directory:
    def __init__(self, http: _Http, identifier: str, path: str) -> None:
        self._http = http
        self.identifier = identifier
        self.__path = path
    
    def __repr__(self) -> str:
        return '<Directory path=%s>' % self.__path
    
    def __str__(self) -> str:
        return self.__path
    
    @property
    def path(self) -> str:
        return self.__path
    
    async def get_files(self) -> list[File]:
        data = await self._http.get(
            '/servers/%s/files/list?directory=%s' % (self.identifier, self.__path)
        )
        res: list[File] = []
        
        for datum in data['data']:
            if datum['attributes']['mimetype'] == 'inode/directory':
                continue
            else:
                res.append(File(
                    self.__path,
                    self.identifier,
                    self.__path,
                    datum['attributes']
                ))
        
        return res
    
    async def get_directories(self):
        data = await self._http.get(
            '/servers/%s/files/list?directory=%s' % (self.identifier, self.__path)
        )
        res: list[Directory] = []
        
        for datum in data['data']:
            if datum['attributes']['mimetype'] == 'inode/directory':
                path = self._clean(self.__path + datum['attributes']['name'])
                res.append(Directory(self._http, self.identifier, path))
        
        return res
    
    def _clean(self, path: str) -> str:
        if 'home/directory' in path:
            path = path.replace('home/directory', '')
        
        return '/' + path.replace('\\', '/').removeprefix('/').removesuffix('/')
    
    def into_dir(self, dir: str):
        path = self._clean(self.__path + dir)
        return Directory(self._http, self.identifier, path)
    
    def back_dir(self, dir: str):
        path = self._clean(self.__path + dir)
        if '..' in path:
            path = path.split('..')[0]
        
        return Directory(self._http, self.identifier, path)
