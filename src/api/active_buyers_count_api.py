from fastapi import APIRouter
from src.services.active_buyers_service import active_buyers_service
from src.api.api_model.response_model import ActiveBuyersResponse
from src.api.api_model.request_model import SellerInput

active_users_router = APIRouter(
    prefix = '/analysis'
)

@active_users_router.post('/active_buyers', response_model=ActiveBuyersResponse)
async def get_active_buyers_count(seller: SellerInput) -> ActiveBuyersResponse:
    total_active_buyers = await active_buyers_service.get_active_buyers(seller.seller_id)
    return ActiveBuyersResponse(active_buyers=total_active_buyers)