from fastapi import FastAPI
from .routers import router

app = FastAPI()

# Include routers
app.include_router(router)
