# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html
# https://boto3.amazonaws.com/v1/documentation/api/latest/guide/dynamodb.html

import time
import boto3
import sys
import table_info as ti

ddb = boto3.resource('dynamodb')
ddb_client = ddb.meta.client

def put_items(tablename) :

    t = ti.table_exists(tablename)
    if t == None :
        print("** Table", tablename, "does not exist in this region")
        return

    count = 0
    for d in [ ("keyval1", 1, "nonkeyval1"),
                  ("keyval2", 2, "nonkeyval2"),
                  ("keyval3", 3, "nonkeyval3")  ] :
        keyval = d[0]
        nonkeyintval = d[1]
        nonkeystringval = d[2]

        # Add records, specifying the key column and two non-key columns
        # NB for Python, type seems to be inferred, so just do 
        #    'colname' : <stringvalue>
        # rather than the syntax inplied in the documentation.
        #    'colname' : { "S" : <stringvalue> }
        print("Adding record", keyval, "...")
        itemsDict = { 
                    'kcol' : keyval,
                    'nkeyint' : { "N" : nonkeyintval },
                    'nkeystring' : nonkeystringval
        } 

        # Add another non-key field to one item, don't have to have same fields in each item
        if count == 2 :
            itemsDict['anothernonkey'] = 'abc'

        try :
            response = ddb_client.put_item(            
                TableName = tablename,
                Item = itemsDict,
                ConditionExpression = 'attribute_not_exists(kcol)'      # i.e. don't replace existing item with the same key
            )
            print(response)
        except ddb_client.exceptions.ConditionalCheckFailedException as e:
            print("- duplicate key, not added")
        except Exception as e:
            print("Exception", e)

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
		put_items(tn)
	print()
