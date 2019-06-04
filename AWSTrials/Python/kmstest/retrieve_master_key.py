# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms.html
# https://boto3.amazonaws.com/v1/documentation/api/latest/guide/kms-example-encrypt-decrypt-file.html

import time
import boto3

kms_client = boto3.client('kms')

def find_cmk_by_description(descriptionStart) :
	print("Finding CMK master key starting:", descriptionStart, "...")
	response = kms_client.list_keys()

	#print("Found", len(response['Keys']), "keys")
	foundCMK = None

	for cmk in response['Keys'] :
		#print(cmk)
		arn = cmk['KeyArn']
		keyInfo = kms_client.describe_key(KeyId=arn) 
		keyDesc = keyInfo['KeyMetadata']['Description']
		if keyDesc.startswith(descriptionStart) :
			#print("Found")
			foundCMK = cmk
			break

	return foundCMK

if __name__ == "__main__" :
	print(kms_client)
	test_session = boto3.session.Session()
	print()
	cmk = find_cmk_by_description('KMS Test CMK')

	if cmk == None :
		print("... not found")
	else :
		print("... found: ", cmk)
