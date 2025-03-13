from abc import ABC

#Abstract repository for database operations
class AbstractActiveBuyersRepository(ABC):
    async def get_marketplaces_by_seller():
        raise NotImplementedError
    
    async def get_buyers_by_marketplaces():
        raise NotImplementedError