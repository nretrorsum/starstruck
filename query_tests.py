import os
import boto3
import pytest
import logging
from moto import mock_aws
from src.db.queries import ActiveBuyersRepository
from src.db.connection_initialising import dynamodb
logging.basicConfig(level=logging.DEBUG)

@pytest.fixture(scope="function")
def aws_credentials():
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "us-west-2"

@pytest.fixture
def setup_dynamodb():
    """ Фікстура для створення мок-таблиці в DynamoDB """
    with mock_aws():
        dynamodb = boto3.client('dynamodb', region_name='us-west-2')
        dynamodb.create_table(
                TableName='MarketplacesBySellerCounter',
                KeySchema=[{'AttributeName': 'SellerID', 'KeyType': 'HASH'}],
                AttributeDefinitions=[
                {'AttributeName': 'SellerID', 'AttributeType': 'S'}],
                ProvisionedThroughput={'ReadCapacityUnits': 1, 'WriteCapacityUnits': 1}
                )
        
        dynamodb = boto3.client('dynamodb', region_name='us-west-2')
        dynamodb.create_table(
            TableName='MarketplacesFull',
            KeySchema=[{'AttributeName':'MpId', 'KeyType':'HASH'}],
            AttributeDefinitions=[
                {'AttributeName':'MpId', 'AttributeType':'S'}
            ],
            ProvisionedThroughput={'ReadCapacityUnits':1, 'WriteCapacityUnits': 1}
        )
        
        dynamodb.put_item(
            TableName='MarketplacesBySellerCounter',
            Item={
                'SellerID': {'S': 'seller_123'},
                'MarketplacesCounterCount': {'N': '2'},
                'MpIdList': {'L': [
                    {'S': 'e86cb2f989S944a2b3086af621cf2'},
                    {'S': 'b1234f989S944a2b3086af621cf3'}
                ]}
            }
        )
        
        dynamodb.put_item(
            TableName='MarketplacesFull',
            Item={
                'MpId': {'S': 'e86cb2f989S944a2b3086af621cf2'},
                'MpActive': {'S':'True'},
                'MpDevPortalUrl': {'S':'https://some-site.com'},
                'MpFeaturedOnStarstruck': {'S': 'False'},
                'MpmActiveBuyers': {'N': '4848733'}
            }
        )

        dynamodb.put_item(
            TableName='MarketplacesFull',
            Item={
                'MpId': {'S': 'b1234f989S944a2b3086af621cf3'},
                'MpActive': {'S':'True'},
                'MpDevPortalUrl': {'S':'https://another-some-site.com'},
                'MpFeaturedOnStarstruck': {'S': 'True'},
                'MpmActiveBuyers': {'N': '452876'}
            }
        )
        yield dynamodb


@pytest.mark.asyncio
async def test_get_marketplaces_by_seller(setup_dynamodb):
    """ Тестування отримання списку маркетплейсів для продавця """
    repo = ActiveBuyersRepository(dynamodb=dynamodb)
    result = await repo.get_marketplaces_by_seller(seller_id='seller_123')
    sum_of_buyers = await repo.get_buyers_by_marketplaces(items = result)
    logging.info(f'Sum of users{sum_of_buyers}')

    assert result == ['e86cb2f989S944a2b3086af621cf2', 
                      'b1234f989S944a2b3086af621cf3', 
                      'a23c4d5e678f9b0c1234d5678e9f3c12', 
                      'f4d5b6789c0e12345a6789f0d23b4567', 
                      '9f3a6b7890d12e34b5f678f9c1b23d456', 
                      'e12a34d5f6789b0c123d45678f9b2345c', 
                      'b23f4a5679c0d123e5678b9f123a4567d', 
                      'c6b2345f9d123ab6789e0f12d3456789c', 
                      'd4c5678b9f0a1e23b5679c345d1f2345a', 
                      'a12345d6789b0f12c5678e9f34b56789c', 
                      'f12a345b6789c012d2345e6789b9d567f', 
                      'b678a1234f9d5e678b0c123456789f012'], \
        "Помилка: список маркетплейсів неправильний!"
    assert sum_of_buyers == 11498037
