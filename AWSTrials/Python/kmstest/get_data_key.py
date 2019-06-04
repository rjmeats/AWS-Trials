# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms.html
# https://boto3.amazonaws.com/v1/documentation/api/latest/guide/kms-example-encrypt-decrypt-file.html

import time
import boto3
import retrieve_master_key as r

kms_client = boto3.client('kms')

def getDataKey(masterKeyDescriptionStart) :

	cmk = r.find_cmk_by_description(masterKeyDescriptionStart)

	if cmk == None :
		print("... master key not found")
		return
	
	print("... found master key: ", cmk)
	dkresponse = kms_client.generate_data_key(KeyId=cmk['KeyArn'], KeySpec='AES_256')
	print(dkresponse)
	ciphertextblob = dkresponse['CiphertextBlob']
	plaintext = dkresponse['Plaintext']
	print()
	print("Ciphertext:", len(ciphertextblob), ciphertextblob)
	print("Plaintext:", len(plaintext), plaintext)
	print()
	# Would now use the data key to encrypt some data .. and save the encrypted data with the ciphertext form of the data key
	# https://docs.aws.amazon.com/encryption-sdk/latest/developer-guide/python-example-code.html
	#
	# And to get the original data back, need to decript the ciphertext form of the data key ...
	decryptResponse = kms_client.decrypt(CiphertextBlob=ciphertextblob)
	print("Decrypted ciphertext:", decryptResponse['Plaintext'])
	# And then use this to decrypt the actual data
	# https://docs.aws.amazon.com/encryption-sdk/latest/developer-guide/python-example-code.html

	return 

if __name__ == "__main__" :
	print(kms_client)
	test_session = boto3.session.Session()
	print()
	getDataKey('KMS Test CMK')
