import tweepy
from app.src.AuthTokens import AuthTokens


class Authentication:

    def __init__(
            self,
            auth_tokens: AuthTokens
    ):
        self.auth_tokens = auth_tokens

    def authenticate(self):
        # == OAuth Authentication ==
        auth = tweepy.OAuthHandler(self.auth_tokens.consumer_key, self.auth_tokens.consumer_secret)
        auth.set_access_token(self.auth_tokens.access_token, self.auth_tokens.access_token_secret)
        return auth

