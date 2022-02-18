from time import time
from typing import Callable
from ..requests import RequestError, PteroAPIError, RequestManager


class PteroApp:
    def __init__(self, domain: str, auth: str, **kwargs):
        self.domain = domain.removesuffix('/')
        self.auth = auth
        self.options = None # TODO: use kwargs
        
        self.ready_at = 0.0
        self.ping = -1.0
        
        self.requests = RequestManager('Application', self.domain, self.auth)
    
    async def connect(self) -> bool:
        if self.ready_at:
            raise Exception('pteroapp already connected')
        
        start = time()
        try:
            await self.requests.rget('/application/api')
        except PteroAPIError:
            self.ping = time() - start
        except Exception as e:
            raise RequestError(
                'pterodactyl api is unavailable\nresponse: %s' % str(e)
            )
        
        self.ready_at = time()
        return True
    
    def on_receive(self, func: Callable[[dict[str,]], None]):
        return self.requests.on_receive(func)
    
    def on_debug(self, func: Callable[[str], None]):
        return self.requests.on_debug(func)
