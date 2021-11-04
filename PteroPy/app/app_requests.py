from .pteroapp import PteroApp
from ..structures.errors import RequestError, PteroAPIError
from json import loads
from aiohttp import ClientSession


class AppRequestManager:
    headers = {
        'User-Agent': 'Application PteroPy v0.0.1a',
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    
    def __init__(self, client: PteroApp) -> None:
        self.client = client
        self.headers['Authorization'] = 'Bearer '+ client.auth
        self.session = ClientSession()
        self.suspended = False
    
    async def make(self, path, method: str = 'GET', params: dict = None):
        if self.client.ping is None:
            raise RequestError('attempted request before application was ready')
        
        if self.suspended:
            raise RequestError('[429] application is ratelimited')
        
        body: str = None
        if params is not None:
            if params.get('_raw'):
                body = params
            else:
                body = loads(params)
        
        async with self.session.get(self.client.domain + path,
                                    body=body, headers=self.headers) as response:
            if response.status in (201, 204):
                return
            
            if response.status == 200:
                return await response.json()
            
            if response.status in (400, 404, 422):
                data = await response.json()
                raise PteroAPIError(data)
            
            if response.status == 401: raise RequestError('[401] unauthorised api request')
            if response.status == 403: raise RequestError('[403] endpoint forbidden')
            if response.status == 429:
                self.suspended = True
                raise RequestError('[429] application is ratelimited')
            
            raise RequestError('Pterodactyl API returned an invalid or malformed payload: %d'
                            % response.status)
    
    async def ping(self) -> bool:
        try:
            self.client.ping = -1
            await self.make('/api/application')
        except (Exception, PteroAPIError) as e:
            if isinstance(e, PteroAPIError):
                return True
            else:
                raise e