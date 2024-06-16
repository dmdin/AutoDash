import uvicorn
from presentation.web.main import create_app
from shared.base import logger
from shared.settings import app_settings

uvicorn_app = create_app()

if __name__ == '__main__':
    logger.info(
        'starting server on {}:{} with {} workers',
        app_settings.uvicorn_host,
        app_settings.uvicorn_port,
        app_settings.uvicorn_workers,
    )

    uvicorn.run(
        'web_entrypoint:uvicorn_app',
        host=app_settings.uvicorn_host,
        port=app_settings.uvicorn_port,
        workers=app_settings.uvicorn_workers,
    )
