# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns.html

import time
import boto3

sns = boto3.resource('sns')

def create_topic(topicname) :
	print("Creating new topic called:", topicname)

	attrs = {}
	attrs['DisplayName'] = topicname
	t = sns.create_topic(Name=topicname, Attributes=attrs)
	print()
	print("Topic created:", t)

if __name__ == "__main__" :
	print(sns)
	print()
	create_topic('test_topic2')
	print()
