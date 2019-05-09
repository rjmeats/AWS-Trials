# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns.html

import time
import boto3
import botocore
import list_topics as lt

sns_client = boto3.client('sns')

def delete_topic(topicname) :
	arn = 'arn:aws:sns:eu-west-2:686915945833:' + topicname
	print("Deleting topic called:", topicname, "using ARN:", arn)

	sns_client.delete_topic(TopicArn=arn)

if __name__ == "__main__" :
	print(sns_client)
	print()
	lt.list_topics()
	print()
	delete_topic('test_topic2')
	print()
	lt.list_topics()
