# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html
# https://boto3.amazonaws.com/v1/documentation/api/latest/guide/dynamodb.html

import time
import sys

import boto3
from boto3.dynamodb.conditions import Key, Attr

import table_info as ti

ddb = boto3.resource('dynamodb')
ddb_client = ddb.meta.client

def scan_items(tablename) :

    t = ti.table_exists(tablename)
    if t == None :
        print("** Table", tablename, "does not exist in this region")
        return

    response = ddb_client.scan(
        TableName = tablename
    )

    print(len(response['Items']), "item(s) found")
    count = 0
    for item in response['Items'] :
        print("Item", count)
        for k,v in item.items() :
            print("-", k, ":", v)
        count += 1

    # Do a count scan operation
    countResponse = ddb_client.scan(
        TableName = tablename,
        Select = "COUNT"
    )

    print()
    print("Count:", countResponse['Count'], "Scanned count:", countResponse['ScannedCount'])

    # Do a filtered query - using DDB low-levelclient means using FilterExpression as a string 
    # Not clear how to format these - get syntax errors.
    #filter = "nkeyint = '2'"
    #filteredResponse = ddb_client.scan(
    #    TableName = tablename,
    #    FilterExpression = filter
    #)

    # So use the DDB resource-level interface instead, which has a higher-level filtering approach, using Attr objects (see imports)
    tab = ddb.Table(tablename)
    filteredResponse = tab.scan(
        FilterExpression = Attr('nkeyint').eq(2) & Attr('nkeystring').begins_with('non')    # NB & not and
    )

    print(len(filteredResponse['Items']), "filtered item(s) found", filteredResponse['ScannedCount'], "item(s) were scanned")
    count = 0
    for item in filteredResponse['Items'] :
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
		scan_items(tn)
	print()
