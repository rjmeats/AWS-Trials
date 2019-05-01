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

