import os
import boto3
import pandas as pd

from boto3.dynamodb.conditions import Key
from dotenv import load_dotenv


load_dotenv()

ACCESS_KEY = os.getenv('access_key')
SECRET_KEY = os.getenv('secret_key')


def pulling_dataframe(access_key, secret_key):
    session = boto3.session.Session(region_name='us-east-1')
    s3_instance = boto3.client('s3',
                                 aws_access_key_id = access_key, 
                                 aws_secret_access_key = secret_key)
    
    response = s3_instance.get_object(Bucket='album-csv', 
                                      Key='Vectorizor_df.csv')

    df = pd.read_csv(response['Body'], index_col=[0])

    return df


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


def query_album(index, access_key, secret_key):
    dynamo_db = boto3.resource('dynamodb', region_name='us-east-1',
                                aws_access_key_id = access_key, 
                                aws_secret_access_key = secret_key)
    dynamo_table = dynamo_db.Table('Albums')

    response = dynamo_table.query(
        KeyConditionExpression=Key('Index').eq(index)
    )
    return response['Items']


# print(query_album(3103, ACCESS_KEY, SECRET_KEY))


    