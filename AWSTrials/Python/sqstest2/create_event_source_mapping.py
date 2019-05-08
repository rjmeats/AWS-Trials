# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sqs.html

import boto3
import botocore

lambda_client = boto3.client('lambda')

def create_mapping(qname, lname) :
	print("Creating mapping between", qname, "and", lname)

	response = lambda_client.create_event_source_mapping(
		EventSourceArn='arn:aws:sqs:eu-west-2:686915945833:' + qname,
		FunctionName=lname,
		Enabled=True,
		BatchSize=10
	)
	
	print(response)

if __name__ == "__main__" :
	print(lambda_client)
	print()
	qname = 'test_lambda_sqs'
	lname = 'testPythonSQS'
	create_mapping(qname, lname)
	print()
