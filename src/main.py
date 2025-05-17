from fastapi import FastAPI
from tortoise import Tortoise, generate_config, run_async
from tortoise.contrib.fastapi import RegisterTortoise, register_tortoise
from contextlib import asynccontextmanager
from typing import AsyncGenerator
import os
from src.auth.presentation.rest.api import auth_router
from src.shared.infra.repository.rdb_repository.configs import RDB_CONFIG


@asynccontextmanager
async def lifespan_test(_app: FastAPI) -> AsyncGenerator[None, None]:
    config = generate_config(
        os.getenv("TORTOISE_TEST_DB", "sqlite://:memory:"),
        app_modules={
            "apps": [],
        },
        testing=True,
        connection_label="default",
    )
    async with RegisterTortoise(
        app=_app,
        config=config,
        generate_schemas=True,
        add_exception_handlers=True,
        _create_db=True,
    ):
        # db connected
        # print(Tortoise.get_connection("default"))
        yield
        # app teardown
    # db connections closed
    await Tortoise.close_connections()
    # await Tortoise._drop_databases()


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncGenerator[None, None]:
    if getattr(_app.state, "testing", None):
        async with lifespan_test(_app) as _:
            yield
    else:
        # app startup
        async with RegisterTortoise(
            app=_app,
            config=RDB_CONFIG,
            generate_schemas=True,
            add_exception_handlers=True,
        ):
            yield


app = FastAPI(title="application for schedule service",lifespan=lifespan)
app.include_router(auth_router)

