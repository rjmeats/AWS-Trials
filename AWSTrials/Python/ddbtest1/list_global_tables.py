# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html
# https://boto3.amazonaws.com/v1/documentation/api/latest/guide/dynamodb.html

import time
import boto3

ddb = boto3.resource('dynamodb')
ddb_client = boto3.client('dynamodb')

def list_global_tables() :

	response = ddb_client.list_global_tables()
	print(response)

if __name__ == "__main__" :
	print(ddb)
	print()
	test_session = boto3.session.Session()
	my_region = test_session.region_name
	print("Region is", my_region)
	print()
	list_global_tables()
