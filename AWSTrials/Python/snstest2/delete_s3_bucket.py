# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html

import sys
import time
import boto3
import botocore

s3 = boto3.resource('s3')

def delete_bucket(bucketname) :

    bucket = s3.Bucket(bucketname)
    print("Deleting bucket")
    bucket.delete()

if __name__ == "__main__" :
	print(len(sys.argv))
	if len(sys.argv) < 2 :
		print("*** No bucket name argument specified")
	else :
		bucketname = sys.argv[1]
		print(s3)
		print()
		delete_bucket(bucketname)
		print()

