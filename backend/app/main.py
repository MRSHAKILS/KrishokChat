from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.qa import router as qa_router
from app.api.classify import router as classify_router
from app.api.detect import router as detect_router
from app.api.benchmark import router as benchmark_router
from app.api.vision import router as vision_router
from app.core.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(
    title="KrishokChat Advisory System",
    description="Safety-aware Bengali agricultural AI assistant",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_origin],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(qa_router)
app.include_router(vision_router)
app.include_router(benchmark_router)


@app.get("/health")
async def health_check():
    return {"status": "ok", "version": "0.1.0"}
