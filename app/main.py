from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import schemas

from .api.v1.endpoints.api import router


app = FastAPI()
app.include_router(router=router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
