from .http import RequestManager
from .types import Activity, SSHKey
from .users import Account


__all__ = ('PteroClient')

class PteroClient:
    def __init__(self, url: str, key: str) -> None:
        self.url = url.removesuffix('/')
        self.key = key
        self._http = RequestManager('client', self.url, key)
    
    def __repr__(self) -> str:
        return '<PteroClient>'
    
    @property
    def event(self):
        return self._http.event
    
    async def get_permission_keys(self) -> dict[str,]:
        data = await self._http.get('/permissions')
        return data['attributes']
    
    async def get_account(self) -> Account:
        data = await self._http.get('/account')
        return Account(self._http, data['attributes'])
    
    async def get_account_two_factor(self) -> dict[str, str]:
        data = await self._http.get('/account/two-factor')
        return data['data']
    
    async def enable_account_two_factor(self, code: int) -> list[str]:
        data = await self._http.post('/account/two-factor', body={'code': code})
        return data['attributes']['tokens']
    
    async def disable_account_two_factor(self, password: str) -> None:
        await self._http.delete('/account/two-factor', body={'password': password})
    
    async def update_account_email(self, email: str, password: str) -> None:
        await self._http.put('/account/email', {'email': email, 'password': password})
    
    async def update_account_password(self, old: str, new: str) -> None:
        await self._http.put(
            self,
            body={
                'current_password': old,
                'new_password': new,
                'password_confirmation': new}
        )
    
    async def get_account_activities(self) -> list[Activity]:
        data = await self._http.get('/account/activity')
        res: list[Activity] = []
        
        for datum in data['data']:
            res.append(Activity(**datum['attributes']))
        
        return res
    
    async def get_ssh_keys(self) -> list[SSHKey]:
        data = await self._http.get('/account/ssh-keys')
        res: list[Activity] = []
        
        for datum in data['data']:
            res.append(SSHKey(**datum['attributes']))
        
        return res
    
    async def create_ssh_key(self, *, name: str, public_key: str) -> SSHKey:
        data = await self._http.post(
            '/account/ssh-keys',
            body={'name': name, 'public_key': public_key}
        )
        return SSHKey(**data['attributes'])
    
    async def remove_ssh_key(self, fingerprint: str) -> None:
        await self._http.post(
            '/account/ssh-keys/remove',
            body={'fingerprint': fingerprint}
        )
