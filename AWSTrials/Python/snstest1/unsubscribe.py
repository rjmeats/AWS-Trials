# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns.html

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
	subscription_arn = 'arn:aws:sns:eu-west-2:686915945833:test_topic2:3fe5dcc6-a1da-4f05-8b8e-e1fe57622aa9'
	unsubscribe(subscription_arn)
	print()
	lt.list_topics()
