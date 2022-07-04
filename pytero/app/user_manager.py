from ..users import PteroUser
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
        if data.get('data') is not None:
            if not len(data['data']):
                return {}
            
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
        external: bool = False,
        page: int = 0,
        per_page: int = None
    ):
        if user_id and not force:
            if user := self.cache.get(user_id):
                return user
        
        data = await self.client.requests.rget(
            '/users%s%s'
            % (
                ('/external' if external and user_id else ''),
                ('/'+ str(user_id) if user_id else '')),
            include=['servers' if with_servers else None],
            page=page, per_page=per_page)
        
        return self._patch(data)
    
    async def query(
        self,
        entity: str,
        *,
        _filter: str = None,
        sort: str = None,
        per_page: int = None
    ) -> dict[int, PteroUser]:
        if _filter is None and sort is None:
            raise SyntaxError('filter or sort is required for query')
        
        if _filter is not None:
            if _filter not in ('email', 'uuid', 'username', 'external_id'):
                raise KeyError("invalid filter option '%s'" % _filter)
        
        if sort is not None:
            if sort not in ('id', '-id', 'uuid', '-uuid'):
                raise KeyError("invalid sort option '%s'" % sort)
        
        data = await self.client.requests.rget(
            '/users',
            filter=(_filter, entity) if _filter else None,
            sort=sort, per_page=per_page
        )
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
            email=email,
            username=username,
            first_name=firstname,
            last_name=lastname,
            password=password)
        
        return self._patch(data)
    
    async def update(
        self,
        user_id: int,
        *,
        email: str = None,
        username: str = None,
        firstname: str = None,
        lastname: str = None,
        language: str = None,
        password: str = None
    ) -> PteroUser:
        if not any([
                email,
                username,
                firstname,
                lastname,
                language
            ]):
            raise KeyError('no arguments provided to update the user')
        
        user = await self.fetch(user_id)
        email = email or user.email
        username = username or user.username
        firstname = firstname or user.firstname
        lastname = lastname or user.lastname
        language = language or user.language
        
        data = await self.client.requests.rpatch(
            '/users/%d' % user_id,
            email=email,
            username=username,
            first_name=firstname,
            last_name=lastname,
            language=language,
            password=password)
        
        return self._patch(data)
    
    async def delete(self, user_id: int) -> bool:
        await self.client.requests.rdelete('/users/%d' % user_id)
        del self.cache[user_id]
        return True
