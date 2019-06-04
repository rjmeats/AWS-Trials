# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms.html

import time
import boto3

kms_client = boto3.client('kms')

def delete_cmk(keyid) :
	print("Deleting CMK master key:", keyid)
	response = kms_client.schedule_key_deletion(
		KeyId=keyid,
		PendingWindowInDays = 7
	)

	# NB Goes to pending-delete state for 7 days before true deletion.
	print(response)

if __name__ == "__main__" :
	print(kms_client)
	test_session = boto3.session.Session()
	print()
	delete_cmk('d6cf7472-fb91-4a73-ba8a-03e9ad70f735')		
	print()
