from fastapi import APIRouter, status
from fastapi.responses import UJSONResponse
from presentation.dependencies import container
from presentation.web.schemas import HealthResponse, HealthStatuses
from shared.base import logger

router = APIRouter(prefix='')


@router.get(
    '/health',
    response_model=HealthResponse,
    response_model_exclude_none=True,
)
async def check_server_health() -> UJSONResponse:
    """
    Check service health
    """
    try:
        await container.heath_service.check()
    except Exception as exc:
        logger.exception('Exception while checking health')
        return UJSONResponse(
            content=HealthResponse(
                status=HealthStatuses.ERR, error=f'{exc.__class__.__name__}: {str(exc)}'
            ).jsonable_encoder(by_alias=True),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return UJSONResponse(
        HealthResponse(status=HealthStatuses.OK).jsonable_encoder(by_alias=True)
    )
