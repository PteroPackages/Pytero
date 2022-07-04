from typing import Optional
from ..servers import AppServer
from ..types import _PteroApp
from ..util import select


class AppServerManager:
    def __init__(self, client: _PteroApp) -> None:
        self.client = client
        self.cache: dict[int, AppServer] = {}
    
    def __repr__(self) -> str:
        return '<AppServerManager cached=%d>' % len(self.cache)
    
    def __len__(self) -> int:
        return len(self.cache)
    
    def __getitem__(self, server: int):
        return self.cache.get(server)
    
    def __delitem__(self, server: int):
        del self.cache[server]
    
    def _patch(self, data: dict[str,]):
        if data.get('data') is not None:
            if not len(data['data']):
                return {}
            
            res: dict[int, AppServer] = {}
            
            for obj in data['data']:
                res[obj['attributes']['id']] = AppServer(
                    self.client, obj['attributes']
                )
            
            self.cache.update(res)
            return res
        else:
            server = AppServer(self.client, data['attributes'])
            self.cache[server.id] = server
            return server
    
    async def fetch(
        self,
        server_id: int = None,
        *,
        force: bool = False,
        include: list[str] = [],
        page: int = 0,
        per_page: int = None
    ):
        if server_id and not force:
            if server := self.cache.get(server_id):
                return server
        
        data = await self.client.requests.rget(
            '/servers%s' % ('/%d' % server_id if server_id else ''),
            include=include, page=page, per_page=per_page
        )
        return self._patch(data)
    
    async def create(
        self,
        user_id: int,
        *,
        name: str,
        egg: int,
        image: str,
        startup: str,
        allocation: dict[str,],
        description: Optional[str] = None,
        environment: dict[str,] = {},
        deploy: dict[str,] = {},
        limits: dict[str, int] = {},
        feature_limits: dict[str, int] = {},
        skip_scripts: bool = True,
        oom_disabled: bool = True,
        start_on_completion: bool = True
    ):
        deploy = select(deploy, ['locations', 'dedicated_ip', 'port_range'])
        if v := deploy.get('locations'):
            if not isinstance(v, list):
                raise TypeError("'deploy.locations' must be a number list")
            
            if not all(filter(lambda i: type(i) is int, v)):
                raise TypeError("'deploy.locations' must be a number list")
        
        if deploy.get('dedicated_ip') is None:
            deploy['dedicated_ip'] = False
        
        if v := deploy.get('port_range'):
            if not isinstance(v, list):
                raise TypeError("'deploy.port_range' must be a string list")
            
            if not all(filter(lambda i: type(i) is str, v)):
                raise TypeError("'deploy.port_range' must be a string list")
        
        limits = select(
            limits,
            ['memory', 'swap', 'disk', 'io', 'threads', 'cpu']
        )
        feature_limits = select(
            feature_limits,
            ['allocations', 'backups', 'databases']
        )
        
        data = await self.client.requests.rpost(
            '/servers',
            user=user_id,
            name=name,
            description=description,
            egg=egg,
            image=image,
            startup=startup,
            allocation=allocation,
            environment=environment,
            deploy=deploy,
            limits=limits,
            feature_limits=feature_limits,
            skip_scripts=skip_scripts,
            oom_disabled=oom_disabled,
            start_on_completion=start_on_completion
        )
        return self._patch(data)
    
    async def update_details(
        self,
        server_id: int,
        *,
        name: str = None,
        owner: int = None,
        external_id: int = None,
        description: str = None
    ):
        if not any([
                name,
                owner,
                external_id,
                description]):
            raise KeyError('no arguments provided to update the server')
        
        server = await self.fetch(server_id)
        name = name or server.name
        owner = owner or server.owner_id
        external_id = external_id or server.external_id
        description = description or server.description
        
        data = await self.client.requests.rpatch(
            '/servers/%d/details' % server_id,
            name=name,
            user=owner,
            external_id=external_id,
            description=description
        )
        return self._patch(data)
    
    async def update_build(
        self,
        server_id: int,
        *,
        allocation: int = None,
        swap: int = None,
        memory: int = None,
        disk: int = None,
        cpu: int = None,
        threads: Optional[str] = None,
        io: int = None,
        feature_limits: dict[str, int] = {}
    ):
        return NotImplemented
    
    async def update_startup(
        self,
        server_id: int,
        *,
        startup: str = None,
        environment: dict[str,] = {},
        egg: int = None,
        image: str = None,
        skip_scripts: bool = False
    ):
        return NotImplemented
    
    async def suspend(self, server_id: int):
        await self.client.requests.rpost('/servers/%d/suspend' % server_id)
        if server := self.cache.get(server_id):
            server.suspended = True
            server.usable = False
    
    async def unsuspend(self, server_id: int):
        await self.client.requests.rpost('/servers/%d/unsuspend' % server_id)
        if server := self.cache.get(server_id):
            server.suspended = False
            server.usable = True
    
    async def reinstall(self, server_id: int):
        await self.client.requests.rpost('/servers/%d/reinstall' % server_id)
    
    async def delete(self, server_id: int, force: bool = False):
        await self.client.requests.rdelete(
            '/servers/%d%s'
            % (server_id, '/force' if force else '')
        )
        del self.cache[server_id]
