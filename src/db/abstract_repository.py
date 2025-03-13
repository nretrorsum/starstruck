from abc import ABC

class AbstractActiveBuyersRepository(ABC):
    def __init__():
        pass
    
    async def get_marketplaces_by_seller():
        raise NotImplementedError
    
    async def get_buyers_by_marketplaces():
        raise NotImplementedError