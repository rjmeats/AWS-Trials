# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html
# https://boto3.amazonaws.com/v1/documentation/api/latest/guide/dynamodb.html

import time
import boto3
import sys
import table_info as ti

ddb = boto3.resource('dynamodb')
ddb_client = ddb.meta.client

def delete_items(tablename) :

    t = ti.table_exists(tablename)
    if t == None :
        print("** Table", tablename, "does not exist in this region")
        return

    count = 0
    for keyval in [ "keyval1", "keyval2", "keyval3" ] :

        # Add records, specifying the key column and two non-key columns
        print("Deleting record", keyval, "...")
        keysDict = { 
                    'kcol' : keyval
        } 

        response = ddb_client.delete_item(            
            TableName = tablename,
            Key = keysDict
        )

        count += 1 
        print(response)

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
		delete_items(tn)
	print()
