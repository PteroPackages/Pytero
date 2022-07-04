from aiohttp import ClientSession, ClientResponse
from json import dumps
from time import time
from typing import Callable, Optional
from .errors import PteroAPIError, RequestError
from .events import Emitter


__all__ = ('RequestManager')

class RequestManager(Emitter):
    def __init__(self, api: str, url: str, key: str) -> None:
        super().__init__()
        self._api = api
        self.url = url
        self.key = key
        self.ping: float = float('nan')
    
    def get_headers(self, content: str) -> dict[str, str]:
        return {
            'User-Agent': '%s Pytero v0.1.0' % self._api,
            'Content-Type': content,
            'Accept': 'application/json,text/plain',
            'Authorization': 'Bearer %s' % self.key}
    
    def _validate_query(self) -> str:
        ...
    
    async def _make(
        self,
        method: str,
        path: str,
        *,
        body = None,
        content: str = 'application/json',
        filter: tuple[str, str] = (),
        include: list[str] = [],
        sort: tuple[str, str] = ()
    ):
        if method not in ('GET', 'POST', 'PATCH', 'PUT', 'DELETE'):
            raise KeyError("invalid http method '%s'" % method)
        
        payload = None
        if body:
            if content == 'application/json':
                payload = dumps(body)
            else:
                payload = body
        
        query = self._validate_query(filter, include, sort)
        async with ClientSession() as session:
            start = time()
            async with getattr(session, method.lower())(
                self.url + path + query,
                data=payload,
                headers=self.get_headers(content)
            ) as response:
                self.ping = time() - start
                response: ClientResponse
                
                if response.status == 204:
                    return None
                
                if response.status in (200, 201, 202):
                    if response.headers.get('content-type') == 'application/json':
                        data = await response.json()
                        return data
                    else:
                        data = await response.text()
                        return data
                
                if 400 <= response.status < 500:
                    err: dict[str,] = await response.json()
                    raise PteroAPIError(err['errors'][0]['code'], err)
                
                raise RequestError(
                    'pterodactyl api returned an invalid or unacceptable'
                    ' response (status: %d)' % response.status)
    
    def event(self, func: Callable[[str], None]) -> Callable[[str], None]:
        super().add_event(func.__name__, func)
        return func
