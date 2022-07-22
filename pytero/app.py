from .http import RequestManager
from .node import Node
from .servers import AppServer
from .types import Allocation, AppDatabase, DeployNodeOptions, DeployServerOptions, \
    Egg, FeatureLimits, Limits, Nest, NodeConfiguration, Location
from .users import User


__all__ = ('PteroApp')

class PteroApp:
    def __init__(self, url: str, key: str) -> None:
        self.url = url.removesuffix('/')
        self.key = key
        self._http = RequestManager('application', self.url, key)
    
    def __repr__(self) -> str:
        return '<PteroApp>'
    
    @property
    def event(self):
        return self._http.event
    
    async def get_users(self) -> list[User]:
        data = await self._http.get('/users')
        res: list[User] = []
        
        for datum in data['data']:
            res.append(User(self, datum['attributes']))
        
        return res
    
    async def get_user(self, id: int) -> User:
        data = await self._http.get(f'/users/{id}')
        return User(self, data['attributes'])
    
    async def get_external_user(self, id: str) -> User:
        data = await self._http.get(f'/users/external/{id}')
        return User(self, data['attributes'])
    
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
        return User(self, data['attributes'])
    
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
        body = {
                'email': email or old.email,
                'username': username or old.username,
                'first_name': first_name or old.first_name,
                'last_name': last_name or old.last_name,
                'external_id': external_id or old.external_id,
                'root_admin': root_admin if root_admin is not None else old.root_admin}
        
        if password is not None:
            body['password'] = password
        
        data = await self._http.patch(f'/users/{id}', body=body)
        return User(self, data['attributes'])
    
    async def delete_user(self, id: int) -> None:
        await self._http.delete(f'/users/{id}')
    
    async def get_servers(self) -> list[AppServer]:
        data = await self._http.get('/servers')
        res: list[AppServer] = []
        
        for datum in data['data']:
            res.append(AppServer(self, datum['attributes']))
        
        return res
    
    async def get_server(self, id: int | str) -> AppServer:
        path = f'/servers/{id}' if isinstance(id, int) else f'/servers/external/{id}'
        data = await self._http.get(path)
        return AppServer(self, data['attributes'])
    
    async def create_server(
        self,
        *,
        name: str,
        user: int,
        egg: int,
        docker_image: str,
        startup: str,
        environment: dict[str, int | str | bool],
        limits: Limits,
        feature_limits: FeatureLimits,
        external_id: str = None,
        default_allocation: int = None,
        additional_allocations: list[int] = None,
        deploy: DeployServerOptions = None,
        skip_scripts: bool = False,
        oom_disabled: bool = True,
        start_on_completion: bool = False
    ) -> AppServer:
        body = {
            'name': name,
            'user': user,
            'egg': egg,
            'docker_image': docker_image,
            'startup': startup,
            'environment': environment,
            'limits': limits.to_dict(),
            'feature_limits': feature_limits.to_dict(),
            'external_id': external_id,
            'skip_scripts': skip_scripts,
            'oom_disabled': oom_disabled,
            'start_on_completion': start_on_completion}
        
        if deploy is not None:
            body['deploy'] = dict(deploy)
        else:
            body['allocation'] = {
                'default': default_allocation,
                'additional': additional_allocations}
        
        data = await self._http.post('/servers', body=body)
        return AppServer(self, data['attributes'])
    
    async def update_server_details(
        self,
        id: int,
        *,
        external_id: str = None,
        name: str = None,
        user: int = None,
        description: str = None
    ) -> AppServer:
        old = await self.get_server(id)
        data = await self._http.patch(
            f'/servers/{id}/details',
            body={
                'external_id': external_id or old.external_id,
                'name': name or old.name,
                'user': user or old.user,
                'description': description or old.description}
        )
        return AppServer(self, data['attributes'])
    
    async def update_server_build(
        self,
        id: int,
        *,
        allocation: int = None,
        oom_disabled: bool = True,
        limits: Limits = None,
        feature_limits: FeatureLimits = None,
        add_allocations: list[int] = [],
        remove_allocations: list[int] = []
    ) -> AppServer:
        old = await self.get_server(id)
        data = await self._http.patch(
            f'/servers/{id}/build',
            body={
                'allocation': allocation or old.allocation_id,
                'oom_disabled': oom_disabled,
                'limits': limits.to_dict() if limits is not None else old.limits.to_dict(),
                'feature_limits': feature_limits.to_dict() if feature_limits is not None else old.feature_limts.to_dict(),
                'add_allocations': add_allocations,
                'remove_allocations': remove_allocations}
        )
        return AppServer(self, data['attributes'])
    
    async def update_server_startup(
        self,
        id: int,
        *,
        startup: str = None,
        environment: dict[str, int | str | bool] = None,
        egg: int = None,
        image: str = None,
        skip_scripts: bool = False
    ) -> AppServer:
        old = await self.get_server(id)
        data = await self._http.patch(
            f'/servers/{id}/startup',
            body={
                'startup': startup or old.container.startup_command,
                'environment': environment or old.container.environment,
                'egg': egg or old.egg_id,
                'image': image or old.container.image,
                'skip_scripts': skip_scripts}
        )
        return AppServer(self, data['attributes'])
    
    async def suspend_server(self, id: int, /) -> None:
        await self._http.post(f'/servers/{id}/suspend')
    
    async def unsuspend_server(self, id: int, /) -> None:
        await self._http.post(f'/servers/{id}/unsuspend')
    
    async def reinstall_server(self, id: int, /) -> None:
        await self._http.post(f'/servers/{id}/reinstall')
    
    async def delete_server(self, id: int, *, force: bool = False) -> None:
        await self._http.delete('/servers/%d%s' % (id, '/force' if force else ''))
    
    async def get_server_databases(self, server: int) -> list[AppDatabase]:
        data = await self._http.get(f'/servers/{server}/databases')
        res: list[AppDatabase] = []
        
        for datum in data['data']:
            res.append(AppDatabase(**datum['attributes']))
        
        return res
    
    async def get_server_database(self, server: int, id: int) -> AppDatabase:
        data = await self._http.get(f'/servers/{server}/databases/{id}')
        return AppDatabase(**data['attributes'])
    
    async def create_database(self, server: int, *, database: str, remote: str) -> AppDatabase:
        data = await self._http.post(
            f'/servers/{server}/databases',
            body={'database': database, 'remote': remote}
        )
        return AppDatabase(**data['attributes'])
    
    async def reset_database_password(self, server: int, id: int) -> AppDatabase:
        data = await self._http.post(f'/servers/{server}/databases/{id}/reset-password')
        return AppDatabase(**data['attributes'])
    
    async def delete_database(self, server: int, id: int) -> None:
        await self._http.delete(f'/servers/{server}/databases/{id}')
    
    async def get_nodes(self) -> list[Node]:
        data = await self._http.get('/nodes')
        res: list[Node] = []
        
        for datum in data['data']:
            res.append(Node(self, datum['attributes']))
        
        return res
    
    async def get_node(self, id: int) -> Node:
        data = await self._http.get(f'/nodes/{id}')
        return Node(self, data['attributes'])
    
    async def get_deployable_nodes(self, options: DeployNodeOptions, /) -> list[Node]:
        data = await self._http.get('/nodes/deployable', body=options.to_dict())
        res: list[Node] = []
        
        for datum in data['data']:
            res.append(Node(self, datum['attributes']))
        
        return res
    
    async def get_node_configuration(self, id: int, /) -> NodeConfiguration:
        data = await self._http.get(f'/nodes/{id}/configuration')
        return NodeConfiguration(**data)
    
    def create_node(self) -> None:
        return NotImplemented
    
    def update_node(self) -> None:
        return NotImplemented
    
    async def delete_node(self, id: int, /) -> None:
        await self._http.delete(f'/nodes/{id}')
    
    async def get_node_allocations(self, node: int) -> list[Allocation]:
        data = await self._http.get(f'/nodes/{node}/allocations')
        res: list[Allocation] = []
        
        for datum in data['data']:
            res.append(Allocation(**datum['attributes']))
        
        return res
    
    async def create_node_allocation(
        self,
        node: int,
        *,
        ip: str,
        ports: list[str],
        alias: str = None
    ) -> Allocation:
        data = await self._http.post(
            f'/nodes/{node}/allocations',
            body={
                'ip': ip,
                'alias': alias,
                'ports': ports}
        )
        return Allocation(**data['attributes'])
    
    async def delete_node_allocation(self, node: int, id: int) -> None:
        await self._http.delete(f'/nodes/{node}/allocations/{id}')
    
    async def get_locations(self) -> list[Location]:
        data = await self._http.get('/locations')
        res: list[Location] = []
        
        for datum in data['data']:
            res.append(Location(**datum['attributes']))
        
        return res
    
    async def get_location(self, id: int) -> Location:
        data = await self._http.get(f'/locations/{id}')
        return Location(**data['attributes'])
    
    async def create_location(self, *, short: str, long: str) -> Location:
        data = await self._http.post('/locations', body={'short': short, 'long': long})
        return Location(**data['attributes'])
    
    async def update_location(
        self,
        id: int,
        *,
        short: str = None,
        long: str = None
    ) -> Location:
        old = await self.get_location(id)
        data = await self._http.patch(
            f'/locations/{id}',
            body={
                'short': short or old.short,
                'long': long or old.long}
        )
        return Location(**data['attributes'])
    
    async def delete_location(self, id: int, /) -> None:
        await self._http.delete(f'/locations/{id}')
    
    async def get_nests(self) -> list[Nest]:
        data = await self._http.get('/nests')
        res: list[Nest] = []
        
        for datum in data['data']:
            res.append(Nest(**datum['attributes']))
        
        return res
    
    async def get_nest(self, nest: int) -> Nest:
        data = await self._http.get(f'/nests/{nest}')
        return Nest(**data['attributes'])
    
    async def get_nest_eggs(self, nest: int) -> list[Egg]:
        data = await self._http.get(f'/nests/{nest}/eggs')
        res: list[Egg] = []
        
        for datum in data['data']:
            res.append(Egg(**datum['attributes']))
        
        return res
    
    async def get_nest_egg(self, nest: int, id: int) -> Egg:
        data = await self._http.get(f'/nests/{nest}/eggs/{id}')
        return Egg(**data['attributes'])
