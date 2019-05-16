# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html
# https://boto3.amazonaws.com/v1/documentation/api/latest/guide/dynamodb.html

import time
import boto3

ddb_client = boto3.client('dynamodb')

def delete_table(tablename) :
	print("Deleting table called:", tablename)

	response = ddb_client.delete_table(TableName=tablename)
	print(response)

	print('Waiting for table to not exist...')
	ddb_client.get_waiter('table_not_exists').wait(TableName=tablename)
	print('... finished waiting')


if __name__ == "__main__" :
	print(ddb_client)
	print()
	delete_table('ddb_test_table1')
	print()
