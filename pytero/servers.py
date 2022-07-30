from .types import _Http, Allocation, Container, Egg, FeatureLimits, Limits, \
    Location, Nest
from .util import transform


__all__ = ('AppServer', 'ClientServer')


class AppServer:
    def __init__(self, http, data: dict[str,]) -> None:
        self._http = http
        self.id: int = data['id']
        self.external_id: str | None = data.get('external_id')
        self.uuid: str = data['uuid']
        self.identifier: str = data['identifier']
        self.created_at: str = data['created_at']
        self._patch(data)
        self._patch_relations(data.get('relationships'))
    
    def __repr__(self) -> str:
        return '<AppServer id=%d identifier=%s>' % (self.id, self.identifier)
    
    def __str__(self) -> str:
        return self.name
    
    def _patch(self, data: dict[str,]) -> None:
        self.name: str = data['name']
        self.description: str | None = data.get('description')
        self.status: str | None = data.get('status')
        self.suspended: bool = data.get('suspended', False)
        self.limits: Limits = Limits(**data['limits'])
        self.feature_limits: FeatureLimits = FeatureLimits(**data['feature_limits'])
        self.user_id: int = data['user']
        self.node_id: int = data['node']
        self.allocation_id: int = data['allocation']
        self.allocations: list[Allocation] | None = None
        self.nest_id: int = data['nest']
        self.nest: Nest | None = None
        self.egg_id: int = data['egg']
        self.egg: Egg | None = None
        self.container: Container = Container(**data['container'])
        self.location: Location | None = None
        self.updated_at: str | None = data.get('updated_at')
    
    def _patch_relations(self, data: dict[str,] | None) -> None:
        if data is None:
            return
        
        if 'allocations' in data:
            self.allocations = []
            for datum in data['allocations']['data']:
                self.allocations.append(Allocation(**datum['attributes']))
        
        if 'nest' in data:
            self.nest = Nest(**data['nest']['attributes'])
        
        if 'egg' in data:
            self.egg = Egg(**data['egg']['attributes'])
        
        if 'location' in data:
            self.location = Location(**data['location']['attributes'])
    
    def to_dict(self) -> dict[str,]:
        return transform(
            self,
            ignore=['_http'],
            maps={
                'user_id': 'user',
                'node_id': 'node',
                'allocation_id': 'allocation',
                'egg_id': 'egg',
                'nest_id': 'nest'})
    
    async def update_details(
        self,
        *,
        external_id: str = None,
        name: str = None,
        user: int = None,
        description: str = None
    ) -> None:
        external_id = external_id or self.external_id
        name = name or self.name
        user = user or self.user_id
        description = description or self.description
        
        data: AppServer = await self._http.update_server_details(
            self.id,
            external_id=external_id,
            name=name,
            user=user,
            description=description)
        
        self._patch(data.to_dict())
    
    async def update_build(
        self,
        *,
        allocation: int = None,
        oom_disabled: bool = True,
        limits: Limits = None,
        feature_limits: FeatureLimits = None,
        add_allocations: list[int] = None,
        remove_allocations: list[int] = None
    ) -> None:
        body = {
                'allocation': allocation or self.allocation_id,
                'limits': limits or self.limits,
                'feature_limits': feature_limits or self.feature_limits}
        
        if oom_disabled is not None:
            body['oom_disabled'] = oom_disabled
        
        if add_allocations is not None:
            body['add_allocations'] = add_allocations
        
        if remove_allocations is not None:
            body['remove_allocations'] = remove_allocations
        
        data: AppServer = await self._http.update_server_build(self.id, **body)
        self._patch(data.to_dict())
    
    async def update_startup(
        self,
        *,
        startup: str = None,
        environment: dict[str, int | str | bool] = None,
        egg: int = None,
        image: str = None,
        skip_scripts: bool = False
    ) -> None:
        data: AppServer = await self._http.update_server_startup(
            self.id,
            startup=startup or self.container.startup_command,
            environment=environment or self.container.environment,
            egg=egg or self.egg_id,
            image=image or self.container.image,
            skip_scripts=skip_scripts)
        
        self._patch(data.to_dict())
    
    async def suspend(self) -> None:
        await self._http.suspend_server(self.id)
        self.suspended = True
    
    async def unsuspend(self) -> None:
        await self._http.unsuspend_server(self.id)
        self.suspended = False
    
    async def reinstall(self) -> None:
        await self._http.reinstall_server(self.id)


class ClientServer:
    def __init__(self, http: _Http, data: dict[str,]) -> None:
        self._http = http
        self.uuid: str = data['uuid']
        self.identifier: str = data['identifier']
        self.internal_id: int = data['internal_id']
        self._patch(data)
    
    def __repr__(self) -> str:
        return '<ClientServer identifier=%s>' % self.identifier
    
    def __str__(self) -> str:
        return self.name
    
    def _patch(self, data: dict[str,]) -> None:
        self.server_owner: bool = data['server_owner']
        self.name: str = data['name']
        self.node: str = data['node']
        self.description: str | None = data.get('description')
        self.sftp_details: dict[str,] = data['sftp_details']
        self.limits: Limits = Limits(**data['limits'])
        self.feature_limits: FeatureLimits = FeatureLimits(**data['feature_limits'])
        self.invocation: str = data['invocation']
        self.docker_image: str = data['docker_image']
        self.egg_features: list[str] | None = data.get('egg_features')
        self.status: str | None = data.get('status')
        self.is_suspended: bool = data['is_suspended']
        self.is_installing: bool = data['is_installing']
        self.is_transferring: bool = data['is_transferring']
    
    def _patch_relations(self) -> None:
        pass
    
    def to_dict(self) -> dict[str,]:
        return transform(self, ignore=['_http'])
