from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import simulations

app = FastAPI()


# configure CORS
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# routes
app.include_router(simulations.router)
