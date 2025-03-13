from pydantic import BaseModel

#Pydantic schema created to validate parameters which we get from frontend
class SellerInput(BaseModel):
    seller_id: str