import boto3
import pandas as pd


def loadDataFromS3(bucket, name):
    client = boto3.client('s3',
                          aws_access_key_id='AKIAQ5ZMS5VM2EYR5WGS',
                          aws_secret_access_key='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',
                          region_name='us-east-2')

    # Create the S3 object
    obj = client.get_object(Bucket=bucket, Key=name)
    # Read data from the S3 object
    data = pd.read_csv(obj['Body'])
    return data