from ..types import NodeLocation, _PteroApp


class LocationManager:
    def __init__(self, client: _PteroApp) -> None:
        self.client = client
        self.cache: dict[int, NodeLocation] = {}
    
    def __repr__(self) -> str:
        return '<LocationManager cached=%d>' % len(self.cache)
    
    def __len__(self) -> int:
        return len(self.cache)
    
    def __getitem__(self, loc_id: int):
        return self.cache.get(loc_id)
    
    def __delitem__(self, loc_id: int):
        del self.cache[loc_id]
    
    def _patch(self, data: dict[str,]) -> NodeLocation | dict[int, NodeLocation]:
        if data.get('data'):
            res: dict[int, NodeLocation] = {}
            
            for obj in data['data']:
                res[obj['id']] = obj
            
            self.cache.update(res)
            return res
        else:
            self.cache[data['id']] = data
            return data
    
    async def fetch(self, loc_id: int = None, force: bool = False):
        if loc_id:
            if not force:
                if loc := self.cache.get(loc_id):
                    return loc
        
        data = await self.client.requests.rget(
            '/api/applicaton/locations%s'
            % (('/'+ str(loc_id)) if loc_id else '')
        )
        return self._patch(data)
