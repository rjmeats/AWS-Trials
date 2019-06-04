# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms.html

import time
import boto3

kms_client = boto3.client('kms')

def create_cmk() :
	print("Creating new CMK master key:")
	response = kms_client.create_key(
		Description='KMS Test CMK, created in Python',
		KeyUsage = 'ENCRYPT_DECRYPT'
	)

	print(response)

if __name__ == "__main__" :
	print(kms_client)
	test_session = boto3.session.Session()
	print()
	create_cmk()
	print()
