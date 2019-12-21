class AuthTokens:
    def __init__(
            self,
            consumer_key: str,
            consumer_secret: str,
            access_token: str,
            access_token_secret: str
    ):
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.access_token = access_token
        self.access_token_secret = access_token_secret
