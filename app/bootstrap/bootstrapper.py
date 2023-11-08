from json import JSONEncoder
from logging import Logger
from typing import Any
from uuid import UUID

from fastapi import FastAPI, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from felix_library.interfaces.telemetry.telemetry_interface import TelemetryInterface
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.logging import LoggingInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from pydantic import ValidationError

from app.bootstrap.open_telemetry_middleware import OpenTelemetryMiddleware
from app.components.components import Components
from app.entities.application_error import get_error_responses_schema
from app.exceptions.client_error import ClientError, ClientErrorType
from app.exceptions.server_error import ServerError, ServerErrorType
from app.routers.api.v1.examples import example


def boostrap(components: Components) -> FastAPI:
    telemetry: TelemetryInterface = components.get_component('telemetry')
    app: FastAPI = FastAPI(responses=get_error_responses_schema())

    attach_cors(app)
    attach_app_routers(app)
    attach_app_default_handler(app)
    attach_app_exception_handlers(app, components.get_component('logger').get_logger('fast_api_exception_handler'))

    app.add_middleware(OpenTelemetryMiddleware)

    # Monkey patch for the following issue: https://github.com/jazzband/django-push-notifications/issues/586
    rewrite_json_encoder()

    RequestsInstrumentor().instrument()
    FastAPIInstrumentor.instrument_app(app, tracer_provider=telemetry.get_tracer_provider())
    LoggingInstrumentor().instrument(set_logging_format=True)

    return app


def attach_cors(
    app: FastAPI
) -> None:
    origins: list[str] = ['*']
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )


def attach_app_routers(app: FastAPI) -> None:
    app.include_router(example.router, prefix='/api/v1/examples', tags=['examples'])


def attach_app_default_handler(app: FastAPI) -> None:
    @app.get('/', include_in_schema=False)
    async def index() -> str:
        return 'Félix <NAME OF YOUR SERVICE> Service'


def attach_app_exception_handlers(app: FastAPI, logger: Logger) -> None:
    @app.exception_handler(RequestValidationError)
    async def request_validation_exception_handler(_, e: RequestValidationError) -> JSONResponse:
        logger.error('RequestValidationError handled %s', e)
        return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content={'message': e.json()})

    @app.exception_handler(ValidationError)
    async def validation_exception_handler(_, e: ValidationError) -> JSONResponse:
        logger.error('ValidationError handled %s', e)

        return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content={'message': e.json()})

    @app.exception_handler(ClientError)
    async def client_exception_handler(_, e: ClientError) -> JSONResponse:
        logger.error('ClientError handled %s', e)

        if e.client_error_type == ClientErrorType.INVALID_INPUT:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={'message': e.message})
        elif e.client_error_type == ClientErrorType.UNAUTHORIZED:
            return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={'message': e.message})
        elif e.client_error_type == ClientErrorType.FORBIDDEN:
            return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={'message': e.message})
        elif e.client_error_type == ClientErrorType.NOT_FOUND:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={'message': e.message})
        else:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={'message': e.message})

    @app.exception_handler(ServerError)
    async def server_exception_handler(_, e: ServerError) -> JSONResponse:
        logger.error('ServerError handled %s ', e)

        if e.server_error_type == ServerErrorType.INTERNAL_SERVER_ERROR:
            return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={'message': e.message})
        else:
            return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={'message': e.message})


def rewrite_json_encoder() -> None:
    old_default = JSONEncoder.default

    def new_default(self: JSONEncoder, o: Any) -> Any:
        if isinstance(o, UUID):
            return str(o)
        return old_default(self, o)

    JSONEncoder.default = new_default  # type: ignore
