import time
from typing import Optional
from fastapi import Request
from sqlalchemy.exc import SQLAlchemyError
from fastapi.responses import JSONResponse
from starlette.types import Scope, Receive, Send
from elrahapi.middleware.crud_middleware import save_log
from elrahapi.exception.custom_http_exception import (
    CustomHttpException as CHE,
)
from elrahapi.session.session_manager import SessionManager
from elrahapi.websocket.connection_manager import ConnectionManager


class ErrorHandlingMiddleware:
    def __init__(
        self,
        app,
        LogModel=None,
        session_manager: Optional[SessionManager] = None,
        websocket_manager: ConnectionManager = None,
    ):
        self.app = app
        self.LogModel = LogModel
        self.session_manager = session_manager
        self.websocket_manager = websocket_manager
        self.has_log = self.session_manager and self.LogModel

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        if scope["type"] not in ("http"):
            await self.app(scope, receive, send)
            return

        request = Request(scope, receive=receive)
        db = self.session_manager.yield_session()if self.has_log else None

        try:
            request.state.start_time = time.time()
            await self.app(scope, receive, send)
        except CHE as custom_http_exc:
            http_exc = custom_http_exc.http_exception
            response = self._create_json_response(
                http_exc.status_code, {"detail": http_exc.detail}
            )
            await self._log_error(
                request, db, response, f"Custom HTTP error: {http_exc.detail}"
            )
            await response(scope, receive, send)
        except SQLAlchemyError as db_error:
            response = self._create_json_response(
                500, {"error": "Database error", "details": str(db_error)}
            )
            await self._log_error(request, db, response, f"Database error: {db_error}")
            await response(scope, receive, send)
        except Exception as exc:
            response = self._create_json_response(
                500, {"error": "Unexpected error", "details": str(exc)}
            )
            await self._log_error(request, db, response, f"Unexpected error: {exc}")
            await response(scope,receive,send)
        finally:
            if db:
                db.close()

    def _create_json_response(self, status_code, content):
        return JSONResponse(status_code=status_code, content=content)

    async def _log_error(self, request, db, response, error):
        if self.has_log:
            await save_log(
                request=request,
                LogModel=self.LogModel,
                db=db,
                response=response,
                websocket_manager=self.websocket_manager,
                error=error,
            )
