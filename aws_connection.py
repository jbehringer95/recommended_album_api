import os
import boto3
import pandas as pd
import logging
from typing import Dict, List, Any

from boto3.dynamodb.conditions import Key
from dotenv import load_dotenv

class DatabaseError(Exception):
    """Custom exception for database-related errors"""
    pass

load_dotenv()

ACCESS_KEY = os.getenv('access_key')
SECRET_KEY = os.getenv('secret_key')

logger = logging.getLogger(__name__)


def pulling_dataframe(access_key: str, secret_key: str, key_name: str):
    logger.info(f"Pulling dataframe from S3: {key_name}")
    
    try:
        session = boto3.session.Session(region_name='us-east-1')
        s3_instance = boto3.client('s3',
                                 aws_access_key_id=access_key, 
                                 aws_secret_access_key=secret_key)
        
        response = s3_instance.get_object(Bucket='album-csv', Key=key_name)
        df = pd.read_csv(response['Body'], index_col=[0])
        logger.info(f"Successfully loaded dataframe with {len(df)} rows")
        return df
        
    except boto3.exceptions.BotoServerError as e:
        logger.error(f"AWS server error: {e}")
        raise DatabaseError(f"Failed to connect to AWS: {str(e)}")
    except Exception as e:
        logger.error(f"Failed to pull dataframe: {e}")
        raise DatabaseError(f"Failed to load dataframe: {str(e)}")


def populating_album_database(df, access_key, secret_key):
    # This function only runs once to populate the Database
    dynamo_db = boto3.resource('dynamodb', region_name='us-east-1',
                                aws_access_key_id = access_key,
                                aws_secret_access_key = secret_key)
    dynamo_table = dynamo_db.Table('Albums')

    with dynamo_table.batch_writer() as batch:
        for index, row in df.iterrows():
            print(index)
            content = {
                'Index': index,
                'Album_Name': row['Album'],
                'Artist': row['Artist'],
                'Genres': row['Genres'],
                'Sec_Genres': row['Secondary_Genres'],
                'Descriptors': row['Album_Descriptors']
            }
            batch.put_item(Item=content)


def query_album(index: int, access_key: str, secret_key: str) -> List[Dict[str, Any]]:
    logger.info(f"Querying album with index: {index}")
    
    try:
        dynamo_db = boto3.resource('dynamodb', region_name='us-east-1',
                                 aws_access_key_id=access_key, 
                                 aws_secret_access_key=secret_key)
        dynamo_table = dynamo_db.Table('Albums')

        response = dynamo_table.query(
            KeyConditionExpression=Key('Index').eq(index)
        )
        
        if not response['Items']:
            logger.warning(f"No album found for index {index}")
        else:
            logger.debug(f"Found {len(response['Items'])} items for index {index}")
            
        return response['Items']
        
    except boto3.exceptions.BotoServerError as e:
        logger.error(f"DynamoDB server error: {e}")
        raise DatabaseError(f"Failed to connect to DynamoDB: {str(e)}")
    except Exception as e:
        logger.error(f"Failed to query album: {e}")
        raise DatabaseError(f"Failed to query album: {str(e)}")
