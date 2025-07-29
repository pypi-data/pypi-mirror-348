class BaseService:
    def __init__(self, api_key: str, api_url: str, debug: bool = False) -> None:
        self.api_key: str = api_key
        self.api_url: str = api_url
        self.debug: bool = debug
