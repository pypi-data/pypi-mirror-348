from litestar.connection import ASGIConnection as ASGIConnection
from litestar.middleware.authentication import AbstractAuthenticationMiddleware, AuthenticationResult
from litestar.middleware.base import ASGIMiddleware
from litestar.types import ASGIApp as ASGIApp, Receive as Receive, Scope as Scope, Send as Send

DEFAULT_AUTH_TOKEN_MAX_AGE: int

class BearerTokenAuthenticationMiddleware(AbstractAuthenticationMiddleware):
    async def ensure_bearer_token(self, connection: ASGIConnection) -> str: ...

class TimestampHmacAuthenticationMiddleware(BearerTokenAuthenticationMiddleware):
    async def authenticate_request(self, connection: ASGIConnection) -> AuthenticationResult: ...

class JwtAuthenticationMiddleware(BearerTokenAuthenticationMiddleware):
    async def authenticate_request(self, connection: ASGIConnection) -> AuthenticationResult: ...

class ActivateJwtOnApiKeyMiddleware(ASGIMiddleware):
    """Middleware to activate JWT on API key"""
    async def handle(self, scope: Scope, receive: Receive, send: Send, next_app: ASGIApp) -> None: ...
