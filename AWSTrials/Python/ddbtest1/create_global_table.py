# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html
# https://boto3.amazonaws.com/v1/documentation/api/latest/guide/dynamodb.html

import time
import boto3
import table_info as ti

ddb_eu_1 = boto3.resource('dynamodb', region_name='eu-west-1')
ddb_eu_2 = boto3.resource('dynamodb', region_name='eu-west-2')

def create_global_table(tablename) :
	print("Creating new table called:", tablename)

	for rno in [1,2] :
		region_resource = ddb_eu_1 if rno == 1 else ddb_eu_2

		if ti.table_exists_in_region(region_resource, tablename) :
			print("Table already exists in region", rno)

		else :
			print("Creating local table in region", rno)
			t1 = region_resource.create_table(
				TableName = tablename,
				AttributeDefinitions = [
					{ 'AttributeName' : 'kcol', 'AttributeType' : 'S'}
				],
				KeySchema = [
					{ 'AttributeName' : 'kcol', 'KeyType' : 'HASH'}
				],
				StreamSpecification={
					'StreamEnabled' : True,
					'StreamViewType' : 'NEW_AND_OLD_IMAGES'
				},
				BillingMode = 'PAY_PER_REQUEST'		# Default is 'PROVISIIONED, must then specify Read and Write Capacity Units
			)
			print(t1)
			print(t1.attribute_definitions)

			print('Waiting for table to exist...')
			t1.meta.client.get_waiter('table_exists').wait(TableName=tablename)
			print('... finished waiting')

	# Now create global table in the two regions, from the two separate empty tables

	print("Creating global table")
	tgresponse = ddb_eu_2.meta.client.create_global_table(
		GlobalTableName = tablename,
		ReplicationGroup = [ { 'RegionName' : 'eu-west-1' }, { 'RegionName' : 'eu-west-2' } ]
	)

	print("Created global table", tablename)
	print(tgresponse)

if __name__ == "__main__" :
	print(ddb_eu_1)
	print(ddb_eu_2)
	test_session = boto3.session.Session()
	print()
	create_global_table('ddb_global_test_table1')
	print()
