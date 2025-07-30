from typing import List, Dict, Any
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.middleware.base import BaseHTTPMiddleware

from ..middlewares import runtime, http_exception, validation_exception
from ..routes.router import Router


__all__ = (
    'SubApp',
)


class SubApp:
    def __init__(
        self,
        application_title: str,
        version: str = "*",
        redoc_url: str = "/",
        docs_url: str = "/swagger",
        middlewares: List = None,
        routers: List[Router] = None,
        gzip_compression: int = None,
        session_middleware_settings: Dict[str, Any] = None,
    ):
        """
        Initialize a SubApp instance and create the FastAPI application.
        """
        self.application_title = application_title
        self.version = version
        self.redoc_url = redoc_url
        self.docs_url = docs_url
        self.middlewares = middlewares or []
        self.routers = routers or []
        self.gzip_compression = gzip_compression
        self.session_middleware_settings = session_middleware_settings or {}
        self.app = self._create_app()

    def _create_app(self) -> FastAPI:
        """
        Create and configure a FastAPI application.
        """
        app = FastAPI(
            title=self.application_title,
            version=self.version,
            redoc_url=self.redoc_url,
            docs_url=self.docs_url,
            swagger_ui_parameters={"defaultModelsExpandDepth": -1},
        )

        # Add GZip middleware
        if self.gzip_compression is not None:
            from fastapi.middleware.gzip import GZipMiddleware
            app.add_middleware(GZipMiddleware, minimum_size=self.gzip_compression)

        # Add custom middlewares
        applicable_middlewares = [runtime.Runtime()] + self.middlewares
        for middleware in applicable_middlewares:
            app.add_middleware(BaseHTTPMiddleware, dispatch=middleware)

        # Add session middleware if settings provided
        if self.session_middleware_settings:
            from starlette.middleware.sessions import SessionMiddleware
            app.add_middleware(
                SessionMiddleware,
                **self.session_middleware_settings
            )

        # Exception handlers
        @app.exception_handler(StarletteHTTPException)
        async def http_exception_handler(request, exc):
            return await http_exception.http_exception_handler(request, exc)

        @app.exception_handler(RequestValidationError)
        async def validation_exception_handler(request, exc):
            return await validation_exception.validation_exception_handler(request, exc)

        # Add routers
        for router in self.routers:
            app.include_router(router=router.get_router())

        return app

    def get_app(self) -> FastAPI:
        """
        Get the created FastAPI application instance.
        """
        return self.app
