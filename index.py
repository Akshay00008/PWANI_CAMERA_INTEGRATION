from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from services.service1 import router as service1

app = FastAPI()

# CORS Middleware (if needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust based on security needs
    allow_credentials=False,  # Ensure no credentials are included
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(service1, prefix="/screenshot")