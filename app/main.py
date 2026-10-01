from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.user import router as user_router
from app.routers.todo import router as todo_router
from app.routers import auth as auth_router


app = FastAPI(
    title="Todos Service API",
    description="Backend API for managing users and their todos",
    version="1.0.0",
)



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(user_router)
app.include_router(todo_router)
app.include_router(auth_router.router)



@app.get(
    "/",
    tags=["Health"],
    summary="Root endpoint",
)
def root():
    return {
        "message": "Todos Services Backend is running"
    }


@app.get(
    "/health",
    tags=["Health"],
    summary="Health check",
)
def health_check():
    return {
        "status": "healthy",
        "service": "Todos Services Backend"
    }