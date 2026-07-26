from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.api.api_business_exception import AppBusinessException
from app.api.request_response.global_error_response import GlobalErrorResponse


# --- HANDLER 1: Custom Business Logic Failures ---

async def business_exception_handler(request: Request, exc: AppBusinessException):
    payload = GlobalErrorResponse(
        error_code=exc.error_code,
        message=exc.message
    )
    return JSONResponse(
        status_code=exc.status_code,
        content=payload.model_dump()
    )


# --- HANDLER 2: Override Pydantic Data Validation Errors (422) ---

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    # Re-map Pydantic errors into your clean structured details layout
    error_details = [{"field": err["loc"][-1], "issue": err["msg"]} for err in exc.errors()]

    payload = GlobalErrorResponse(
        error_code="VALIDATION_FAILED",
        message="The request body parameters failed type verification.",
        details=error_details
    )
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=payload.model_dump()
    )


# --- HANDLER 3: Catch-All for Unexpected Server Crashes (500) ---

async def global_unhandled_exception_handler(request: Request, exc: Exception):
    # Log 'exc' securely to terminal or Datadog/Sentry monitoring here
    payload = GlobalErrorResponse(
        error_code="INTERNAL_SERVER_ERROR",
        message="An unexpected server error occurred. Please try again later."
    )
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=payload.model_dump()
    )

# Create a setup function to bundle them together
def init_exception_handlers(app : FastAPI):
    app.add_exception_handler(AppBusinessException, business_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(Exception, global_unhandled_exception_handler)