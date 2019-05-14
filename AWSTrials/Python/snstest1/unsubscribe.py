# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns.html

import sys
import time
import boto3
import botocore
import list_topics as lt

sns_client = boto3.client('sns')

def unsubscribe(subscription_arn) :
	print("Unsubscribing from", subscription_arn)
	sns_client.unsubscribe(SubscriptionArn=subscription_arn)

if __name__ == "__main__" :
	print(sns_client)
	print()
	lt.list_topics()
	print()
	print(len(sys.argv))
	if len(sys.argv) < 2 :
		print("*** No subscription ARN argument specified")
	else :
		subscription_arn = sys.argv[1]
		unsubscribe(subscription_arn)
		print()
		lt.list_topics()
