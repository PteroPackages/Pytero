from ..structures.node import Node
from ..types import _PteroApp


class NodeManager:
    DEFAULT_INCLUDE: tuple[str] = ('allocations', 'locations', 'servers')
    
    def __init__(self, client: _PteroApp) -> None:
        self.client = client
        self.cache: dict[int, Node] = {}
    
    def __repr__(self) -> str:
        return '<NodeManager cached=%d>' % len(self.cache)
    
    def __len__(self) -> int:
        return len(self.cache)
    
    def __getitem__(self, node_id: int):
        return self.cache.get(node_id)
    
    def __delitem__(self, node_id: int):
        del self.cache[node_id]
    
    def _patch(self, data: dict[str,]) -> Node | dict[int, Node]:
        if data.get('data'):
            res: dict[int, Node] = {}
            
            for obj in data['data']:
                node = Node(self.client, obj['attributes'])
                res[node.id] = node
            
            self.cache.update(res)
            return res
        else:
            node = Node(self.client, data['attributes'])
            self.cache[node.id] = node
            return node
    
    def _parse_include(self, options: list[str]) -> str:
        if not len(options):
            return ''
        
        for op in options:
            if op not in self.DEFAULT_INCLUDE:
                raise KeyError("invalid include option '%s'" % op)
        
        return '?include=%s' % ','.join(options)
    
    async def fetch(
        self,
        node_id: int = None,
        *,
        force: bool = False,
        include: list[str] = []
    ):
        if node_id and not force:
            if node := self.cache.get(node_id):
                return node
        
        data = await self.client.requests.rget(
            '/nodes%s%s'
            % (
                ('/' + str(node_id)) if node_id else '',
                self._parse_include(include)))
        
        return self._patch(data)
    
    async def update(
        self,
        node_id: int,
        *,
        name: str = None,
        location: int = None,
        fqdn: str = None,
        scheme: str = None,
        memory: int = None,
        memory_overallocate: int = None,
        disk: int = None,
        disk_overallocate: int = None,
        sftp: dict[str, int] = {},
        upload_size: int = None
    ):
        if not any([
                name,
                location,
                fqdn,
                scheme,
                memory,
                memory_overallocate,
                disk,
                disk_overallocate,
                sftp,
                upload_size]):
            raise KeyError('no arguments provided to update the node')
        
        node = await self.fetch(node_id)
        name = name or node.name
        location = location or node.location_id
        fqdn = fqdn or node.fqdn
        scheme = scheme or node.scheme
        memory = memory or node.memory
        memory_overallocate = memory_overallocate or node.memory_overallocate
        disk = disk or node.disk
        disk_overallocate = disk_overallocate or node.disk_overallocate
        sftp['port'] = sftp.get('port', node.daemon_sftp)
        sftp['listen'] = sftp.get('listen', node.daemon_listen)
        upload_size = upload_size or node.upload_size
        
        data = await self.client.requests.rpatch(
            '/nodes/%d' % node_id,
            name=name,
            location=location,
            fqdn=fqdn,
            scheme=scheme,
            memory=memory,
            memory_overallocate=memory_overallocate,
            disk=disk,
            disk_overallocate=disk_overallocate,
            sftp=sftp,
            upload_size=upload_size)
        
        return self._patch(data)
    
    async def delete(self, node_id: int) -> bool:
        await self.client.requests.rdelete(
            '/nodes/%d' % node_id
        )
        del self.cache[node_id]
        return True
