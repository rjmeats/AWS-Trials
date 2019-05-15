# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns.html

import time
import boto3
import list_topics as lt

sns_client = boto3.client('sns')

def publish_to_topic(topicname) :
	arn = lt.convert_topic_name_to_arn(topicname)

	if arn == "" :
		print("Topic", topicname, "not found")
	else :
		print("Publishing to topic:", topicname, "arn =", arn)

		response = sns_client.publish(
			TopicArn = arn,
			Message = "SNS message text string",
			Subject = "SNS email subject"
		)

		print("Response:", response)

if __name__ == "__main__" :
	print(sns_client)
	print()
	publish_to_topic('test_topic_s3')
	print()
