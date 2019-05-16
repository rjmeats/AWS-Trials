# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html
# https://boto3.amazonaws.com/v1/documentation/api/latest/guide/dynamodb.html

import time
import boto3

ddb = boto3.resource('dynamodb')
ddb_client = boto3.client('dynamodb')

def list_tables() :

	tlist = ddb.tables.all()

	count = 0

	for t in tlist :
		count += 1
		print(t)
		print(t.attribute_definitions)
		response = ddb_client.describe_table(TableName=t.table_name)
		print(response)

	if count > 0 :
		print()

	print(count, "tables" if count != 1 else "table")

if __name__ == "__main__" :
	print(ddb)
	print()
	test_session = boto3.session.Session()
	my_region = test_session.region_name
	print("Region is", my_region)
	print()
	list_tables()
