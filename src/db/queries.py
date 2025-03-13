from src.db.connection_initialising import dynamodb
from src.db.abstract_repository import AbstractActiveBuyersRepository
from fastapi import HTTPException
from botocore.exceptions import ClientError
import logging

logging.basicConfig()

class ActiveBuyersRepository(AbstractActiveBuyersRepository):
    def __init__(self, dynamodb):
        self.connection = dynamodb
    #First query to extract marketplaces ID's
    async def get_marketplaces_by_seller(self, **kwargs):
        try: 
            response = self.connection.get_item(
                TableName='MarketplacesBySellerCounter',
                Key={
                    'SellerID': {'S': kwargs.get('seller_id')}
                    }
                )
            #Handling missing seller in the database
            if 'Item' not in response:
                logging.error(f"Seller with ID '{kwargs.get('seller_id')}' not found in MarketplacesBySellerCounter table.")
                raise HTTPException(status_code=404, detail=f"Seller with ID '{kwargs.get('seller_id')}' not found.")
            
            if 'Item' in response:
                MpIdLists = response['Item'].get('MpIdList', {}).get('L', [])
                #Handling missing marketplaces related to seller
                if not MpIdLists:
                    logging.warning(f"No marketplaces found for Seller ID '{kwargs.get('seller_id')}'.")
                    raise HTTPException(status_code=404, detail=f"No marketplaces found for Seller ID '{kwargs.get('seller_id')}'.")
                
                marketplace_id_list = [item['S'] for item in MpIdLists if 'S' in item]
                logging.info(f'Marketplaces id list:{marketplace_id_list}')
                #print(f'Marketplace_id_list:{marketplace_id_list}')
                return marketplace_id_list
        except ClientError as e:
            #Handling iternal errors with DynamoDB
            logging.error(f"AWS DynamoDB ClientError: {e.response['Error']['Message']}")
            raise HTTPException(status_code=500, detail="Internal Server Error")

    async def get_buyers_by_marketplaces(self, items: list):
        try:
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
            #print(f'Sum of buyers:{sum(all_items)}')
            return sum(all_items)
        except ClientError as e:
            #Handling iternal errors with DynamoDB
            logging.warning(f'logging.error(f"AWS DynamoDB ClientError: {e.response['Error']['Message']}")')
            raise HTTPException(status_code=500, detail='Internal Server Error')

active_buyers_repository = ActiveBuyersRepository(dynamodb)