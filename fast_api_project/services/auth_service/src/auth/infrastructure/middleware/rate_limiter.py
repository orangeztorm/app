import time  # time module for tracking request timestamps
from collections import (
    defaultdict,  # for default dictionary to store request timestamps
)

from fastapi import (  # FastAPI request and exception handling
    HTTPException,
    Request,
    status,
)
from starlette.middleware.base import (
    BaseHTTPMiddleware,  # base class for creating middleware
)


class RateLimiter:  # core logic
    """In memory rate limiter"""

    def __init__(self, request_per_minute: int):
        self.request_per_minute = request_per_minute  # max requests per minute
        self.requests = defaultdict(list)  # store request timestamps

    def is_allowed(self, identifier: str) -> bool:
        now = time.time()  # current timestamp
        minute_ago = now - 60  # timestamp one minute ago

        # Remove old requests
        self.requests[identifier] = [
            req_time for req_time in self.requests[identifier] if req_time > minute_ago
        ]

        # check if within limit
        if len(self.requests[identifier]) < self.request_per_minute:
            self.requests[identifier].append(now)  # log current request
            return True
        return False


class RateLimiterMiddleware(BaseHTTPMiddleware):  # middleware class
    """Rate limit middleware"""

    def __init__(self, app, request_per_minute: int):
        super().__init__(app)
        self.rate_limiter = RateLimiter(request_per_minute)  # instantiate rate limiter

    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host  # identify client by IP

        if not self.rate_limiter.is_allowed(client_ip):
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Too many requests, please try again later.",
            )

        response = await call_next(request)  # proceed with request
        response.headers["X-RateLimit-Limit"] = str(
            self.rate_limiter.request_per_minute
        )

        return response
