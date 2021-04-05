"""
Creates a folder structure in S3, for testing Data Factory key nesting.

Usage:
  BUCKET_NAME=aws-bucket-name python nested-folder-generator.py

"""

import os, sys, boto3

random_json = """
REPLACE THIS STRING WITH SWAGGER PETSTORE YAML, TO RECREATE THE SAME TEST
"""

s3 = None
bucket_name = None

def get_s3_client():
    if os.getenv('LOCALSTACK_MODE') is not None and os.getenv('LOCALSTACK_MODE') == 'true':
        print('Localstack mode')
        return boto3.client('s3',
            endpoint_url="http://localhost:4566",
            use_ssl=False,
            aws_access_key_id='a',
            aws_secret_access_key='b',
            region_name='eu-west-1')
    else:
        print('AWS mode')
        return boto3.client('s3')

def create_a_directory(dir_name):
    s3.put_object(Bucket=bucket_name, Body='', Key='{}/'.format(dir_name))

def create_an_object(key_name):
    s3.put_object(Bucket=bucket_name, Body=random_json, Key=key_name)

def create_directories(count: int):
    create_a_directory('Earth')
    create_a_directory('Earth/UK')
    create_a_directory('Earth/UK/Oxfordshire')
    create_a_directory('Earth/UK/Oxfordshire/Oxford')
    create_a_directory('Earth/UK/Oxfordshire/Didcot')
    create_a_directory('Earth/UK/Nottinghamshire')
    create_a_directory('Earth/UK/Nottinghamshire/Nottingham')
    create_a_directory('Earth/UK/Nottinghamshire/Southwell')
    
    # Create the streets and house numbers
    for x in range(count):
        # Oxford
        create_a_directory('Earth/UK/Oxfordshire/Oxford/Street {}'.format(x))
        create_an_object('Earth/UK/Oxfordshire/Oxford/Street {}/{}.yaml'.format(x, x))

        # Didcot
        create_a_directory('Earth/UK/Oxfordshire/Didcot/Street {}'.format(x))
        create_an_object('Earth/UK/Oxfordshire/Didcot/Street {}/{}.yaml'.format(x, x))

        # Nottingham
        create_a_directory('Earth/UK/Nottinghamshire/Nottingham/Street {}'.format(x))
        create_an_object('Earth/UK/Nottinghamshire/Nottingham/Street {}/{}.yaml'.format(x, x))

        # Southwell
        create_a_directory('Earth/UK/Nottinghamshire/Southwell/Street {}'.format(x))
        create_an_object('Earth/UK/Nottinghamshire/Southwell/Street {}/{}.yaml'.format(x, x))


if __name__ == '__main__':
    if os.getenv('BUCKET_NAME') is None:
        sys.exit('BUCKET_NAME not set')
    bucket_name = os.getenv('BUCKET_NAME')
    
    s3 = get_s3_client()
    create_directories(1000)
