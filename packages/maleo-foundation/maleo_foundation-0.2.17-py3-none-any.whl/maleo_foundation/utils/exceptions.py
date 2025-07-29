from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from functools import wraps
from starlette.exceptions import HTTPException as StarletteHTTPException
from sqlalchemy.exc import SQLAlchemyError
from typing import Optional
from maleo_foundation.models.responses import BaseResponses
from maleo_foundation.models.transfers.results.service.general \
    import BaseServiceGeneralResultsTransfers
from maleo_foundation.models.transfers.results.service.query \
    import BaseServiceQueryResultsTransfers
from maleo_foundation.utils.logging import BaseLogger

class BaseExceptions:
    @staticmethod
    def authentication_error_handler(request:Request, exc:Exception):
        return JSONResponse(
            content=BaseResponses.Unauthorized(other=str(exc)).model_dump(mode="json"),
            status_code=status.HTTP_401_UNAUTHORIZED
        )

    @staticmethod
    async def validation_exception_handler(request:Request, exc:RequestValidationError):
        return JSONResponse(
            content=BaseResponses.ValidationError(other=exc.errors()).model_dump(mode="json"),
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
        )

    @staticmethod
    async def http_exception_handler(request:Request, exc:StarletteHTTPException):
        if exc.status_code in BaseResponses.other_responses:
            return JSONResponse(
                content=BaseResponses.other_responses[exc.status_code]["model"]().model_dump(mode="json"),
                status_code=exc.status_code
            )

        return JSONResponse(
            content=BaseResponses.ServerError().model_dump(mode="json"),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    @staticmethod
    def database_exception_handler(
        operation:str,
        logger:Optional[BaseLogger] = None,
        fail_result_class:type[BaseServiceQueryResultsTransfers.Fail] = BaseServiceQueryResultsTransfers.Fail
    ):
        """Decorator to handle database-related exceptions consistently."""
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                try:
                    return func(*args, **kwargs)
                except SQLAlchemyError as e:
                    logger.error("Database error occurred while %s: '%s'", operation, str(e), exc_info=True)
                    return fail_result_class(
                        message=f"Failed {operation}",
                        description=f"A database error occurred while {operation}. Please try again later or contact administrator.",
                        other="Database operation failed"
                    )
                except Exception as e:
                    logger.error("Unexpected error occurred while %s: '%s'", operation, str(e), exc_info=True)
                    return fail_result_class(
                        message=f"Failed {operation}",
                        description=f"An unexpected error occurred while {operation}. Please try again later or contact administrator.",
                        other="Internal processing error"
                    )
            return wrapper
        return decorator

    @staticmethod
    def service_exception_handler(
        operation:str,
        logger:Optional[BaseLogger] = None,
        fail_result_class:type[BaseServiceGeneralResultsTransfers.Fail] = BaseServiceGeneralResultsTransfers.Fail
    ):
        """Decorator to handle service-related exceptions consistently."""
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    logger.error("Unexpected error occurred while %s: '%s'", operation, str(e), exc_info=True)
                    return fail_result_class(
                        message=f"Failed {operation}",
                        description=f"An unexpected error occurred while {operation}. Please try again later or contact administrator.",
                        other="Internal processing error"
                    )
            return wrapper
        return decorator