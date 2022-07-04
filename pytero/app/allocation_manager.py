from ..errors import RangeError
from ..types import _PteroApp, Allocation


class AllocationManager:
    def __init__(self, client: _PteroApp) -> None:
        self.client = client
        self.cache: dict[int, Allocation] = {}
    
    def __repr__(self) -> str:
        return '<AllocationManager cached=%d>' % len(self.cache)
    
    def __len__(self) -> int:
        return len(self.cache)
    
    def __getitem__(self, alloc_id: int):
        return self.cache.get(alloc_id)
    
    def __delitem__(self, alloc_id: int):
        del self.cache[alloc_id]
    
    def _patch(self, data: dict[str,]) -> Allocation | dict[int, Allocation]:
        if data.get('data') is not None:
            if not len(data['data']):
                return {}
            
            res: dict[int, Allocation] = {}
            
            for obj in data['data']:
                res[obj['attributes']['id']] = Allocation(**obj['attributes'])
            
            self.cache.update(res)
            return res
        else:
            self.cache[data['id']] = Allocation(**data)
            return self.cache[data['id']]
    
    async def fetch(
        self,
        node_id: int,
        alloc_id: int = None,
        force: bool = False,
        include: list[str] = [],
        page: int = 0,
        per_page: int = None
    ):
        if alloc_id and not force:
            if alloc := self.cache.get(alloc_id):
                return alloc
        
        data = await self.client.requests.rget(
            '/nodes/%d/allocations%s'
            % (
                node_id, ('/%d' % alloc_id if alloc_id else '')
            ),
            include=include, page=page, per_page=per_page
        )
        
        return self._patch(data)
    
    async def get_available(self, node_id: int, single: bool = False):
        data = await self.fetch(node_id, include=['servers'])
        res = {k: data[k] for k in data if data[k].assigned}
        
        if single:
            return res[0] if len(res) else None
        else:
            return res
    
    async def create(self, node_id: int, ip: str, ports: list[str] = []):
        for port in ports:
            if not isinstance(port, str):
                raise TypeError('allocation ports must be strings')
            
            if '-' not in port:
                continue
            
            start, stop = port.split('-')
            start, stop = int(start), int(stop)
            
            if start > stop:
                raise RangeError('start cannot be greater than stop')
            
            if start <= 1024 or stop > 65535:
                raise RangeError('port range must be between 1024 and 65535')
            
            if stop - start > 1000:
                raise RangeError('maximum port range exceeded (1000)')
        
        await self.client.requests.rpost(
            '/nodes/%d/allocations' % node_id,
            body={'ip': ip, 'ports': ports}
        )
    
    async def delete(self, node_id: int, alloc_id: int):
        await self.client.requests.rdelete(
            '/nodes/%d/allocations/%d' % (node_id, alloc_id)
        )
        if c := self.cache.get(node_id):
            del c[alloc_id]
        
        return True
