import json
import boto3

def lambda_handler(event, context):

	s3 = boto3.resource('s3')
	b = ''
	for bucket in s3.buckets.all() :
		b = b + ',' + bucket.name

	session = boto3.Session()

	cred = session.get_credentials()
	if cred.token == None:
		token = "-"
	else :
		token = cred.token

	# get_user() with no parameters fails when called within a Lambda environment
	# user = boto3.client('iam').get_user()

	region = session.region_name

	return {
		'statusCode': 999,
		'body': json.dumps(b),
		'access_key': json.dumps(cred.access_key),
		'secret_key': json.dumps(cred.secret_key),
		'token': json.dumps(token),
		'method': json.dumps(cred.method),
		'region': json.dumps(region)
	}


if __name__ == "__main__" :
	print("Running as main")
	ret = lambda_handler(0, 0)
	print(ret)

