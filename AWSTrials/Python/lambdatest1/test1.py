import sys
import os
import json
import boto3
import botocore

def lambda_handler(event, context):

	python_version = sys.version
	botocore_version = botocore.__version__
	boto3_version = boto3.__version__

	sys_path = sys.path
	sys_platform = sys.platform
	if "LAMBDA_TASK_ROOT" in os.environ :
		lambda_task_root = os.environ["LAMBDA_TASK_ROOT"]
	else :
		lambda_task_root = "-"

	# Some info about the 'event' parameter
	event_type = str(type(event))
	event_length = 0
		
	if type(event) == int :
		event_length = 1
	elif type(event) == float :
		event_length = 1
	elif type(event) == str :
		event_length = len(event)	
	elif type(event) == list :
		event_length = len(event)
	elif type(event) == dict :
		event_length = len(event)
	else :
		event_length = -1

	# Info about the AWS session
	session = boto3.Session()
	region = session.region_name
	cred = session.get_credentials()
	if cred.token == None:
		token = "-"
	else :
		token = cred.token

	# NB get_user() with no parameters fails when called within a Lambda environment
	# user = boto3.client('iam').get_user()

	# Invoke some S3 calls to list buckets
	s3 = boto3.resource('s3')
	buckets = ''
	for bucket in s3.buckets.all() :
		buckets = buckets + ',' + bucket.name
	buckets = buckets[1:]

	return {
		'python_version' : python_version,
		'sys_path' : sys_path,
		'sys_platform' : sys_platform,
		'lambda_task_root' : lambda_task_root,
		'botocore_version' : botocore_version,
		'boto3_version' : boto3_version,
		'event_type' : event_type,
		'event_length' : event_length,
		'region': region,
		'access_key': cred.access_key,
		'secret_key': cred.secret_key,
		'token': token,
		'method': cred.method,
		'buckets': buckets
	}


if __name__ == "__main__" :
	#print("Running as main")
	#ret = lambda_handler([0,1,2,3,5], 0)
	#ret = lambda_handler({"a":1,"b":2}, 0)
	ret = lambda_handler(10.34, 0)
	print(ret)

