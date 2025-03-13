import boto3
from botocore.exceptions import ClientError

#Initialize connection with DynamoDB
dynamodb = boto3.client('dynamodb', endpoint_url='http://localhost:8000', region_name='us-west-2')
