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
    
    async def get_users(self) -> list[User]:
        data = await self._http.get('/users')
        res: list[User] = []
        
        for attr in data['data']:
            res.append(User(self._http, attr['attributes']))
        
        return res
    
    async def get_user(self, id: int) -> User:
        data = await self._http.get(f'/users/{id}')
        return User(self._http, data['attributes'])
    
    async def get_external_user(self, id: str) -> User:
        data = await self._http.get(f'/users/external/{id}')
        return User(self._http, data['attributes'])
    
    async def create_user(
        self,
        *,
        email: str,
        username: str,
        first_name: str,
        last_name: str,
        password: str = None,
        external_id: str = None,
        root_admin: bool = False
    ) -> User:
        data = await self._http.post(
            '/users',
            body={
                'email': email,
                'username': username,
                'first_name': first_name,
                'last_name': last_name,
                'password': password,
                'external_id': external_id,
                'root_admin': root_admin}
        )
        return User(self._http, data['attributes'])
    
    async def update_user(
        self,
        id: int,
        *,
        email: str,
        username: str,
        first_name: str,
        last_name: str,
        password: str = None,
        external_id: str = None,
        root_admin: bool = False
    ) -> User:
        old = await self.get_user(id)
        data = await self._http.patch(
            f'/users/{id}',
            body={
                'email': email or old.email,
                'username': username or old.username,
                'first_name': first_name or old.first_name,
                'last_name': last_name or old.last_name,
                'password': password or old.last_name,
                'external_id': external_id or old.external_id,
                'root_admin': root_admin if root_admin is not None else old.root_admin}
        )
        return User(self._http, data['attributes'])
    
    async def delete_user(self, id: int) -> None:
        await self._http.delete(f'/users/{id}')
