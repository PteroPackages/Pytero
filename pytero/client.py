from .http import RequestManager
from .types import APIKey, Activity, ClientDatabase, SSHKey, Statistics, WebSocketAuth
from .servers import ClientServer
from .shard import Shard
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
    
    async def get_api_keys(self) -> list[APIKey]:
        data = await self._http.get('/account/api-keys')
        res: list[APIKey] = []
        
        for datum in data['data']:
            res.append(APIKey(**datum['attributes']))
        
        return res
    
    async def create_api_key(
        self,
        *,
        description: str,
        allowed_ips: list[str] = []
    ) -> APIKey:
        data = await self._http.post(
            '/account/api-keys',
            body={'description': description, 'allowed_ips': allowed_ips}
        )
        return APIKey(**data['attributes'])
    
    async def delete_api_key(self, identifier: str) -> None:
        await self._http.delete(f'/account/api-keys/{identifier}')
    
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
    
    async def get_servers(self) -> list[ClientServer]:
        data = await self._http.get('/')
        res: list[ClientServer] = []
        
        for datum in data['data']:
            res.append(ClientServer(self._http, datum['attributes']))
        
        return res
    
    async def get_server(self, identifier: str) -> ClientServer:
        data = await self._http.get(f'/servers/{identifier}')
        return ClientServer(self._http, data['attributes'])
    
    async def get_server_ws(self, identifier: str) -> WebSocketAuth:
        data = await self._http.get(f'/servers/{identifier}/websocket')
        return WebSocketAuth(**data['data'])
    
    def create_shard(self, identifier: str) -> Shard:
        return Shard(self._http, identifier)
    
    async def get_server_resources(self, identifier: str) -> Statistics:
        data = await self._http.get(f'/servers/{identifier}/resources')
        return Statistics(**data['attributes'])
    
    async def get_server_activities(self, identifier: str) -> list[Activity]:
        data = await self._http.get(f'/servers/{identifier}/activity')
        res: list[Activity] = []
        
        for datum in data['data']:
            res.append(Activity(**datum['attributes']))
        
        return res
    
    async def send_server_command(self, identifier: str, command: str) -> None:
        await self._http.post(
            f'/servers/{identifier}/command',
            body={'command': command}
        )
    
    async def send_server_power(self, identifier: str, state: str) -> None:
        await self._http.post(
            f'/servers/{identifier}/power',
            body={'signal': state}
        )
    
    async def get_server_databases(self, identifier: str) -> list[ClientDatabase]:
        data = await self._http.get(f'/servers/{identifier}/databases')
        res: list[ClientDatabase] = []
        
        for datum in data['data']:
            res.append(ClientDatabase(**datum['attributes']))
        
        return res
    
    async def create_server_database(
        self,
        identifier: str,
        *,
        database: str,
        remote: str
    ) -> ClientDatabase:
        data = await self._http.post(
            f'/servers/{identifier}/databases',
            body={
                'database': database,
                'remote': remote}
        )
        return ClientDatabase(**data['attributes'])
    
    async def rotate_database_password(self, identifier: str, id: str) -> ClientDatabase:
        data = await self._http.post(
            f'/servers/{identifier}/databases/{id}/rotate-password'
        )
        return ClientDatabase(**data['attributes'])
    
    async def delete_server_database(self, identifier: str, id: str) -> None:
        await self._http.delete(f'/servers/{identifier}/databases/{id}')
