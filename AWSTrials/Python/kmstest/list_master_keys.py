# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms.html
# https://boto3.amazonaws.com/v1/documentation/api/latest/guide/kms-example-encrypt-decrypt-file.html

import time
import boto3

kms_client = boto3.client('kms')

def list_master_keys() :
	print("Listing CMK master keys:")
	response = kms_client.list_keys()

	print("Found", len(response['Keys']), "keys")
	for cmk in response['Keys'] :
		print()
		arn = cmk['KeyArn']
		id = cmk['KeyId']
		keyInfo = kms_client.describe_key(KeyId=arn) 
		keyDesc = keyInfo['KeyMetadata']['Description']
		print("Arn:", arn)
		print("Id:", id)
		print("Description:", keyDesc)
		print('Creation date:', keyInfo['KeyMetadata']['CreationDate'])
		print('Enabled', keyInfo['KeyMetadata']['Enabled'])
		print('KeyUsage', keyInfo['KeyMetadata']['KeyUsage'])
		print('KeyState', keyInfo['KeyMetadata']['KeyState'])
		print('Origin', keyInfo['KeyMetadata']['Origin'])
		print('KeyManager', keyInfo['KeyMetadata']['KeyManager'])

if __name__ == "__main__" :
	print(kms_client)
	test_session = boto3.session.Session()
	my_region = test_session.region_name
	print("Region is", my_region)
	print()
	list_master_keys()
