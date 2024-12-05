from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

from common.logger import log
from utils.timezone import timezone


class AccessMiddleware(BaseHTTPMiddleware):
  """Промежуточное программное обеспечение журнала запросов"""

  async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
    start_time = timezone.now()
    response = await call_next(request)
    end_time = timezone.now()
    log.info(
        f'{request.client.host: <15} | {request.method: <8} | {response.status_code: <6} | '
        f'{request.url.path} | {round((end_time - start_time).total_seconds(), 3) * 1000.0}ms'
    )
    return response
