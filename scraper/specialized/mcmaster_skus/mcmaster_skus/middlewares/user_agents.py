
import random

from .constants import USER_AGENTS


class UserAgentsMiddleware:

    def process_request(self, request, spider):
        request.headers.setdefault('User-Agent', random.choice(USER_AGENTS))
