from .http import RequestManager
from .node import Node
from .servers import AppServer
from .types import Allocation, AppDatabase, DeployNodeOptions, DeployServerOptions, \
    Egg, FeatureLimits, Limits, Location, Nest, NodeConfiguration
from .users import User


__all__ = ('PteroApp')


class PteroApp:
    '''A class/interface for interacting with the application API.

    Parameters
    ----------
    url: :class:`str`
        The URL of the Pterodactyl domain. This must be an absolute URL, not one that contains
        paths (trailing forward slash is allowed).
    key: :class:`str`
        The API key to use for HTTP requests. This can be either an application API key or a Client
        API key (as of Pterodactyl v1.8).
    '''
    def __init__(self, url: str, key: str) -> None:
        self.url = url.removesuffix('/')
        self.key = key
        self._http = RequestManager('application', self.url, key)
    
    def __repr__(self) -> str:
        return '<PteroApp>'
    
    @property
    def event(self):
        '''Returns the HTTP class event decorator for registering events to trigger on.'''
        return self._http.event
    
    async def get_users(
        self,
        *,
        filter: tuple[str, str] = None,
        include: list[str] = None,
        sort: str = None
    ) -> list[User]:
        '''Returns a list of users from the API with the given options if specified.
        
        Parameters
        ----------
        filter: Optional[tuple[:class:`str`, :class:`str`]]
            A tuple containing the filter type and argument to filter by (default is ``None``).
            This supports:
            * email
            * uuid
            * username
            * external_id
        include: Optional[list[:class:`str`]]
            A list of additional resources to include (default is ``None``). This supports:
            * servers
        sort: Optional[:class:`str`]
            The order to sort the results in (default is ``None``). This supports:
            * id
            * uuid
        '''
        data = await self._http.get('/users', filter=filter, include=include, sort=sort)
        return [User(self, datum['attributes']) for datum in data['data']]
    
    async def get_user(
        self,
        id: int,
        *,
        include: list[str] = None
    ) -> User:
        '''Returns a user from the API with the given ID.
        
        Parameters
        ----------
        id: :class:`int`
            The ID of the user.
        include: Optional[list[:class:`str`]]
            A list of additional resources to include (default is ``None``). This supports:
                * servers
        '''
        data = await self._http.get(f'/users/{id}', include=include)
        return User(self, data['attributes'])
    
    async def get_external_user(self, id: str, /) -> User:
        '''Returns a user from the API with the given external identifier.
        
        Parameters
        ----------
        id: :class:`str`
            The external identifier of the user.
        '''
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
        '''Creates a new user account with the given fields.
        
        Parameters
        ----------
        email: :class:`str`
            The email for the user.        
        username: :class:`str`
            The username for the user.
        fist_name: :class:`str`
            The first name of the user.
        last_name: :class:`str`
            The last name of the user.
        password: Optional[:class:`str`]
            The password for the user (default is ``None``).
        external_id: Optional[:class:`str`]
            An external identifier for the user (default is ``None``).
        root_admin: Optional[:class:`bool`]
            Whether the user should be considered an admin (default is ``False``).
        '''
        data = await self._http.post(
            '/users',
            {
                'email': email,
                'username': username,
                'first_name': first_name,
                'last_name': last_name,
                'password': password,
                'external_id': external_id,
                'root_admin': root_admin
            })
        
        return User(self, data['attributes'])
    
    async def update_user(
        self,
        id: int,
        *,
        email: str = None,
        username: str = None,
        first_name: str = None,
        last_name: str = None,
        password: str = None,
        external_id: str = None,
        root_admin: bool = False
    ) -> User:
        '''Updates a specified user with the given fields.
        
        Parameters
        ----------
        id: :class:`int`
            The ID of the user to update.
        email: Optional[:class:`str`]
            The email for the user (default is the current value).
        username: Optional[:class:`str`]
            The username for the user (default is the current value).
        fist_name: Optional[:class:`str`]
            The first name of the user (default is the current value).
        last_name: Optional[:class:`str`]
            The last name of the user (default is the current value).
        password: Optional[:class:`str`]
            The password for the user (default is ``None``).
        external_id: Optional[:class:`str`]
            An external identifier for the user (default is the current value).
        root_admin: Optional[:class:`bool`]
            Whether the user should be considered an admin (default is the current value).
        '''
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
        
        data = await self._http.patch(f'/users/{id}', body)
        return User(self, data['attributes'])
    
    async def delete_user(self, id: int, /) -> None:
        '''Deletes a user by its ID.
        
        Parameters
        ----------
        id: :class:`int`
            The ID of the user to delete.
        '''
        await self._http.delete(f'/users/{id}')
    
    async def get_servers(
        self,
        *,
        filter: tuple[str, str] = None,
        include: list[str] = None,
        sort: str = None
    ) -> list[AppServer]:
        data = await self._http.get('/servers',
                                    filter=filter, include=include, sort=sort)
        
        res: list[AppServer] = []
        
        for datum in data['data']:
            res.append(AppServer(self, datum['attributes']))
        
        return res
    
    async def get_server(
        self,
        id: int,
        *,
        filter: tuple[str, str] = None,
        include: list[str] = None,
        sort: str = None
    ) -> AppServer:
        data = await self._http.get(f'/servers/{id}',
                                    filter=filter, include=include, sort=sort)
        
        return AppServer(self, data['attributes'])
    
    async def get_external_server(self, id: str, /) -> AppServer:
        data = await self._http.get(f'/servers/external/{id}')
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
            body['deploy'] = deploy.to_dict()
        else:
            body['allocation'] = {
                                'default': default_allocation,
                                'additional': additional_allocations}
        
        data = await self._http.post('/servers', body)
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
            {
                'external_id': external_id or old.external_id,
                'name': name or old.name,
                'user': user or old.user,
                'description': description or old.description
            })
        
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
            {
                'allocation': allocation or old.allocation_id,
                'oom_disabled': oom_disabled,
                'limits': (limits or old.limits).to_dict(),
                'feature_limits': (feature_limits or old.feature_limits).to_dict(),
                'add_allocations': add_allocations,
                'remove_allocations': remove_allocations
            })
        
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
            {
                'startup': startup or old.container.startup_command,
                'environment': environment or old.container.environment,
                'egg': egg or old.egg_id,
                'image': image or old.container.image,
                'skip_scripts': skip_scripts
            })
        
        return AppServer(self, data['attributes'])
    
    async def suspend_server(self, id: int, /) -> None:
        await self._http.post(f'/servers/{id}/suspend', None)
    
    async def unsuspend_server(self, id: int, /) -> None:
        await self._http.post(f'/servers/{id}/unsuspend', None)
    
    async def reinstall_server(self, id: int, /) -> None:
        await self._http.post(f'/servers/{id}/reinstall', None)
    
    async def delete_server(self, id: int, *, force: bool = False) -> None:
        await self._http.delete('/servers/%d%s' % (id, '/force' if force else ''))
    
    async def get_server_databases(
        self,
        server: int,
        *,
        include: list[str] = None
    ) -> list[AppDatabase]:
        data = await self._http.get(f'/servers/{server}/databases', include=include)
        res: list[AppDatabase] = []
        
        for datum in data['data']:
            res.append(AppDatabase(**datum['attributes']))
        
        return res
    
    async def get_server_database(
        self,
        server: int,
        id: int,
        *,
        include: list[str] = None
    ) -> AppDatabase:
        data = await self._http.get(
            '/servers/%d/databases/%d' % (server, id),
            include=include)
        
        return AppDatabase(**data['attributes'])
    
    async def create_database(
        self,
        server: int,
        *,
        database: str,
        remote: str
    ) -> AppDatabase:
        data = await self._http.post(f'/servers/{server}/databases',
                                    {'database': database, 'remote': remote})
        
        return AppDatabase(**data['attributes'])
    
    async def reset_database_password(self, server: int, id: int) -> AppDatabase:
        data = await self._http.post(
            '/servers/%d/databases/%d/reset-password' % (server, id),
            None)
        
        return AppDatabase(**data['attributes'])
    
    async def delete_database(self, server: int, id: int) -> None:
        await self._http.delete(f'/servers/{server}/databases/{id}')
    
    async def get_nodes(
        self,
        *,
        filter: tuple[str, str] = None,
        include: list[str] = None,
        sort: str = None
    ) -> list[Node]:
        data = await self._http.get('/nodes', filter=filter, include=include, sort=sort)
        res: list[Node] = []
        
        for datum in data['data']:
            res.append(Node(self, datum['attributes']))
        
        return res
    
    async def get_node(
        self,
        id: int,
        *,
        filter: tuple[str, str] = None,
        include: list[str] = None,
        sort: str = None
    ) -> Node:
        data = await self._http.get(f'/nodes/{id}',
                                    filter=filter, include=include, sort=sort)
        
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
    
    async def get_node_allocations(self, node: int, /) -> list[Allocation]:
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
            {
                'ip': ip,
                'alias': alias,
                'ports': ports
            })
        
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
        data = await self._http.post('/locations', {'short': short, 'long': long})
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
            {
                'short': short or old.short,
                'long': long or old.long
            })
        
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
