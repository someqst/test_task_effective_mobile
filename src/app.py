import uvicorn
from fastapi import FastAPI, Request
from fastapi.exceptions import HTTPException

from handlers.user.auth import router as auth_router


app = FastAPI()


app.include_router(auth_router, prefix="/auth", tags=["authentification"])


@app.exception_handler(Exception)
async def handle_global_exception(req: Request, exc: Exception):
    print(exc)
    # logger.error(exc)
    raise HTTPException(status_code=500, detail="Internal Server Error")


if __name__ == "__main__":
    uvicorn.run(app)
