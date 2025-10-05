from contextlib import asynccontextmanager
from lib2to3.pytree import Base  # async database connection handling

from fastapi import FastAPI

from .config import engine  # async database engine
from .interface.api.auth_routes import router as auth_router  # auth routes


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan context manager.
    """

    print("🚀 Starting auth service...")

    # Initialize resources here (e.g., database connections)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        # You can run startup SQL commands here if needed
        pass

    yield  # Application runs here

    print("👋 Shutting down...")
    await engine.dispose()


app = FastAPI(title="Auth Service", lifespan=lifespan)

# Include routers
app.include(auth_router)


@app.get("/health")
async def health():
    return {"status": "healthy"}


# ============================================================================
# RUN SERVER: python -m src.auth.main
# ============================================================================
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("auth.main:app", host="0.0.0.0", port=8000, reload=True)
# ============================================================================
