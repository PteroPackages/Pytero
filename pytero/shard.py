from aiohttp import ClientSession, ClientWebSocketResponse, WSMessage
from json import loads
from time import time
from typing import Callable, Optional
from .errors import ShardError
from .events import Emitter
from .types import WebSocketEvent


__all__ = ('Shard')

class Shard(Emitter):
    def __init__(self, http, identifier: str) -> None:
        super().__init__()
        self._http = http
        self._conn: ClientWebSocketResponse = None
        self.origin: str = http.url
        self.identifier: str = identifier
        self.ping: float = float('nan')
        self.last_ping: float = float('nan')
    
    def __repr__(self) -> str:
        return '<Shard identifier=%s status=%s>' % (self.identifier, self.status)
    
    @property
    def closed(self) -> bool:
        return self._conn is None
    
    def event(self, func: Callable[[str], None]) -> Callable[[str], None]:
        super().add_event(func.__name__, func)
        return func
    
    async def _debug(self, msg: str) -> None:
        await super().emit_event('on_debug', 'debug %s: %s' % (self.identifier, msg))
    
    def _evt(self, name: str, args: list[str] = []) -> dict[str, list[str]]:
        return {'event': name, 'args': args}
    
    async def _heartbeat(self) -> None:
        if self.closed:
            raise ShardError('connection not available for this shard')
        
        auth: dict[str,] = await self._http.get(f'/servers/{self.identifier}/websocket')
        await self._conn.send_json(self._evt('auth', auth['data']['token']))
    
    async def launch(self) -> None:
        if not self.closed:
            return
        
        auth: dict[str,] = await self._http.get(f'/servers/{self.identifier}/websocket')
        await self._debug('attempting to connect to websocket')
        
        async with ClientSession() as session:
            async with session.ws_connect(auth['data']['socket'], origin=self.origin) as self._conn:
                await self._debug('authenticating connection')
                await self._conn.send_json(self._evt('auth', auth['data']['token']))
                
                async for msg in self._conn:
                    await self._on_event(msg)
    
    def destroy(self) -> None:
        if not self.closed:
            self._conn.close()
            self._conn = None
    
    async def _on_event(self, event: WSMessage) -> None:
        json = event.json()
        await self._debug('received event: %s' % data.event)
        await super().emit_event('on_raw', event.json())
        data = WebSocketEvent(**json)
        
        match data.event:
            case 'auth success':
                self.ping = time() - self.last_ping
                self.last_ping = time()
            case 'token expiring':
                await self._heartbeat()
            case 'token expired':
                self.destroy()
                await self.launch()
            case _:
                parsed: Optional[dict[str,]] = None
                if data.args is not None:
                    parsed = loads(''.join(data.args))
                
                await super().emit_event(data.event, parsed)
