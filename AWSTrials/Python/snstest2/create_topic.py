# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns.html

# Info on setting up topic access policy, to allow S3 bucket to publish it
# https://stackoverflow.com/questions/49961491/using-boto3-to-send-s3-put-requests-to-sns

import time
import boto3
import json

sns = boto3.resource('sns')
sns_client = boto3.client('sns')

def create_topic(topicname) :
	print("Creating new topic called:", topicname)

	attrs = {}
	attrs['DisplayName'] = topicname

	sns_topic_policy = {
 	   "Version": "2012-10-17",
    	"Statement": [
			{
				"Effect": "Allow",
				"Principal": "*",
				"Action": "sns:Publish",
				"Resource": "arn:aws:sns:eu-west-1:686915945833:test_topic_s3",
				"Condition": {
					"ArnLike": {"AWS:SourceArn": f"arn:aws:s3:*:*:rjm-sns-bucket"},
				},
			},
		],
	}

	t = sns.create_topic(Name=topicname, Attributes=attrs)
	print()
	print("Topic created:", t)
	print(t.attributes['Policy'])

	print("Changing attributes")
	resp = sns_client.set_topic_attributes(
		TopicArn=t.arn,
		AttributeName='Policy',
		AttributeValue=json.dumps(sns_topic_policy),
	)

	print(resp)

if __name__ == "__main__" :
	print(sns)
	print()
	create_topic('test_topic_s3')
	print()
