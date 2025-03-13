from src.db.queries import active_buyers_repository

class ActiveBuyersService():
    async def get_active_buyers(self, seller_id: str):
        #Here we get all ID's of marketplaces
        marketplaces = await active_buyers_repository.get_marketplaces_by_seller(seller_id = seller_id)
        #Here we get all data about marketplaces from which we must extract information about buyers 
        marketplaces_data = await active_buyers_repository.get_buyers_by_marketplaces(items = marketplaces)
        return marketplaces_data
    
active_buyers_service = ActiveBuyersService()