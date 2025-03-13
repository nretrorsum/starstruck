from pydantic import BaseModel

#Pydantic schema created to fetch data before sending it to the frontend.
class ActiveBuyersResponse(BaseModel):
    active_buyers: int