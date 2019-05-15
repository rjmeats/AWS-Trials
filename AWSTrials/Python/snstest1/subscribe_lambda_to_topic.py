# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns.html

import sys
import time
import boto3
import list_topics as lt

sns_client = boto3.client('sns')

def subscribe_to_topic_for_lambda(topicname, lambda_arn) :
	arn = lt.convert_topic_name_to_arn(topicname)

	# Check for existing subscription for this combo ?

	if arn == "" :
		print("Topic", topicname, "not found")
	else :
		print("Subscribing Lambda ARN", lambda_arn, "to topic:", topicname, "arn =", arn)

		response = sns_client.subscribe(
			TopicArn = arn,
			Protocol = 'lambda',
			Endpoint = lambda_arn,		# No restriction on what this is, could send to anyone!
			ReturnSubscriptionArn = True
		)

		print("Response:", response)

		# NB No confirmation stage, automatically confirmed immediately. 

if __name__ == "__main__" :
	print(len(sys.argv))
	if len(sys.argv) < 2 :
		print("*** No Lambda ARN argument specified")
	else :
		lambda_arn = sys.argv[1]
		print(sns_client)
		print()
		subscribe_to_topic_for_lambda('test_topic2', lambda_arn)
		print()
