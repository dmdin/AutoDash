from contextlib import asynccontextmanager
import os
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from presentation.web.router import health_router, model_router, parser_router
from presentation.dependencies import container

PARENT = Path(os.path.realpath(__file__)).parent
with open(PARENT / 'rapidoc.html', 'r') as f:
    _rapidoc_html = f.read()


@asynccontextmanager
async def lifespan(app: FastAPI):
    FastAPICache.init(
        RedisBackend(container.redis_repository.r), prefix='fastapi-cache'
    )
    yield


def create_app() -> FastAPI:
    app = FastAPI(title='LCT ML Backend Service', lifespan=lifespan, root_path='/api')

    app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )
    app.include_router(health_router.router)
    app.include_router(parser_router.router)
    app.include_router(model_router.router)

    @app.get('/rapidoc', response_class=HTMLResponse, include_in_schema=False)
    def rapidoc() -> str:
        return _rapidoc_html.format(openapi_url='/openapi.json')

    return app
