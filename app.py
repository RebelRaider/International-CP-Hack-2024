import sys

from fastapi import FastAPI
from loguru import logger
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware

from configs.Environment import get_environment_variables
from errors.handlers import init_exception_handlers

from routing.v1.auth import router as auth_router
from routing.v1.metric import router as metric_router
from routing.v1.card import router as card_router
from routing.v1.vacancy import router as vacancy_router
from routing.v1.personality_model import router as personality_model_router

app = FastAPI(openapi_url="/api/v1/openapi.json", docs_url="/api/v1/core/docs")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "https://91.224.87.165.sslip.io"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(TrustedHostMiddleware, allowed_hosts=["*"])

init_exception_handlers(app)

env = get_environment_variables()

if not env.DEBUG:
    logger.remove()
    logger.add(sys.stdout, level="INFO")

app.include_router(auth_router)
app.include_router(metric_router)
app.include_router(card_router)
app.include_router(vacancy_router)
app.include_router(personality_model_router)
