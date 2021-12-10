from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from utilities.helpers import querystring_to_dict
from rest_framework.authtoken.models import Token

@database_sync_to_async
def get_user(token:str):
    try:
        obj = Token.objects.get(key=token)
        return obj.user
    except Token.DoesNotExist:
        return AnonymousUser()




class QueryAuthMiddleware:
    """
    Custom middleware (insecure) that takes user IDs from the query string.
    """

    def __init__(self, app):
        # Store the ASGI application we were passed
        self.app = app

    async def __call__(self, scope, receive, send):
        # Look up user from query string (you should also do things like
        # checking if it is a valid user ID, or if scope["user"] is already
        # populated).
        querystring:str = scope["query_string"].decode()
        kwargs = querystring_to_dict(querystring)
        scope['user'] = await get_user(kwargs.get("token"))
        return await self.app(scope, receive, send)