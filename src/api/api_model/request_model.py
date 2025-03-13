from pydantic import BaseModel

class SellerInput(BaseModel):
    seller_id: str