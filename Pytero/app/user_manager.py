from ..structures.users import PteroUser
from ..types import _PteroApp


class UserManager:
    def __init__(self, client: _PteroApp) -> None:
        self.client = client
        self.cache: dict[int, PteroUser] = {}
    
    def __repr__(self) -> str:
        return '<UserManager cached=%d>' % len(self.cache)
    
    def __len__(self) -> int:
        return len(self.cache)
    
    def __getitem__(self, user_id: int):
        return self.cache.get(user_id)
    
    def __delitem__(self, user_id: int):
        del self.cache[user_id]
    
    def _patch(self, data: dict[str,]) -> PteroUser | dict[int, PteroUser]:
        if data.get('data'):
            res: dict[int, PteroUser] = {}
            
            for obj in data['data']:
                user = PteroUser(self.client, obj['attributes'])
                res[user.id] = user
            
            self.cache.update(res)
            return res
        else:
            user = PteroUser(self.client, data['attributes'])
            self.cache[user.id] = user
            return user
    
    async def fetch(
        self,
        user_id: int = None,
        *,
        force: bool = False,
        with_servers: bool = False,
        external: bool = False
    ):
        if user_id:
            if not force:
                if user := self.cache.get(user_id):
                    return user
        
        data = await self.client.requests.rget(
            '/api/application/users%s%s%s'
            % (
                ('/external' if external and user_id else ''),
                ('/'+ str(user_id) if user_id else ''),
                ('?include=servers' if with_servers else '')))
        
        return self._patch(data)
    
    async def create(
        self,
        email: str,
        username: str,
        firstname: str,
        lastname: str,
        password: str = None
    ) -> PteroUser:
        data = await self.client.requests.rpost(
            '/api/application/users',
            {
                'email': email,
                'username': username,
                'first_name': firstname,
                'last_name': lastname,
                'password': password
            }
        )
        return self._patch(data)
    
    async def delete(self, user_id: int) -> bool:
        await self.client.requests.rdelete(
            '/api/application/users/%d' % user_id)
        del self.cache[user_id]
        return True
