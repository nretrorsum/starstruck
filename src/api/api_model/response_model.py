from pydantic import BaseModel

class ActiveBuyersResponse(BaseModel):
    active_buyers: int