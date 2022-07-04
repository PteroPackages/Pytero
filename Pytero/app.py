from .http import RequestManager


__all__ = ('PteroApp')

class PteroApp:
    def __init__(self, url: str, key: str) -> None:
        self.url = url.removesuffix('/')
        self.key = key
        self._http = RequestManager('Application', self.url, key)
    
    def __repr__(self) -> str:
        return 'PteroApp'
    
    @property
    def event(self):
        return self._http.event
