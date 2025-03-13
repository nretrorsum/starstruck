import boto3
from botocore.exceptions import ClientError

dynamodb = boto3.client('dynamodb', endpoint_url='http://localhost:8000', region_name='us-west-2')

def create_table_if_not_exists(table_name, key_schema, attribute_definitions, throughput):
    try:
        response = dynamodb.describe_table(TableName=table_name)
        print(f"Table {table_name} already exists!")
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceNotFoundException':
            print(f"Creating table {table_name}...")
            dynamodb.create_table(
                TableName=table_name,
                KeySchema=key_schema,
                AttributeDefinitions=attribute_definitions,
                ProvisionedThroughput=throughput
            )
            print(f"Table {table_name} created successfully!")
        else:
            raise e

def create_tables():
    create_table_if_not_exists(
        'MarketplacesBySellerCounter',
        [{'AttributeName': 'SellerID', 'KeyType': 'HASH'}],
        [{'AttributeName': 'SellerID', 'AttributeType': 'S'}],
        {'ReadCapacityUnits': 1, 'WriteCapacityUnits': 1}
    )

    create_table_if_not_exists(
        'MarketplacesFull',
        [{'AttributeName': 'MpId', 'KeyType': 'HASH'}],
        [{'AttributeName': 'MpId', 'AttributeType': 'S'}],
        {'ReadCapacityUnits': 1, 'WriteCapacityUnits': 1}
    )

    dynamodb.put_item(
        TableName='MarketplacesBySellerCounter',
        Item={
            'SellerID': {'S': 'seller_123'},
            'MarketplacesCounterCount': {'N': '12'},
            'MpIdList': {'L': [
                {'S': 'e86cb2f989S944a2b3086af621cf2'},
                {'S': 'b1234f989S944a2b3086af621cf3'},
                {"S": "a23c4d5e678f9b0c1234d5678e9f3c12"},
                {"S": "f4d5b6789c0e12345a6789f0d23b4567"},
                {"S": "9f3a6b7890d12e34b5f678f9c1b23d456"},
                {"S": "e12a34d5f6789b0c123d45678f9b2345c"},
                {"S": "b23f4a5679c0d123e5678b9f123a4567d"},
                {"S": "c6b2345f9d123ab6789e0f12d3456789c"},
                {"S": "d4c5678b9f0a1e23b5679c345d1f2345a"},
                {"S": "a12345d6789b0f12c5678e9f34b56789c"},
                {"S": "f12a345b6789c012d2345e6789b9d567f"},
                {"S": "b678a1234f9d5e678b0c123456789f012"}
            ]}
        }
    )

    dynamodb.put_item(
        TableName='MarketplacesBySellerCounter',
        Item={
            'SellerID': {'S': 'amazon'},
            'MarketplacesCounterCount': {'N': '2'},
            'MpIdList': {'L': [
                {'S': 'c6789a12b345d6e7890f12345a6789b0'},
                {'S': 'b45f6789a12c345d6789e01234f5678g'},
            ]}
        }
    )
    
    dynamodb.put_item(
        TableName='MarketplacesFull',
        Item={
            'MpId': {'S': 'e86cb2f989S944a2b3086af621cf2'},
            'MpActive': {'S': 'True'},
            'MpDevPortalUrl': {'S': 'https://some-site.com'},
            'MpFeaturedOnStarstruck': {'S': 'False'},
            'MpmActiveBuyers': {'N': '4848733'}
        }
    )

    dynamodb.put_item(
        TableName='MarketplacesFull',
        Item={
            'MpId': {'S': 'b1234f989S944a2b3086af621cf3'},
            'MpActive': {'S': 'True'},
            'MpDevPortalUrl': {'S': 'https://another-some-site.com'},
            'MpFeaturedOnStarstruck': {'S': 'True'},
            'MpmActiveBuyers': {'N': '452876'}
        }
    )
    dynamodb.put_item(
    TableName='MarketplacesFull',
    Item={
        'MpId': {'S': 'a23c4d5e678f9b0c1234d5678e9f3c12'},
        'MpActive': {'S': 'True'},
        'MpDevPortalUrl': {'S': 'https://some-site1.com'},
        'MpFeaturedOnStarstruck': {'S': 'False'},
        'MpmActiveBuyers': {'N': '823456'}
    }
)

    dynamodb.put_item(
        TableName='MarketplacesFull',
        Item={
            'MpId': {'S': 'f4d5b6789c0e12345a6789f0d23b4567'},
            'MpActive': {'S': 'True'},
            'MpDevPortalUrl': {'S': 'https://some-site2.com'},
            'MpFeaturedOnStarstruck': {'S': 'True'},
            'MpmActiveBuyers': {'N': '934567'}
        }
    )

    dynamodb.put_item(
        TableName='MarketplacesFull',
        Item={
            'MpId': {'S': '9f3a6b7890d12e34b5f678f9c1b23d456'},
            'MpActive': {'S': 'True'},
            'MpDevPortalUrl': {'S': 'https://some-site3.com'},
            'MpFeaturedOnStarstruck': {'S': 'True'},
            'MpmActiveBuyers': {'N': '1023456'}
        }
    )

    dynamodb.put_item(
        TableName='MarketplacesFull',
        Item={
            'MpId': {'S': 'e12a34d5f6789b0c123d45678f9b2345c'},
            'MpActive': {'S': 'False'},
            'MpDevPortalUrl': {'S': 'https://some-site4.com'},
            'MpFeaturedOnStarstruck': {'S': 'False'},
            'MpmActiveBuyers': {'N': '54321'}
        }
    )

    dynamodb.put_item(
        TableName='MarketplacesFull',
        Item={
            'MpId': {'S': 'b23f4a5679c0d123e5678b9f123a4567d'},
            'MpActive': {'S': 'True'},
            'MpDevPortalUrl': {'S': 'https://some-site5.com'},
            'MpFeaturedOnStarstruck': {'S': 'True'},
            'MpmActiveBuyers': {'N': '1122334'}
        }
    )

    dynamodb.put_item(
        TableName='MarketplacesFull',
        Item={
            'MpId': {'S': 'c6b2345f9d123ab6789e0f12d3456789c'},
            'MpActive': {'S': 'True'},
            'MpDevPortalUrl': {'S': 'https://some-site6.com'},
            'MpFeaturedOnStarstruck': {'S': 'False'},
            'MpmActiveBuyers': {'N': '876543'} 
        }
    )

    dynamodb.put_item(
        TableName='MarketplacesFull',
        Item={
            'MpId': {'S': 'd4c5678b9f0a1e23b5679c345d1f2345a'},
            'MpActive': {'S': 'True'},
            'MpDevPortalUrl': {'S': 'https://some-site7.com'},
            'MpFeaturedOnStarstruck': {'S': 'True'},
            'MpmActiveBuyers': {'N': '654321'}
        }
    )

    dynamodb.put_item(
        TableName='MarketplacesFull',
        Item={
            'MpId': {'S': 'a12345d6789b0f12c5678e9f34b56789c'},
            'MpActive': {'S': 'False'},
            'MpDevPortalUrl': {'S': 'https://some-site8.com'},
            'MpFeaturedOnStarstruck': {'S': 'True'},
            'MpmActiveBuyers': {'N': '320987'}
        }
    )

    dynamodb.put_item(
        TableName='MarketplacesFull',
        Item={
            'MpId': {'S': 'f12a345b6789c012d2345e6789b9d567f'},
            'MpActive': {'S': 'True'},
            'MpDevPortalUrl': {'S': 'https://some-site9.com'},
            'MpFeaturedOnStarstruck': {'S': 'True'},
            'MpmActiveBuyers': {'N': '231456'}
        }
    )

    dynamodb.put_item(
        TableName='MarketplacesFull',
        Item={
            'MpId': {'S': 'b678a1234f9d5e678b0c123456789f012'},
            'MpActive': {'S': 'False'},
            'MpDevPortalUrl': {'S': 'https://some-site10.com'},
            'MpFeaturedOnStarstruck': {'S': 'False'},
            'MpmActiveBuyers': {'N': '154987'}
        }
    )
    
    dynamodb.put_item(
        TableName='MarketplacesFull',
        Item={
            'MpId': {'S': 'b45f6789a12c345d6789e01234f5678g'},
            'MpActive': {'S': 'True'},
            'MpDevPortalUrl': {'S': 'https://some-site.com'},
            'MpFeaturedOnStarstruck': {'S': 'False'},
            'MpmActiveBuyers': {'N': '200'}
        }
    )
    
    dynamodb.put_item(
        TableName='MarketplacesFull',
        Item={
            'MpId': {'S': 'c6789a12b345d6e7890f12345a6789b0'},
            'MpActive': {'S': 'True'},
            'MpDevPortalUrl': {'S': 'https://some-site.com'},
            'MpFeaturedOnStarstruck': {'S': 'False'},
            'MpmActiveBuyers': {'N': '200'}
        }
    )

create_tables()
