class RequestError(Exception):
    pass


class PteroAPIError(Exception):
    def __init__(self, data: object) -> None:
        err = data['errors'][0]
        super().__init__('%d: %s' % (err['status'], err['detail']))


class WebSocketError(Exception):
    pass
