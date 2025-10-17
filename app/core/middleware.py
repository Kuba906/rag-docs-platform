import time, uuid
from collections import deque
import structlog
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

_logger = structlog.get_logger()
_lat = deque(maxlen=500)

class RequestIdMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        rid = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        request.state.request_id = rid
        resp: Response = await call_next(request)
        resp.headers["X-Request-ID"] = rid
        return resp

class MetricsMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        t0 = time.perf_counter()
        resp: Response = await call_next(request)
        dur = (time.perf_counter() - t0) * 1000
        _lat.append(dur)
        n = len(_lat)
        if n >= 20 and n % 20 == 0:
            p95 = sorted(_lat)[max(int(0.95*n)-1, 0)]
            _logger.info("api_latency", p95_ms=round(p95,2), count=n)
        resp.headers["X-Response-Time-ms"] = f"{dur:.2f}"
        return resp
