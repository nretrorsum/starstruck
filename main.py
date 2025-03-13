from fastapi import FastAPI
from src.api.active_buyers_count_api import active_users_router

app = FastAPI()

app.include_router(
    active_users_router,
    tags=['Active Buyers API Endpoint']
)

