from ..types import Nest, _PteroApp


class NestManager:
    def __init__(self, client: _PteroApp) -> None:
        self.client = client
        self.cache: dict[int, Nest] = {}
    
    def __repr__(self) -> str:
        return '<NestManager cached=%d>' % len(self.cache)
    
    def __len__(self) -> int:
        return len(self.cache)
    
    def __getitem__(self, nest_id: int):
        return self.cache.get(nest_id)
    
    def __delitem__(self, nest_id: int):
        del self.cache[nest_id]
    
    def _patch(self, data: dict[str,]) -> Nest | dict[int, Nest]:
        if data.get('data'):
            res: dict[int, Nest] = {}
            
            for obj in data['data']:
                res[obj['id']] = obj
            
            self.cache.update(res)
            return res
        else:
            self.cache[data['id']] = data
            return data
    
    async def fetch(self, nest_id: int = None, force: bool = False):
        if nest_id:
            if not force:
                if nest := self.cache.get(nest_id):
                    return nest
        
        data = await self.client.requests.rget(
            '/nests%s'
            % (('/'+ str(nest_id)) if nest_id else ''))
        
        return self._patch(data)
