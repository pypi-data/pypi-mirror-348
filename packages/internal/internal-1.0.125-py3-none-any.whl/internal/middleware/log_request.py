import logging
import time

from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware
from ..const import CORRELATION_ID_HEADER_KEY_NAME


class LogRequestMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI, logger: logging.Logger):
        super().__init__(app)
        self.app = app
        self.logger = logger

    async def dispatch(self, request: Request, call_next):
        # 记录请求的URL和参数
        url = request.url.path
        method = request.method
        headers = request.headers
        request_id = headers.get(CORRELATION_ID_HEADER_KEY_NAME, "")
        params = dict(request.query_params)
        body = await request.body()
        self.logger.info(
            f"[Request id: {request_id}] Method: {method}, URL: {url} - Headers: {headers} - Params: {params} - Body: {body} start processing...")

        # 记录请求处理时间
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time

        self.logger.info(
            f"[Request id: {request_id}] Method: {method}, URL: {url} - Headers: {headers} - Params: {params} - Body: {body}, Completed in {process_time:.4f} seconds")
        return response
