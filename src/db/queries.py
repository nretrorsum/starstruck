from src.db.connection_initialising import dynamodb
from src.db.abstract_repository import AbstractActiveBuyersRepository
from fastapi import HTTPException
import logging

logging.basicConfig()

class ActiveBuyersRepository(AbstractActiveBuyersRepository):
    def __init__(self, dynamodb):
        self.connection = dynamodb
    #First query to extract marketplaces ID's
    async def get_marketplaces_by_seller(self, **kwargs): 
        response = self.connection.get_item(
            TableName='MarketplacesBySellerCounter',
            Key={
                'SellerID': {'S': kwargs.get('seller_id')}
            }
        )
        if 'Item' in response:
            MpIdLists = response['Item'].get('MpIdList', {}).get('L', [])
            marketplace_id_list = [item['S'] for item in MpIdLists if 'S' in item]
            logging.info(f'Marketplaces id list:{marketplace_id_list}')
            print(f'Marketplace_id_list:{marketplace_id_list}')
            
            return marketplace_id_list
        else:
            raise HTTPException(status_code=404, detail='Seller not found')
    #Second query to extract active buyers from each marketplace
    async def get_buyers_by_marketplaces(self, items: list):
        all_items = []
        for marketplace_id in items:
            response = self.connection.query(
                TableName='MarketplacesFull',
                KeyConditionExpression='MpId = :marketplace_id',
                ExpressionAttributeValues={':marketplace_id': {'S': marketplace_id}}
            )
            data = response.get('Items', [])
            if data:
                for item in data:
                    MpActiveBuyers = item.get('MpmActiveBuyers', {}).get('N', '0')
                    IntMpActiveBuyers = int(MpActiveBuyers)
                    all_items.append(IntMpActiveBuyers)
        print(f'Sum of users:{sum(all_items)}')
        return sum(all_items)

active_buyers_repository = ActiveBuyersRepository(dynamodb)