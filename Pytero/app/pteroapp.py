from .apprequestmanager import AppRequestManager


class PteroApp:
    def __init__(self, domain: str, auth: str, **kwargs):
        self.domain = domain.removesuffix('/')
        self.auth = auth
        self.options = None
        
        self.ready_at: int = None
        self.ping: float = None
        
        self.requests = AppRequestManager(self)
    
    async def connect(self):
        if self.ready_at:
            raise Exception('pteroapp already connected')
        
        return NotImplemented
