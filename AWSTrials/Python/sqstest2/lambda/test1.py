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
	
def get_lambda_context_vars(c) :
	d = {}
	if type(c) != int :
		d['remaining_time_ms'] = c.get_remaining_time_in_millis()
		d['function_name'] = c.function_name
		d['function_version'] = c.function_version
		d['invoked_function_arn'] = c.invoked_function_arn
		d['memory_limit_in_mb'] = c.memory_limit_in_mb
		d['aws_request_id'] = c.aws_request_id
		d['log_group_name'] = c.log_group_name
		d['log_stream_name'] = c.log_stream_name
		d['cognito_identity_id'] = c.identity.cognito_identity_id
		d['cognito_identity_pool_id'] = c.identity.cognito_identity_pool_id
		# Stuff which is only available when invoked via Mobile ?
		# d['client_installation_id'] = c.client_context.client.installation_id 
	return d

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
	# Variables defined with the Lambda itself
	add_env_var(d, "MYVAR1")
	add_env_var(d, "MYVAR2")
	
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
				bodytext = ""
				trigger=""

				if k == "Records" :
					event_detail = event_detail + " len:" + str(len(v))
					if len(v) > 0 :
						msg0 = v[0]
						if 'body' in msg0 :
							bodytext = msg0['body']
						if 'eventSourceARN' in msg0 :
							trigger = msg0['eventSourceARN']
							
				event_detail = event_detail + " body:" + bodytext + " trigger:" + trigger

	else :
		event_length = -1

	context_vars = get_lambda_context_vars(context)

	# Info about the AWS session from SDK
	session = boto3.Session()
	region = session.region_name
	cred = session.get_credentials()
	if cred.token == None:
		token = "-"
	else :
		token = cred.token

	# return ignored, so print out instead, to be captured in CloudWatch log
	summary = {
		'lambdaname' : 'PythonSQS', 
		'python_version' : python_version,
		'sys_path' : sys_path,
		'sys_platform' : sys_platform,
		'region': region,
		'access_key': cred.access_key,
		'secret_key': cred.secret_key,
		'token': token,
		'method': cred.method,
		'known_env_vars': env_vars,
		'context_vars': context_vars,
		'botocore_version' : botocore_version,
		'boto3_version' : boto3_version,
		'event_type' : event_type,
		'event_length' : event_length,
		'event_detail' : event_detail
	}

	print(summary)

if __name__ == "__main__" :
	#print("Running as main")
	#ret = lambda_handler([0,1,2,3,5], 0)
	ret = lambda_handler({"a":1,"b":2, "c" : []}, 0)
	#ret = lambda_handler(10.34, 0)
	print(ret)

