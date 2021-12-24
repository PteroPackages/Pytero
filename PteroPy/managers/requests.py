from ..structures.errors import PteroAPIError, RequestError
import asyncio
from time import time
from json import loads
from aiohttp import ClientSession
from typing import Any, Coroutine, Dict, Union


METHODS = ('GET', 'POST', 'PATCH', 'PUT', 'DELETE')

class RequestManager:
    def __init__(self, client, _type: str) -> None:
        self.client = client
        self._type = _type
        self.headers = {
            'User-Agent': f'{_type} PteroPy v0.0.1a',
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f'Bearer {client.auth}'
        }
        self.loop: asyncio.AbstractEventLoop = asyncio.get_event_loop()
        self.session = ClientSession(loop=self.loop)
        self.suspended = False
    
    async def _make(self, path, method: str = 'GET', params: Dict[str, Any] = None) -> Coroutine[Any, Any, Union[Any, None]]:
        if self.client.ping is None:
            raise RequestError(f'attempted request before {self._type} was ready')
        
        if self.suspended:
            raise RequestError(f'[429] {self._type} is ratelimited')
        
        if method not in METHODS:
            raise KeyError("invalid request method '%s'" % method)
        
        _exec_method = self.session.get
        if method == 'POST':
            _exec_method = self.session.post
        elif method == 'PATCH':
            _exec_method = self.session.patch
        elif method == 'PUT':
            _exec_method = self.session.put
        elif method == 'DELETE':
            _exec_method = self.session.delete
        
        body: str = None
        if params is not None:
            if params.get('_raw'):
                body = params
            else:
                body = loads(params)
        
        async with _exec_method(self.client.domain + path, params=body, headers=self.headers) as res:
            if res.status in (201, 204):
                return
            
            if res.status == 200:
                return await res.json()
            
            if res.status in (400, 404, 422):
                data = await res.json()
                raise PteroAPIError(data)
            
            if res.status == 401: raise RequestError('[401] unauthorised api request')
            if res.status == 403: raise RequestError('[403] endpoint forbidden')
            if res.status == 429:
                self.suspended = True
                raise RequestError(f'[429] {self._type} is ratelimited')
            
            raise RequestError(
                'Pterodactyl API returned an invalid or malformed payload: %d'
                % res.status
            )
    
    async def get(self, path: str):
        return await self._make(path)
    
    async def post(self, path: str, params: Dict[str, Any]):
        return await self._make(path, 'POST', params)
    
    async def patch(self, path: str, params: Dict[str, Any]):
        return await self._make(path, 'PATCH', params)
    
    async def put(self, path: str, params: Dict[str, Any]):
        return await self._make(path, 'PUT', params)
    
    async def delete(self, path: str):
        return await self._make(path, 'DELETE')
    
    async def ping(self) -> Coroutine[bool, None, None]:
        self.client.ping = -1
        now = time()
        try:
            await self.get('/api/application')
        except Exception as e:
            if isinstance(e, PteroAPIError):
                self.client.ping = time() - now
                return True
            else:
                raise e
    
    async def close(self):
        if self.session is None:
            return
        
        try:
            await self.session.close()
        except:
            pass
        
        self.session = None
        self.suspended = False
