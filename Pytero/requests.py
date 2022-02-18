from aiohttp import ClientSession
from typing import Callable, Optional
import json
from .events import EventManager
from .errors import RequestError, PteroAPIError


class RequestManager(EventManager):
    def __init__(self, _type: str, domain: str, auth: str) -> None:
        super().__init__()
        self._type = _type
        self.domain = domain
        self.auth = auth
        self.suspended = False
    
    def get_headers(self) -> dict[str, str]:
        if self._type is None:
            raise TypeError('api type is required for requests')
        
        if self.auth is None:
            raise TypeError('missing authorization for requests')
        
        return {
            'User-Agent': '%s Pytero v0.0.1a' % self._type,
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': 'Bearer %s' % self.auth
        }
    
    async def _make(self, path: str, method: str, params: dict = None):
        if method not in ('GET', 'POST', 'PATCH', 'PUT', 'DELETE'):
            raise ValueError("invalid http method '%s'" % method)
        
        body: Optional[str] = None
        if params is not None:
            if params.get('raw'):
                await self.__debug('sending raw byte payload')
                body = params
            else:
                await self.__debug('sending json payload')
                body = json.dumps(params)
        
        await self.__debug('attempting to start session')
        async with ClientSession() as session:
            await self.__debug('attemping to perform request')
            async with getattr(session, method.lower())(
                self.domain + path,
                params=body,
                headers=self.get_headers()
            ) as response:
                await self.__debug('ensuring session close before continuing')
                await session.close()
                await self.__debug('received status: %d' % response.status)
                
                if response.status == 204:
                    return None
                
                if response.status in (200, 201):
                    data: dict[str,] = await response.json()
                    await super().emit_event('receive', data)
                    return data
                
                if 400 >= response.status < 500:
                    raise PteroAPIError(await response.json())
                
                raise RequestError(
                    'pterodactyl api returned an invalid or unacceptable response (status: %d)'
                    % response.status
                )
    
    async def rget(self, path: str):
        return await self._make(path, 'GET')
    
    async def rpost(self, path: str, params: dict = None):
        return await self._make(path, 'POST', params)
    
    async def rpatch(self, path: str, params: dict = None):
        return await self._make(path, 'PATCH', params)
    
    async def rput(self, path: str, params: dict = None):
        return await self._make(path, 'PUT', params)
    
    async def rdelete(self, path: str):
        return await self._make(path, 'DELETE')
    
    async def __debug(self, message: str) -> None:
        await super().emit_event('debug', message)
    
    def on_receive(self, func: Callable[[dict[str,]], None]) -> Callable[[dict[str,]], None]:
        super().add_event_slot('receive', func)
        return func
    
    def on_debug(self, func: Callable[[str], None]) -> Callable[[str], None]:
        super().add_event_slot('debug', func)
        return func
