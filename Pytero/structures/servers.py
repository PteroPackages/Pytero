from typing import Optional
from .node import Node
from ..types import _PteroApp
from .users import PteroUser
from ..util import transform


class AppServer:
    def __init__(self, client: _PteroApp, data: dict[str,]) -> None:
        self.client = client
        self.id: int = data['id']
        self.uuid: str = data['uuid']
        self.identifier: str = data['identifier']
        self.created_at: str = data['created_at']
        self._deleted: bool = False
        
        self._patch(data)
    
    def _patch(self, data: dict[str,]) -> None:
        self.name: str = data.get('name')
        self.description: Optional[str] = data.get('description', None)
        self.external_id: Optional[str] = data.get('external_id', None)
        self.suspended: bool = data.get('suspended')
        self.usable: bool = not self.suspended or True
        self.limits: dict[str,] = data.get('limits')
        self.feature_limits: dict[str,] = data.get('feature_limits')
        self.owner_id: int = data.get('user')
        self.owner: Optional[PteroUser] = None
        self.node_id: int = data.get('node')
        self.node: Optional[Node] = None
        self.allocation: int = data.get('allocation')
        self.nest: int = data.get('nest')
        self.egg: int = data.get('egg')
    
    def __str__(self) -> str:
        return self.name
    
    def __repr__(self) -> str:
        return '<AppServer id=%d owner=%d>' \
            % (self.id, self.owner_id)
    
    def to_dict(self) -> dict[str,]:
        return transform(
            self,
            ignore=['client', 'owner', 'node'],
            maps={'owner_id': 'user', 'node_id': 'node'}
        )
    
    async def get_owner(self):
        if self.owner is None:
            self.owner = await self.client.users.fetch(
                self.owner_id, force=True
            )
        
        return self.owner
    
    async def update_details(
        self,
        *,
        name: str = None,
        owner: int = None,
        external_id: int = None,
        description: str = None
    ):
        data = await self.client.servers.update_details(
            self.id,
            name=name,
            owner=owner,
            external_id=external_id,
            description=description
        )
        self._patch(data.to_dict())
    
    async def update_build(
        self,
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
        data = await self.client.servers.update_build(
            self.id,
            allocation=allocation,
            swap=swap,
            memory=memory,
            disk=disk,
            cpu=cpu,
            threads=threads,
            io=io,
            feature_limits=feature_limits
        )
        return data
    
    async def update_startup(
        self,
        *,
        startup: str = None,
        environment: dict[str,] = {},
        egg: int = None,
        image: str = None,
        skip_scripts: bool = False
    ):
        data = await self.client.servers.update_startup(
            self.id,
            startup=startup,
            environment=environment,
            egg=egg,
            image=image,
            skip_scripts=skip_scripts
        )
        return data
    
    async def suspend(self):
        await self.client.servers.suspend(self.id)
        self.suspended = True
        self.usable = False
    
    async def unsuspend(self):
        await self.client.servers.unsuspend(self.id)
        self.suspended = False
        self.usable = True
    
    async def reinstall(self):
        await self.client.servers.reinstall(self.id)
        self.usable = False
    
    async def delete(self, force: bool = False):
        await self.client.servers.delete(self.id, force)
        self._deleted = True
        self.usable = False
