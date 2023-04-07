"""The main class/interface for interacting with the Pterodactyl client
API.

This only supports client API keys, NOT application API keys, found at:
https://your.pterodactyl.domain/account/api.
"""

# pylint: disable=R0904

from typing import Any
from .files import Directory, File
from .http import RequestManager
from .permissions import Permissions
from .types import APIKey, Activity, Backup, ClientDatabase, ClientVariable, \
    NetworkAllocation, SSHKey, Statistics, Task, WebSocketAuth
from .schedules import Schedule
from .servers import ClientServer
from .shard import Shard
from .users import Account, SubUser


__all__ = ('PteroClient',)


class PteroClient:
    """A class/interface for interacting with the client API.

    Parameters
    ~~~~~~~~~~
    url: :class:`str`
        The URL of the Pterodactyl domain. This must be an absolute URL, not
        one that contains paths (trailing forward slash is allowed).
    key: :class:`str`
        The API key to use for HTTP requests. This must be a client API key,
        NOT an application API key.
    """

    def __init__(self, url: str, key: str) -> None:
        self.url = url.removesuffix('/')
        self.key = key
        self._http = RequestManager('client', self.url, key)

    def __repr__(self) -> str:
        return '<PteroClient>'

    @property
    def event(self):
        """A decorator shorthand function for :meth:`RequestManager#event`."""
        return self._http.event

    async def get_permission_keys(self) -> dict[str, Any]:
        """Returns a dict containing the permission keys, values and
        descriptions for the client API."""
        data = await self._http.get('/permissions')
        return data['attributes']

    async def get_account(self) -> Account:
        """Returns an account object for the user associated with the API key
        being used."""
        data = await self._http.get('/account')
        return Account(self, data['attributes'])

    async def get_account_two_factor(self) -> dict[str, str]:
        """Returns a dict containing the two-factor authentication details."""
        data = await self._http.get('/account/two-factor')
        return data['data']

    async def enable_account_two_factor(self, code: int, /) -> list[str]:
        """Enables two-factor authentication for the user associated with the
        API key.

        Parameters
        ~~~~~~~~~~
        code: :class:`int`
            The TOTP code generated with the authentication details.
        """
        data = await self._http.post('/account/two-factor', {'code': code})
        return data['attributes']['tokens']

    def disable_account_two_factor(self, password: str, /) -> None:
        """Disables two-factor authentication for the user associated with the
        API key.

        Parameters
        ~~~~~~~~~~
        password: :class:`str`
            The password for the account associated with the API key.
        """
        return self._http.delete('/account/two-factor',
                                 body={'password': password})

    def update_account_email(self, email: str, password: str) -> None:
        """Updates the email for the user account associated with the API key.

        Parameters
        ~~~~~~~~~~
        email: :class:`str`
            The new email for the account.
        password: :class:`str`
            The password for the account.
        """
        return self._http.put('/account/email', {'email': email,
                                                 'password': password})

    def update_account_password(self, old: str, new: str) -> None:
        """Updates the password for the user account associated with the API
        key.

        Parameters
        ~~~~~~~~~~
        old: :class:`str`
            The old password of the account.
        new: :class:`str`
            The new password for the account.
        """
        return self._http.put('/account/password',
                              {
                                  'current_password': old,
                                  'new_password': new,
                                  'password_confirmation': new
                              })

    async def get_account_activities(self) -> list[Activity]:
        data = await self._http.get('/account/activity')
        return [Activity(**datum['attributes']) for datum in data['data']]

    async def get_api_keys(self) -> list[APIKey]:
        data = await self._http.get('/account/api-keys')
        return [APIKey(**datum['attributes']) for datum in data['data']]

    async def create_api_key(
        self,
        *,
        description: str,
        allowed_ips: list[str] = None
    ) -> APIKey:
        data = await self._http.post(
            '/account/api-keys',
            {'description': description, 'allowed_ips': allowed_ips or []})

        return APIKey(**data['attributes'])

    def delete_api_key(self, identifier: str, /) -> None:
        return self._http.delete(f'/account/api-keys/{identifier}')

    async def get_ssh_keys(self) -> list[SSHKey]:
        data = await self._http.get('/account/ssh-keys')
        return [SSHKey(**datum['attributes']) for datum in data['data']]

    async def create_ssh_key(self, *, name: str, public_key: str) -> SSHKey:
        data = await self._http.post('/account/ssh-keys',
                                     {'name': name, 'public_key': public_key})

        return SSHKey(**data['attributes'])

    def remove_ssh_key(self, fingerprint: str, /) -> None:
        return self._http.post('/account/ssh-keys/remove',
                               {'fingerprint': fingerprint})

    async def get_servers(self) -> list[ClientServer]:
        data = await self._http.get('/')
        return [ClientServer(self._http, datum['attributes'])
                for datum in data['data']]

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

    async def get_server_activities(self,
                                    identifier: str, /) -> list[Activity]:
        data = await self._http.get(f'/servers/{identifier}/activity')
        return [Activity(**datum['attributes']) for datum in data['data']]

    def send_server_command(self, identifier: str, command: str) -> None:
        return self._http.post(f'/servers/{identifier}/command',
                               {'command': command})

    def send_server_power(self, identifier: str, state: str) -> None:
        return self._http.post(f'/servers/{identifier}/power',
                               {'signal': state})

    async def get_server_databases(self,
                                   identifier: str, /) -> list[ClientDatabase]:
        data = await self._http.get(f'/servers/{identifier}/databases')
        return [ClientDatabase(**datum['attributes'])
                for datum in data['data']]

    async def create_server_database(
        self,
        identifier: str,
        *,
        database: str,
        remote: str
    ) -> ClientDatabase:
        data = await self._http.post(f'/servers/{identifier}/databases',
                                     {'database': database, 'remote': remote})

        return ClientDatabase(**data['attributes'])

    async def rotate_database_password(self, identifier: str,
                                       _id: str) -> ClientDatabase:
        data = await self._http.post(
            f'/servers/{identifier}/databases/{_id}/rotate-password', None)

        return ClientDatabase(**data['attributes'])

    def delete_server_database(self, identifier: str, _id: str) -> None:
        return self._http.delete(f'/servers/{identifier}/databases/{_id}')

    def get_directory(self, identifier: str, _dir: str) -> Directory:
        return Directory(self._http, identifier, _dir)

    def get_server_files(self, identifier: str, _dir: str = '/') -> list[File]:
        return Directory(self._http, identifier, _dir).get_files()

    def get_server_file_dirs(
        self,
        identifier: str,
        root: str = '/'
    ) -> list[Directory]:
        return Directory(self._http, identifier, root).get_directories()

    async def get_server_schedules(self, identifier: str, /) -> list[Schedule]:
        data = await self._http.get(f'/servers/{identifier}/schedules')
        return [Schedule(self._http, identifier, datum['attributes'])
                for datum in data['data']]

    async def get_server_schedule(self, identifier: str, _id: int) -> Schedule:
        data = await self._http.get(f'/servers/{identifier}/schedules/{_id}')
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
            {
                'name': name,
                'is_active': is_active,
                'minute': minute,
                'hour': hour,
                'day_of_week': day_of_week,
                'day_of_month': day_of_month
            })

        return Schedule(self._http, identifier, data['attributes'])

    async def update_server_schedule(
        self,
        identifier: str,
        _id: int,
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
        old = await self.get_server_schedule(identifier, _id)
        name = name or old.name
        is_active = is_active if is_active is not None else old.is_active
        minute = minute or old.cron.minute
        hour = hour or old.cron.hour
        month = month or old.cron.month
        day_of_week = day_of_week or old.cron.day_of_week
        day_of_month = day_of_month or old.cron.day_of_month
        only_when_online = only_when_online \
            if only_when_online is not None \
            else old.only_when_online

        data = await self._http.post(
            f'/servers/{identifier}/schedules/{_id}',
            {
                'name': name,
                'is_active': is_active,
                'minute': minute,
                'hour': hour,
                'month': month,
                'day_of_week': day_of_week,
                'day_of_month': day_of_month,
                'only_when_online': only_when_online
            })

        return Schedule(self._http, identifier, data['attributes'])

    def execute_server_schedule(self, identifier: str, _id: int) -> None:
        return self._http.post(
            f'/servers/{identifier}/schedules/{_id}/execute', None)

    def delete_server_schedule(self, identifier: str, _id: int) -> None:
        return self._http.delete(f'/servers/{identifier}/schedules/{_id}')

    async def get_schedule_tasks(self, identifier: str,
                                 _id: int) -> list[Task]:
        data = await self._http.get(
            f'/servers/{identifier}/schedules/{_id}/tasks')

        return [Task(**datum['attributes']) for datum in data['data']]

    async def create_schedule_task(
        self,
        identifier: str,
        _id: int,
        *,
        action: str,
        payload: str,
        time_offset: int,
        sequence_id: int = None,
        continue_on_failure: bool = False
    ) -> Task:
        data = await self._http.post(
            f'/servers/{identifier}/schedules/{_id}/tasks',
            {
                'action': action,
                'payload': payload,
                'time_offset': time_offset,
                'sequence_id': sequence_id,
                'continue_on_failure': continue_on_failure
            })

        return Task(**data['attributes'])

    async def update_schedule_task(
        self,
        identifier: str,
        _id: int,
        tid: int,
        *,
        action: str,
        payload: str,
        time_offset: int,
        continue_on_failure: bool = False
    ) -> Task:
        data = await self._http.post(
            f'/servers/{identifier}/schedules/{_id}/tasks/{tid}',
            {
                'action': action,
                'payload': payload,
                'time_offset': time_offset,
                'continue_on_failure': continue_on_failure
            })

        return Task(**data['attributes'])

    def delete_schedule_task(
        self,
        identifier: str,
        _id: int,
        tid: int
    ) -> None:
        return self._http.delete(
            f'/servers/{identifier}/schedules/{_id}/tasks/{tid}')

    async def get_server_allocations(
        self,
        identifier: str,
        /
    ) -> list[NetworkAllocation]:
        data = await self._http.get(
            f'/servers/{identifier}/network/allocations')
        return [NetworkAllocation(**datum['attributes'])
                for datum in data['data']]

    async def create_server_allocation(self, identifier: str, /) \
            -> NetworkAllocation:
        data = await self._http.post(
            f'/servers/{identifier}/network/allocations', None)

        return NetworkAllocation(**data['attributes'])

    async def set_server_allocation_notes(
        self,
        identifier: str,
        _id: int,
        notes: str
    ) -> NetworkAllocation:
        data = await self._http.post(
            f'/servers/{identifier}/network/allocations/{_id}',
            {'notes': notes})

        return NetworkAllocation(**data['attributes'])

    async def set_server_primary_allocation(
        self,
        identifier: str,
        _id: int
    ) -> NetworkAllocation:
        data = await self._http.post(
            f'/servers/{identifier}/network/allocations/{_id}/primary', None)

        return NetworkAllocation(**data['attributes'])

    def delete_server_allocation(self, identifier: str, _id: int) -> None:
        return self._http.delete(
            f'/servers/{identifier}/network/allocations/{_id}')

    async def get_server_subusers(self, identifier: str, /) -> list[SubUser]:
        data = await self._http.get(f'/servers/{identifier}/users')
        return [SubUser(self._http, datum['attributes'])
                for datum in data['data']]

    async def get_server_subuser(self, identifier: str, uuid: str) -> SubUser:
        data = await self._http.get(f'/servers/{identifier}/users/{uuid}')
        return SubUser(self._http, data['attributes'])

    async def add_server_subuser(self, identifier: str, email: str) -> SubUser:
        data = await self._http.post(f'/servers/{identifier}/users',
                                     {'email': email})

        return SubUser(self._http, data['attributes'])

    async def update_subuser_permissions(
        self,
        identifier: str,
        uuid: str,
        permissions: Permissions
    ) -> SubUser:
        data = await self._http.post(f'/servers/{identifier}/users/{uuid}',
                                     {'permissions': permissions.value})

        return SubUser(self._http, data['attributes'])

    def remove_server_subuser(self, identifier: str, uuid: str) -> None:
        return self._http.delete(f'/servers/{identifier}/users/{uuid}')

    async def list_backups(self, identifier: str, /) -> list[Backup]:
        data = await self._http.get(f'/servers/{identifier}/backups')
        return [Backup(**datum['attributes']) for datum in data['data']]

    async def create_backup(self, identifier: str, *, name: str | None = None,
                            ignore_files: list[str] | None = None,
                            locked: bool = False) -> Backup:
        data = await self._http.post(f'/servers/{identifier}/backups',
                                     {"name": name,
                                      "ignore_files": ignore_files,
                                      "locked": locked})

        return Backup(**data['attributes'])

    async def get_backup(self, identifier: str, uuid: str) -> Backup:
        data = await self._http.get(f'/servers/{identifier}/backups/{uuid}')
        return Backup(**data['attributes'])

    async def get_backup_download_url(self, identifier: str, uuid: str) -> str:
        data = await self._http.get(
            f'/servers/{identifier}/backups/{uuid}/download')

        return data['attributes']['url']

    def delete_backup(self, identifier: str, uuid: str) -> None:
        return self._http.delete(f'/servers/{identifier}/backups/{uuid}')

    async def get_server_startup(self,
                                 identifier: str) -> list[ClientVariable]:
        data = await self._http.get(f'/servers/{identifier}/startup')
        return [ClientVariable(**datum['attributes'])
                for datum in data['data']]

    async def set_server_variable(self, identifier: str, key: str,
                                  value: int | str | bool) -> ClientVariable:
        data = await self._http.put(f'/servers/{identifier}/startup/variable',
                                    {'key': key, 'value': value})

        return ClientVariable(**data['attributes'])

    def rename_server(self, identifier: str, name: str) -> None:
        return self._http.post(f'/servers/{identifier}/settings/rename',
                               {'name': name})

    def reinstall_server(self, identifier: str, /) -> None:
        return self._http.post(
            f'/servers/{identifier}/settings/reinstall', None)

    def set_server_docker_image(self, identifier: str, image: str) -> None:
        return self._http.put(f'/servers/{identifier}/settings/docker-image',
                              {'docker_image': image})
