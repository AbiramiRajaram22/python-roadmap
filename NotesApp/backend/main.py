from fastapi import FastAPI, Request
from app.core.config import settings
from app.database import engine
from app.routers import auth
from app.routers import auth as auth_router, user as user_router, note as note_router
from app.schemas import auth as auth_schema, user as user_schema, note as note_schema
from app.models import user, note
from fastapi.responses import JSONResponse
from app.exceptions import (
    DuplicateUserException,
    UnauthorizedAccessException,
    NoDataFoundException
)


# Create database tables
user.Base.metadata.create_all(bind=engine)
note.Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI(
    title="Notes API",
    description="A simple notes application with user management",
    version="1.0.0"
)

# Include routers
app.include_router(auth_router.router, prefix="/auth", tags=["authentication"])
app.include_router(user_router.router, prefix="/users", tags=["user"])
app.include_router(note_router.router, prefix="/notes", tags=["note"])

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@app.exception_handler(DuplicateUserException)
async def duplicate_user_handler(request: Request, exc: DuplicateUserException):
    return JSONResponse(status_code=400, content={"detail": exc.message})

@app.exception_handler(UnauthorizedAccessException)
async def unauthorized_handler(request: Request, exc: UnauthorizedAccessException):
    return JSONResponse(status_code=401, content={"detail": exc.message})

@app.exception_handler(NoDataFoundException)
async def np_data_found_handler(request: Request, exc: NoDataFoundException):
    return JSONResponse(status_code=404, content={"detail": exc.message})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app, 
        host=settings.HOST, 
        port=settings.PORT
    )


