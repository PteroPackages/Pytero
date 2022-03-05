from ..types import _PteroApp


class EggsManager:
    def __init__(self, client: _PteroApp) -> None:
        self.client = client
        self.cache: dict[int, dict[str,]] = {}
    
    def __repr__(self) -> str:
        return '<EggsManager cached=%d>' % len(self.cache)
    
    def __len__(self) -> int:
        return len(self.cache)
    
    def __getitem__(self, nest_id: int):
        return self.cache.get(nest_id)
    
    def __delitem__(self, nest_id: int):
        del self.cache[nest_id]
    
    def _patch(self, data: dict[str,]) -> dict[str,] | dict[int, dict[str,]]:
        if data.get('data'):
            res: dict[int, dict[str,]] = {}
            
            for obj in data['data']:
                res[obj['id']] = obj
            
            self.cache.update(res)
            return res
        else:
            self.cache[data['id']] = data
            return data
    
    async def fetch(
            self,
            nest_id: int,
            egg_id: int = None,
            force: bool = False):
        if egg_id:
            if not force:
                if egg := self.cache.get(egg_id):
                    return egg
        
        data = await self.client.requests.rget(
            '/nests/%d/eggs%s'
            % (nest_id, ('/'+ str(egg_id)) if egg_id else ''))
        
        return self._patch(data)
    
    def find_eggs_in_nest(self, nest_id: int) -> list[dict[str,]]:
        return list(filter(lambda e: e['nest'] == nest_id, self.cache))
