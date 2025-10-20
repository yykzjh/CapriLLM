from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, Response, StreamingResponse


app = FastAPI()


@app.get("/health")
async def health() -> Response:
    """Health check."""
    return Response(status_code=200)

@app.get("/")
async def index() -> JSONResponse:
    return {"message": "Hello World"}
