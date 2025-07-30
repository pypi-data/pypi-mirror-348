from typing import Any, List, Tuple, Dict
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware

from .sub import SubApp


__all__ = (
    'MainApp',
)


class MainApp:
    def __init__(
        self,
        application_title: str,
        applications: List[Tuple[str, SubApp]],
        lifespan: Any = None,
        version: str = "*",
        redirection_path: str = None,
        redoc_url: str | None = None,
        docs_url: str | None = None,
        cors_settings: Dict[str, Any] = None,
    ):
        """
        Initialize a MainApp instance and create the FastAPI application.
        """
        self.application_title = application_title
        self.applications = applications
        self.version = version
        self.redirection_path = redirection_path
        self.redoc_url = redoc_url
        self.docs_url = docs_url
        self.lifespan = lifespan or None
        self.cors_settings = dict(
            allow_credentials=["*"],
            allow_methods=["*"],
            allow_headers=["*"],
            allow_origins=["*"],
            allow_origin_regex=None,
            expose_headers=[],
            max_age=600,
        )
        self.cors_settings.update(cors_settings or {})
        self.app = self._create_app()

    def _create_app(self) -> FastAPI:
        """
        Create and configure the FastAPI application.
        """

        # Default redirection path
        if self.redirection_path is None and self.applications:
            self.redirection_path = self.applications[0][0]

        # Initialize FastAPI app
        app = FastAPI(
            title=self.application_title,
            version=self.version,
            redoc_url=self.redoc_url,
            docs_url=self.docs_url,
            swagger_ui_parameters={"defaultModelsExpandDepth": -1},
            lifespan=self.lifespan,
        )

        # Add CORS middleware
        if self.cors_settings:
            app.add_middleware(
                CORSMiddleware,
                **self.cors_settings
            )

        # Mount sub-applications
        for path, application in self.applications:
            app.mount(path, application.get_app())

        # Redirect root to the specified path
        if self.redirection_path:
            @app.get("/", status_code=302)
            async def redirect():
                return RedirectResponse(self.redirection_path)

        return app

    def get_app(self) -> FastAPI:
        """
        Get the created FastAPI application instance.
        """
        return self.app
