# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html
# https://boto3.amazonaws.com/v1/documentation/api/latest/guide/dynamodb.html

import time
import boto3
import sys

ddb = boto3.resource('dynamodb')
ddb_client = ddb.meta.client

def table_exists(tablename) :

	tlist = ddb.tables.all()
	foundTable = None

	for t in tlist :
		if t.table_name == tablename :
			foundTable = t
			break
	
	return foundTable


def show_info(tablename) :
	print("Info for table:", tablename)

	t = table_exists(tablename)
	if t == None :
		print("** Table", tablename, "does not exist in this region")
		return
	else :
		print("- table exists")
		print()

	#t = ddb.Table(tablename)
	print()
	print('Table name:', t.table_name)
	print('Table Arn:', t.table_arn)
	print('Status:', t.table_status)
	print('Creation date:', t.creation_date_time)
	print('Item count:', t.item_count, ", bytes", t.table_size_bytes)
	print('Attribute definitions:', t.attribute_definitions)
	print('Key schema:', t.key_schema)
	print('Local secondary indexes:', t.local_secondary_indexes)
	print('Global secondary indexes:', t.global_secondary_indexes)
	print('Billing mode:', t.billing_mode_summary['BillingMode'])
	print('Provisioned throughput:', t.provisioned_throughput)
	print('Restore summary:', t.restore_summary)
	print('Latest stream Arn:', t.latest_stream_arn)

	print()
	#desc = ddb_client.describe_table(TableName=tablename)
	#print(desc)

	#print(t)

if __name__ == "__main__" :
	print(ddb)
	print()
	if len(sys.argv) < 2 :
		print("*** No table name argument specified")
	else :
		test_session = boto3.session.Session()
		my_region = test_session.region_name
		print("Region is", my_region)
		print()
		tn = sys.argv[1]
		show_info(tn)
	print()
