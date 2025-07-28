from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from starlette.middleware.cors import CORSMiddleware
import uvicorn

import view

# FatsAPI Lifespan startup and shutdown
def lifespan(app: FastAPI):

    #("startup")

    yield

    # shutdown code

    #print("shutdown")

# FastAPI
app = FastAPI(lifespan=lifespan)

# multi routing
app.include_router(view.router)

# CORS
app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
)


########################################
# Health Check
########################################
@app.get("/api/health", response_class=PlainTextResponse)
async def health():
    return "Healthy"


########################################
# main called in console mode
########################################
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=False,
        workers=1,
        limit_concurrency=4,
        log_level="debug",
        use_colors=True,
    )
