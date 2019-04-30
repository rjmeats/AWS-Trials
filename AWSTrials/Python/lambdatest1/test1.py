import json
import boto3

def lambda_handler(event, context):

	s3 = boto3.resource('s3')
	b = ''
	for bucket in s3.buckets.all() :
		b = b + ',' + bucket.name
	return {
		'statusCode': 999,
		'body': json.dumps(b)
	}


if __name__ == "__main__" :
	print("Running as main")
	ret = lambda_handler(0, 0)
	print(ret)

