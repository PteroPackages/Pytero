"""The main class/interface for interacting with the Pterodactyl application
API.

This supports application and client API keys at:
https://your.pterodactyl.domain/admin/api or
https://your.pterodactyl.domain/account/api.
"""

# pylint: disable=R0904

from .http import RequestManager
from .node import Node
from .servers import AppServer
from .types import Allocation, AppDatabase, DeployNodeOptions, \
    DeployServerOptions, Egg, FeatureLimits, Limits, Location, Nest, \
    NodeConfiguration
from .users import User


__all__ = ('PteroApp',)


class PteroApp:
    """A class/interface for interacting with the application API.

    url: :class:`str`
        The URL of the Pterodactyl domain. This must be an absolute URL, not
        one that contains paths (trailing forward slash is allowed).
    key: :class:`str`
        The API key to use for HTTP requests. This can be either an
        application API key or a Client API key (as of Pterodactyl v1.8).
    """

    def __init__(self, url: str, key: str) -> None:
        self.url = url.removesuffix('/')
        self.key = key
        self._http = RequestManager('application', self.url, key)

    def __repr__(self) -> str:
        return '<PteroApp>'

    @property
    def event(self):
        """Returns the HTTP class event decorator for registering events to
        trigger on.
        """
        return self._http.event

    async def get_users(
        self,
        *,
        _filter: tuple[str, str] = None,
        include: list[str] = None,
        sort: str = None
    ) -> list[User]:
        """Returns a list of users from the API with the given options if
        specified.

        filter: Optional[tuple[:class:`str`, :class:`str`]]
            A tuple containing the filter type and argument to filter by
            (default is ``None``). This supports:
            * email
            * uuid
            * username
            * external_id
        include: Optional[list[:class:`str`]]
            A list of additional resources to include (default is ``None``).
            This supports:
            * servers
        sort: Optional[:class:`str`]
            The order to sort the results in (default is ``None``). This
            supports:
            * id
            * uuid
        """
        data = await self._http.get('/users', _filter=_filter, include=include,
                                    sort=sort)
        return [User(self, datum['attributes']) for datum in data['data']]

    async def get_user(
        self,
        _id: int,
        *,
        include: list[str] = None
    ) -> User:
        """Returns a user from the API with the given ID.

        id: :class:`int`
            The ID of the user.
        include: Optional[list[:class:`str`]]
            A list of additional resources to include (default is ``None``).
            This supports:
            * servers
        """
        data = await self._http.get(f'/users/{_id}', include=include)
        return User(self, data['attributes'])

    async def get_external_user(self, _id: str, /) -> User:
        """Returns a user from the API with the given external identifier.

        id: :class:`str`
            The external identifier of the user.
        """
        data = await self._http.get(f'/users/external/{_id}')
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
        """Creates a new user account with the given fields.

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
            Whether the user should be considered an admin (default is
            ``False``).
        """
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
        _id: int,
        *,
        email: str = None,
        username: str = None,
        first_name: str = None,
        last_name: str = None,
        password: str = None,
        external_id: str = None,
        root_admin: bool = False
    ) -> User:
        """Updates a specified user with the given fields.

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
            Whether the user should be considered an admin (default is the
            current value).
        """
        old = await self.get_user(_id)
        body = {
            'email': email or old.email,
            'username': username or old.username,
            'first_name': first_name or old.first_name,
            'last_name': last_name or old.last_name,
            'external_id': external_id or old.external_id,
            'root_admin': root_admin if root_admin is not None else old.root_admin}  # noqa: E501

        if password is not None:
            body['password'] = password

        data = await self._http.patch(f'/users/{_id}', body)
        return User(self, data['attributes'])

    def delete_user(self, _id: int, /) -> None:
        """Deletes a user by its ID.

        id: :class:`int`
            The ID of the user to delete.
        """
        return self._http.delete(f'/users/{_id}')

    async def get_servers(
        self,
        *,
        _filter: tuple[str, str] = None,
        include: list[str] = None,
        sort: str = None
    ) -> list[AppServer]:
        """Returns a list of servers from the API with the given options if
        specified.

        filter: Optional[tuple[:class:`str`, :class:`str`]]
            A tuple containing the filter type and argument to filter by
            (default is ``None``). This supports:
            * uuid
            * uuidShort
            * name
            * description
            * image
            * external_id
        include: Optional[list[:class:`str`]]
            A list of additional resources to include (default is ``None``).
            This supports:
            * allocations
            * nest
            * egg
            * location
        sort: Optional[:class:`str`]
            The order to sort the results in (default is ``None``). This
            supports:
            * id
            * uuid
        """
        data = await self._http.get('/servers',
                                    _filter=_filter, include=include,
                                    sort=sort)
        return [AppServer(self, datum['attributes']) for datum in data['data']]

    async def get_server(
        self,
        _id: int,
        *,
        include: list[str] = None
    ) -> AppServer:
        """Returns a server from the API with the given ID.

        include: Optional[list[:class:`str`]]
            A list of additional resources to include (default is ``None``).
            This supports:
            * allocations
            * nest
            * egg
            * location
        """
        data = await self._http.get(f'/servers/{_id}', include=include)
        return AppServer(self, data['attributes'])

    async def get_external_server(self, _id: str, /) -> AppServer:
        """Returns a server from the API with the given external identifier.

        id: :class:`str`
            The external identifier of the server.
        """
        data = await self._http.get(f'/servers/external/{_id}')
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
        """Creates a new server with the given fields.

        name: :class:`str`
            The name of the server.
        user: :class:`int`
            The ID of the user that will own the server.
        egg: :class:`int`
            The ID of the egg to use for the server.
        docker_image: :class:`str`
            The docker image to use for the server.
        startup: :class:`str`
            The startup command for the server.
        environment: :class:`dict`
            The environment variables to set for the server.
        limits: :class:`Limits`
            The server resource limits.
        feature_limits: :class:`FeatureLimits`
            The server feature limits.
        external_id: Optional[:class:`str`]
            The external identifier for the server (default is ``None``).
        default_allocation: Optional[:class:`int`]
            The ID of the default allocation for the server. This must be
            specified unless the `deploy` object options is set (default is
            ``None``).
        additional_allocations: Optional[list[:class:`int`]]
            A list of additional allocation IDs to be added to the server
            (default is ``None``).
        deploy: Optional[:class:`DeployServerOptions`]
            An object containing the deploy options for the server. This must
            be specified unless the `default_allocation` option is set (default
            is ``None``).
        skip_scripts: Optional[:class:`bool`]
            Whether the server should skip the egg install script during
            installation (default is ``false``).
        oom_disabled: Optional[:class:`bool`]
            Whether the OOM killer should be disabled (default is ``True``).
        start_on_completion: Optional[:class:`bool`]
            Whether the server should start once the installation is complete
            (default is ``False``).
        """
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
        _id: int,
        *,
        external_id: str = None,
        name: str = None,
        user: int = None,
        description: str = None
    ) -> AppServer:
        """Updates the details for a specified server.

        id: :class:`int`
            The ID of the server.
        external_id: Optional[:class:`str`]
            The external identifier of the server (defaults to the original if
            unset).
        name: Optional[:class:`str`]
            The name of the server (defaults to the original if unset).
        user: Optional[:class:`int`]
            The ID of the server owner (defaults to the original if unset).
        description: Optional[:class:`str`]
            The description of the server (defaults to the original if unset).
        """
        old = await self.get_server(_id)
        data = await self._http.patch(
            f'/servers/{_id}/details',
            {
                'external_id': external_id or old.external_id,
                'name': name or old.name,
                'user': user or old.user,
                'description': description or old.description
            })

        return AppServer(self, data['attributes'])

    async def update_server_build(
        self,
        _id: int,
        *,
        allocation: int = None,
        oom_disabled: bool = True,
        limits: Limits = None,
        feature_limits: FeatureLimits = None,
        add_allocations: list[int] = None,
        remove_allocations: list[int] = None
    ) -> AppServer:
        """Updates the build details of a specified server.

        id: :class:`int`
            The ID of the server.
        allocation: Optional[:class:`int`]
            The ID of the primary allocation for the server (defaults to the
            original if unset).
        oom_disabled: Optional[:class:`bool`]
            Whether OOM should be disabled for the server (defaults to the
            original if unset).
        limits: Optional[:class:`Limits`]
            The resource limits for the server (defaults to the original if
            unset).
        feature_limits: Optional[:class:`FeatureLimits`]
            The feature limits for the server (defaults to the original if
            unset).
        add_allocations: Optional[list[:class:`int`]]
            A list of allocation IDs to add to the server (defaults to
            ``None``).
        remove_allocations: Optional[list[:class:`int`]]
            A list of allocation IDs to remove from the server (defaults to
            ``None``).
        """
        old = await self.get_server(_id)
        data = await self._http.patch(
            f'/servers/{_id}/build',
            {
                'allocation': allocation or old.allocation_id,
                'oom_disabled': oom_disabled,
                'limits': (limits or old.limits).to_dict(),
                'feature_limits':
                    (feature_limits or old.feature_limits).to_dict(),
                'add_allocations': add_allocations or [],
                'remove_allocations': remove_allocations or []
            })

        return AppServer(self, data['attributes'])

    async def update_server_startup(
        self,
        _id: int,
        *,
        startup: str = None,
        environment: dict[str, int | str | bool] = None,
        egg: int = None,
        image: str = None,
        skip_scripts: bool = False
    ) -> AppServer:
        """Updates the startup configuration for a specified server.

        id: :class:`int`
            The ID of the server.
        startup: Optional[:class:`str`]
            The startup command for the server (defaults to the original if
            unset).
        environment: Optional[:class:`dict`]
            The environment variables to set for the server (defaults to
            ``None``). This will update all variables at the same time and
            remove any variables that aren't specified from the server.
        egg: Optional[:class:`int`]
            The ID of the egg to use (defaults to the original if unset).
        image: Optional[:class:`str`]
            The docker image to use for the serverd (defaults to the original
            if unset).
        skip_scripts: Optional[:class:`bool`]
            Whether the server should skip the egg install script during
            installation (defaults to the original if unset).
        """
        old = await self.get_server(_id)
        data = await self._http.patch(
            f'/servers/{_id}/startup',
            {
                'startup': startup or old.container.startup_command,
                'environment': environment or old.container.environment,
                'egg': egg or old.egg_id,
                'image': image or old.container.image,
                'skip_scripts': skip_scripts
            })

        return AppServer(self, data['attributes'])

    def suspend_server(self, _id: int, /) -> None:
        """Suspends a server by its ID.

        id: :class:`int`
            The ID of the server.
        """
        return self._http.post(f'/servers/{_id}/suspend', None)

    def unsuspend_server(self, _id: int, /) -> None:
        """Unsuspends a server by its ID.

        id: :class:`int`
            The ID of the server.
        """
        return self._http.post(f'/servers/{_id}/unsuspend', None)

    def reinstall_server(self, _id: int, /) -> None:
        """Triggers the reinstall process of a server by its ID.

        id: :class:`int`
            The ID of the server.
        """
        return self._http.post(f'/servers/{_id}/reinstall', None)

    def delete_server(self, _id: int, *, force: bool = False) -> None:
        """Deletes a server by its ID.

        id: :class:`int`
            The ID of the server.
        force: Optional[:class:`bool`]
            Whether the server should be deleted with force.
        """
        return self._http.delete(
            f'/servers/{_id}' + ('/force' if force else ''))

    async def get_server_databases(
        self,
        server: int,
        *,
        include: list[str] = None
    ) -> list[AppDatabase]:
        data = await self._http.get(f'/servers/{server}/databases',
                                    include=include)

        return [AppDatabase(**datum['attributes']) for datum in data['data']]

    async def get_server_database(
        self,
        server: int,
        _id: int,
        *,
        include: list[str] = None
    ) -> AppDatabase:
        data = await self._http.get(f'/servers/{server}/databases/{_id}',
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

    async def reset_database_password(self, server: int,
                                      _id: int) -> AppDatabase:
        """Resets the password for a specified database.

        server: :class:`int`
            The ID of the server.
        id: :class:`int`
            The ID of the server database.
        """
        data = await self._http.post(
            f'/servers/{server}/databases/{_id}/reset-password',
            None)

        return AppDatabase(**data['attributes'])

    def delete_database(self, server: int, _id: int) -> None:
        """Deletes a server database by its ID.

        id: :class:`int`
            The ID of the server database.
        """
        return self._http.delete(f'/servers/{server}/databases/{_id}')

    async def get_nodes(
        self,
        *,
        _filter: tuple[str, str] = None,
        include: list[str] = None,
        sort: str = None
    ) -> list[Node]:
        data = await self._http.get('/nodes', _filter=_filter,
                                    include=include, sort=sort)
        return [Node(self, datum['attributes']) for datum in data['data']]

    async def get_node(
        self,
        _id: int,
        *,
        include: list[str] = None
    ) -> Node:
        data = await self._http.get(f'/nodes/{_id}', include=include)
        return Node(self, data['attributes'])

    async def get_deployable_nodes(self,
                                   options: DeployNodeOptions, /) -> list[Node]:  # noqa: E501
        data = await self._http.get('/nodes/deployable',
                                    body=options.to_dict())
        return [Node(self, datum['attributes']) for datum in data['data']]

    async def get_node_configuration(self, _id: int, /) -> NodeConfiguration:
        """Returns the configuration of a specified node.

        id: :class:`int`
            The ID of the node.
        """
        data = await self._http.get(f'/nodes/{_id}/configuration')
        return NodeConfiguration(**data)

    def create_node(self) -> None:
        """TODO: Creates a new node with the given fields."""
        return NotImplemented

    def update_node(self) -> None:
        """TODO: Updates a specified node with the given fields."""
        return NotImplemented

    def delete_node(self, _id: int, /) -> None:
        """Deletes a node by its ID.

        id: :class:`int`
            The ID of the node.
        """
        return self._http.delete(f'/nodes/{_id}')

    async def get_node_allocations(self, node: int, /) -> list[Allocation]:
        data = await self._http.get(f'/nodes/{node}/allocations')
        return [Allocation(**datum['attributes']) for datum in data['data']]

    async def create_node_allocation(
        self,
        node: int,
        *,
        ip: str,
        ports: list[str],
        alias: str = None
    ) -> None:
        """ Create a new allocated node.

        node: :class:`int`
            The ID of the allocation.
        ip: :class:`str`
            The IP for the allocation.
        ports: :class:`list[str]`
            A list of ports or port ranges for the allocation.
        alias: :class:`str`
            Alias name of the allocation.
        """
        await self._http.post(
            f'/nodes/{node}/allocations',
            {
                'ip': ip,
                'alias': alias,
                'ports': ports
            })

    def delete_node_allocation(self, node: int, _id: int) -> None:
        """Deletes an allocation from a node.

        node: :class:`int`
            The ID of the node.
        id: :class:`int`
            The ID of the allocation.
        """
        return self._http.delete(f'/nodes/{node}/allocations/{_id}')

    async def get_locations(self) -> list[Location]:
        data = await self._http.get('/locations')
        return [Location(**datum['attributes']) for datum in data['data']]

    async def get_location(self, _id: int) -> Location:
        data = await self._http.get(f'/locations/{_id}')
        return Location(**data['attributes'])

    async def create_location(self, *, short: str, long: str) -> Location:
        data = await self._http.post('/locations',
                                     {'short': short, 'long': long})

        return Location(**data['attributes'])

    async def update_location(
        self,
        _id: int,
        *,
        short: str = None,
        long: str = None
    ) -> Location:
        old = await self.get_location(_id)
        data = await self._http.patch(
            f'/locations/{_id}',
            {
                'short': short or old.short,
                'long': long or old.long
            })

        return Location(**data['attributes'])

    def delete_location(self, _id: int, /) -> None:
        return self._http.delete(f'/locations/{_id}')

    async def get_nests(self) -> list[Nest]:
        data = await self._http.get('/nests')
        return [Nest(**datum['attributes']) for datum in data['data']]

    async def get_nest(self, nest: int) -> Nest:
        data = await self._http.get(f'/nests/{nest}')
        return Nest(**data['attributes'])

    async def get_nest_eggs(self, nest: int) -> list[Egg]:
        data = await self._http.get(f'/nests/{nest}/eggs')
        return [Egg(**datum['attributes']) for datum in data['data']]

    async def get_nest_egg(self, nest: int, _id: int) -> Egg:
        data = await self._http.get(f'/nests/{nest}/eggs/{_id}')
        return Egg(**data['attributes'])
