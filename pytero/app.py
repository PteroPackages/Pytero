from .http import RequestManager
from .users import User


__all__ = ('PteroApp')

class PteroApp:
    def __init__(self, url: str, key: str) -> None:
        self.url = url.removesuffix('/')
        self.key = key
        self._http = RequestManager('application', self.url, key)
    
    def __repr__(self) -> str:
        return 'PteroApp'
    
    @property
    def event(self):
        return self._http.event
    
    async def get_users(self):
        data = await self._http.get('/users')
        res: list[User] = []
        
        for attr in data['data']:
            res.append(User(self._http, attr['attributes']))
        
        return res
