from typing import Callable
from .eggs_manager import EggsManager
from .location_manager import LocationManager
from .nest_manager import NestManager
from .node_manager import NodeManager
from .user_manager import UserManager
from ..requests import RequestManager


class PteroApp:
    def __init__(self, domain: str, auth: str, **_):
        self.domain = domain.removesuffix('/')
        self.auth = auth
        self.options = None # TODO: use kwargs
        
        self.eggs = EggsManager(self)
        self.locations = LocationManager(self)
        self.nests = NestManager(self)
        self.nodes = NodeManager(self)
        self.requests = RequestManager('Application', self.domain, self.auth)
        self.users = UserManager(self)
    
    def on_receive(self, func: Callable[[dict[str,]], None]):
        return self.requests.on_receive(func)
    
    def on_debug(self, func: Callable[[str], None]):
        return self.requests.on_debug(func)
