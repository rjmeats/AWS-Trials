# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html
# https://boto3.amazonaws.com/v1/documentation/api/latest/guide/dynamodb.html

import time
import boto3
import sys
import table_info as ti

ddb = boto3.resource('dynamodb')
ddb_client = ddb.meta.client

def get_item(tablename) :

    t = ti.table_exists(tablename)
    if t == None :
        print("** Table", tablename, "does not exist in this region")
        return

    tab = ddb.Table(tablename)

    keyval = 'keyval1'
    response = tab.get_item(
        Key= { 'kcol' : keyval }
    )

    if 'Item' in response :
        print(keyval, "found in table", tablename)
        for k,v in response['Item'].items() :
            print("-", k, ":", v)
    else :
        print(keyval, "not found in table", tablename)

    return

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
		get_item(tn)

	print()
