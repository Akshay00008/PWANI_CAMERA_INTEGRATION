from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from services.service1 import router as service1
from services.service2 import router as service2

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(service1, prefix="/screenshot")
app.include_router(service2)  # No prefix; serves directly at /stream/camera{id}