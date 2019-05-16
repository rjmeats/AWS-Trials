# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html
# https://boto3.amazonaws.com/v1/documentation/api/latest/guide/dynamodb.html

import time
import boto3

ddb = boto3.resource('dynamodb')

def create_table(tablename) :
	print("Creating new table called:", tablename)

	# NB When creating the table, only the key fields are specified (and fields used in indexes). Non-key fields can vary
	# from item to item, and are specified as items are added/updated.
	t = ddb.create_table(
		TableName = tablename,
		AttributeDefinitions = [
			{ 'AttributeName' : 'kcol', 'AttributeType' : 'S'}
		],
		KeySchema = [
			{ 'AttributeName' : 'kcol', 'KeyType' : 'HASH'}
		],
		BillingMode = 'PAY_PER_REQUEST'		# Default is 'PROVISIIONED, must then specify Read and Write Capacity Units
	)

	print(t)
	print(t.attribute_definitions)

	print('Waiting for table to exist...')
	t.meta.client.get_waiter('table_exists').wait(TableName=tablename)
	print('... finished waiting')

if __name__ == "__main__" :
	print(ddb)
	print()
	create_table('ddb_test_table1')
	print()
