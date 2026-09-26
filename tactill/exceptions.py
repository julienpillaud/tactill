class TactillError(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)


class TactillRejectedError(TactillError):
    def __init__(self, status_code: int, response: str | None) -> None:
        super().__init__(f"HTTP Error {status_code}")
        self.status_code = status_code
        self.response = response or ""


class TactillUnavailableError(TactillError):
    pass


class TactillUnexpectedResponseError(TactillError):
    pass
