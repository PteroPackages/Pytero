class EventError(Exception):
    '''Raised when there is an error with an event'''
    pass


class PteroAPIError(Exception):
    '''The error object received from Pterodactyl when there is an error'''
    
    def __init__(
            self,
            message: str,
            data: dict[str, list[dict[str, str]]]) -> None:
        super().__init__(message)
        self.codes: dict[int, str] = {}
        self.details: dict[int, str] = {}
        self.statuses: dict[int, int] = {}
        
        for i in range(len(data['errors'])):
            self.codes[i] = data['errors'][i]['code']
            self.details[i] = data['errors'][i]['detail']
            self.statuses[i] = int(data['errors'][i]['status'])
    
    def __getitem__(self, index: int) -> dict[str, int | str]:
        err: dict[str, int | str] = {}
        err['code'] = self.codes[index]
        err['detail'] = self.details[index]
        err['status'] = self.statuses[index]
        
        return err


class RequestError(Exception):
    '''Errors received upon requesting a Pterodactyl endpoint'''
    pass


class ValidationError(Exception):
    '''Errors received when a request validation fails'''
    pass
