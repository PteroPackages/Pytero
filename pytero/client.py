from .files import Directory, File
from .http import RequestManager
from .permissions import Permissions
from .types import APIKey, Activity, ClientDatabase, ClientVariable, NetworkAllocation, \
    SSHKey, Statistics, Task, WebSocketAuth
from .schedules import Schedule
from .servers import ClientServer
from .shard import Shard
from .users import Account, SubUser


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
    
    async def enable_account_two_factor(self, code: int, /) -> list[str]:
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
    
    async def delete_api_key(self, identifier: str, /) -> None:
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
    
    async def remove_ssh_key(self, fingerprint: str, /) -> None:
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
    
    async def get_server(self, identifier: str, /) -> ClientServer:
        data = await self._http.get(f'/servers/{identifier}')
        return ClientServer(self._http, data['attributes'])
    
    async def get_server_ws(self, identifier: str, /) -> WebSocketAuth:
        data = await self._http.get(f'/servers/{identifier}/websocket')
        return WebSocketAuth(**data['data'])
    
    def create_shard(self, identifier: str, /) -> Shard:
        return Shard(self._http, identifier)
    
    async def get_server_resources(self, identifier: str, /) -> Statistics:
        data = await self._http.get(f'/servers/{identifier}/resources')
        return Statistics(**data['attributes'])
    
    async def get_server_activities(self, identifier: str, /) -> list[Activity]:
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
    
    async def get_server_databases(self, identifier: str, /) -> list[ClientDatabase]:
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
    
    async def get_server_files(self, identifier: str, dir: str = '/') -> list[File]:
        return await Directory(self._http, identifier, dir).get_files()
    
    async def get_server_file_dirs(
        self,
        identifier: str,
        root: str = '/'
    ) -> list[Directory]:
        return await Directory(self._http, identifier, root).get_directories()
    
    async def get_server_schedules(self, identifier: str, /) -> list[Schedule]:
        data = await self._http.get(f'/servers/{identifier}/schedules')
        res: list[Schedule] = []
        
        for datum in data['data']:
            res.append(Schedule(self._http, identifier, datum['attributes']))
        
        return res
    
    async def get_server_schedule(self, identifier: str, id: int) -> Schedule:
        data = await self._http.get(f'/servers/{identifier}/schedules/{id}')
        return Schedule(self._http, identifier, data['attributes'])
    
    async def create_server_schedule(
        self,
        identifier: str,
        *,
        name: str,
        is_active: bool,
        minute: str,
        hour: str,
        day_of_week: str,
        day_of_month: str
    ) -> Schedule:
        data = await self._http.post(
            f'/servers/{identifier}/schedules',
            body={
                'name': name,
                'is_active': is_active,
                'minute': minute,
                'hour': hour,
                'day_of_week': day_of_week,
                'day_of_month': day_of_month}
        )
        return Schedule(self._http, identifier, data['attributes'])
    
    async def update_server_schedule(
        self,
        identifier: str,
        id: int,
        *,
        name: str = None,
        is_active: bool = False,
        minute: str = None,
        hour: str = None,
        month: str = None,
        day_of_week: str = None,
        day_of_month: str = None,
        only_when_online: bool = False
    ) -> Schedule:
        old = await self.get_server_schedule(identifier, id)
        name = name or old.name
        is_active = is_active if is_active is not None else old.is_active
        minute = minute or old.cron.minute
        hour = hour or old.cron.hour
        month = month or old.cron.month
        day_of_week = day_of_week or old.cron.day_of_week
        day_of_month = day_of_month or old.cron.day_of_month
        only_when_online = only_when_online if only_when_online is not None else old.only_when_online
        
        data = await self._http.post(
            '/servers/%s/schedules/%d' % (identifier, id),
            body={
                'name': name,
                'is_active': is_active,
                'minute': minute,
                'hour': hour,
                'month': month,
                'day_of_week': day_of_week,
                'day_of_month': day_of_month,
                'only_when_online': only_when_online}
        )
        return Schedule(self._http, identifier, data['attributes'])
    
    async def execute_server_schedule(self, identifier: str, id: int) -> None:
        await self._http.post('/servers/%s/schedules/%d/execute' % (identifier, id))
    
    async def delete_server_schedule(self, identifier: str, id: int) -> None:
        await self._http.delete('/servers/%s/schedules/%d' % (identifier, id))
    
    async def get_schedule_tasks(self, identifier: str, id: int) -> list[Task]:
        data = await self._http.get('/servers/%s/schedules/%d/tasks' % (identifier, id))
        res: list[Task] = []
        
        for datum in data['data']:
            res.append(Task(**datum['attributes']))
        
        return res
    
    async def create_schedule_task(
        self,
        identifier: str,
        id: int,
        *,
        action: str,
        payload: str,
        time_offset: int,
        sequence_id: int = None,
        continue_on_failure: bool = False
    ) -> Task:
        data = await self._http.post(
            '/servers/%s/schedules/%d/tasks' % (identifier, id),
            body={
                'action': action,
                'payload': payload,
                'time_offset': time_offset,
                'sequence_id': sequence_id,
                'continue_on_failure': continue_on_failure}
        )
        return Task(**data['attributes'])
    
    async def update_schedule_task(
        self,
        identifier: str,
        id: int,
        tid: int,
        *,
        action: str,
        payload: str,
        time_offset: int,
        continue_on_failure: bool = False
    ) -> Task:
        data = await self._http.post(
            '/servers/%s/schedules/%d/tasks/%d' % (identifier, id, tid),
            body={
                'action': action,
                'payload': payload,
                'time_offset': time_offset,
                'continue_on_failure': continue_on_failure}
        )
        return Task(**data['attributes'])
    
    async def delete_schedule_task(
        self,
        identifier: str,
        id: int,
        tid: int
    ) -> None:
        await self._http.delete(
            '/servers/%s/schedules/%d/tasks/%d' % (identifier, id, tid)
        )
    
    async def get_server_allocations(
        self,
        identifier: str,
        /
    ) -> list[NetworkAllocation]:
        data = await self._http.get(f'/servers/{identifier}/network/allocations')
        res: list[NetworkAllocation] = []
        
        for datum in data['data']:
            res.append(NetworkAllocation(**datum['attributes']))
        
        return res
    
    async def create_server_allocation(self, identifier: str, /) -> NetworkAllocation:
        data = await self._http.post(
            f'/servers/{identifier}/network/allocations',
            body=None
        )
        return NetworkAllocation(**data['attributes'])
    
    async def set_server_allocation_notes(
        self,
        identifier: str,
        id: int,
        notes: str
    ) -> NetworkAllocation:
        data = await self._http.post(
            '/servers/%s/network/allocations/%d' % (identifier, id),
            body={'notes': notes}
        )
        return NetworkAllocation(**data['attributes'])
    
    async def set_server_primary_allocation(
        self,
        identifier: str,
        id: int
    ) -> NetworkAllocation:
        data = await self._http.post(
            '/servers/%s/network/allocations/%d/primary' % (identifier, id)
        )
        return NetworkAllocation(**data['attributes'])
    
    async def delete_server_allocation(self, identifier: str, id: int) -> None:
        await self._http.delete(
            '/servers/%s/network/allocations/%d' % (identifier, id)
        )
    
    async def get_server_subusers(self, identifier: str, /) -> list[SubUser]:
        data = await self._http.get(f'/servers/{identifier}/users')
        res: list[SubUser] = []
        
        for datum in data['data']:
            res.append(SubUser(self._http, datum['attributes']))
        
        return res
    
    async def get_server_subuser(self, identifier: str, uuid: str) -> SubUser:
        data = await self._http.get('/servers/%s/users/%s' % (identifier, uuid))
        return SubUser(self._http, data['attributes'])
    
    async def add_server_subuser(self, identifier: str, email: str) -> SubUser:
        data = await self._http.post(
            f'/servers/{identifier}/users',
            body={'email': email}
        )
        return SubUser(self._http, data['attributes'])
    
    async def update_subuser_permissions(
        self,
        identifier: str,
        uuid: str,
        permissions: Permissions
    ) -> SubUser:
        data = await self._http.post(
            '/servers/%s/users/%s' % (identifier, uuid),
            body={'permissions': permissions.value}
        )
        return SubUser(self._http, data['attributes'])
    
    async def remove_server_subuser(self, identifier: str, uuid: str) -> None:
        await self._http.delete(
            '/servers/%s/users/%s' % (identifier, uuid)
        )
    
    async def get_server_startup(self, identifier: str) -> list[ClientVariable]:
        data = await self._http.get(f'/servers/{identifier}/startup')
        res: list[ClientVariable] = []
        
        for datum in data['data']:
            res.append(ClientVariable(**datum['attributes']))
        
        return res
    
    async def set_server_variable(
        self,
        identifier: str,
        key: str,
        value: int | str | bool
    ) -> ClientVariable:
        data = await self._http.put(
            f'/servers/{identifier}/startup/variable',
            body={'key': key, 'value': value}
        )
        return ClientVariable(**data['attributes'])
    
    async def rename_server(self, identifier: str, name: str) -> None:
        await self._http.post(
            f'/servers/{identifier}/settings/rename',
            body={'name': name}
        )
    
    async def reinstall_server(self, identifier: str, /) -> None:
        await self._http.post(f'/servers/{identifier}/settings/reinstall')
    
    async def set_server_docker_image(self, identifier: str, image: str) -> None:
        await self._http.put(
            f'/servers/{identifier}/settings/docker-image',
            body={'docker_image': image}
        )
