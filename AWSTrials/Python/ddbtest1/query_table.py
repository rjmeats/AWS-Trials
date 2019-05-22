# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html
# https://boto3.amazonaws.com/v1/documentation/api/latest/guide/dynamodb.html

import time
import sys

import boto3
from boto3.dynamodb.conditions import Key, Attr

import table_info as ti

ddb = boto3.resource('dynamodb')
ddb_client = ddb.meta.client

def query_item(tablename) :

    t = ti.table_exists(tablename)
    if t == None :
        print("** Table", tablename, "does not exist in this region")
        return

    tab = ddb.Table(tablename)
    queryResponse = tab.query(
        KeyConditionExpression = Key('kcol').eq('keyval1')
    )

    # Invalid - OR in key - only one condition allowed in key
    # KeyConditionExpression = Key('kcol').eq('keyval1') | Key('kcol').eq('keyval3')
    # Invalid - 'query key condition not supported'
    # KeyConditionExpression = Key('kcol').begins_with('keyval')
    print(queryResponse)
    print()
    print(len(queryResponse['Items']), "filtered item(s) found", queryResponse['ScannedCount'], "item(s) were scanned")
    count = 0
    for item in queryResponse['Items'] :
        print("Item", count)
        for k,v in item.items() :
            print("-", k, ":", v)
        count += 1

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
		query_item(tn)
	print()
