import sys
import os
import json
import boto3
import botocore

def add_env_var(d, name) :
	if name in os.environ :
		val = os.environ[name]
	else :
		val = "-"
	d[name] = val
	
def get_lambda_env_vars() :
	d =  {}
	add_env_var(d, "_HANDLER")
	add_env_var(d, "AWS_REGION")
	add_env_var(d, "AWS_EXECUTION_ENV")
	add_env_var(d, "AWS_LAMBDA_FUNCTION_NAME")
	add_env_var(d, "AWS_LAMBDA_FUNCTION_MEMORY_SIZE")
	add_env_var(d, "AWS_LAMBDA_FUNCTION_VERSION")
	add_env_var(d, "AWS_LAMBDA_LOG_GROUP_NAME")
	add_env_var(d, "AWS_LAMBDA_LOG_STREAM_NAME")
	add_env_var(d, "AWS_ACCESS_KEY_ID")
	add_env_var(d, "AWS_SECRET_ACCESS_KEY")
	add_env_var(d, "AWS_SESSION_TOKEN")
	add_env_var(d, "LANG")
	add_env_var(d, "TZ")
	add_env_var(d, "LAMBDA_TASK_ROOT")
	add_env_var(d, "LAMBDA_RUNTIME_DIR")
	add_env_var(d, "PATH")
	add_env_var(d, "LD_LIBRARY_PATH")
	add_env_var(d, "PYTHONPATH")
	add_env_var(d, "AWS_LAMBDA_RUNTIME_API")
	
	return d

def lambda_handler(event, context):

	python_version = sys.version
	botocore_version = botocore.__version__
	boto3_version = boto3.__version__

	sys_path = sys.path
	sys_platform = sys.platform
	env_vars = get_lambda_env_vars()

	# Some info about the 'event' parameter
	event_type = str(type(event))
	event_length = 0

	event_detail = ""	
	if type(event) == int :
		event_length = 1
		event_detail = "int " + str(event)
	elif type(event) == float :
		event_length = 1
		event_detail = "float " + str(event)
	elif type(event) == str :
		event_length = len(event)	
		event_detail = "string " + event
	elif type(event) == list :
		event_length = len(event)
		event_detail = "list"
	elif type(event) == dict :
		event_length = len(event)
		event_detail = "dict: "
		for k,v in event.items() :
			if type(v) == int or type(v) == float or type(v) == str :
				event_detail = event_detail + k + "=" + str(v) + ";"
			else :
				event_detail = event_detail + k + "=" + str(type(v)) + ";"
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
		'region': region,
		'access_key': cred.access_key,
		'secret_key': cred.secret_key,
		'token': token,
		'method': cred.method,
		'known_env_vars': env_vars,
		'botocore_version' : botocore_version,
		'boto3_version' : boto3_version,
		'event_type' : event_type,
		'event_length' : event_length,
		'event_detail' : event_detail,
		's3_buckets': buckets
	}


if __name__ == "__main__" :
	#print("Running as main")
	#ret = lambda_handler([0,1,2,3,5], 0)
	ret = lambda_handler({"a":1,"b":2, "c" : []}, 0)
	#ret = lambda_handler(10.34, 0)
	print(ret)

