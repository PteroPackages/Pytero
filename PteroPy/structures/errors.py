class RequestError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class PteroAPIError(Exception):
    def __init__(self, data: object) -> None:
        err = data['errors'][0]
        super().__init__('%d: %s' % (err['status'], err['detail']))


class WebSocketError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
