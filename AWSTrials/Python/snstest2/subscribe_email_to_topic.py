# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns.html

import sys
import time
import boto3
import list_topics as lt

sns_client = boto3.client('sns')

def subscribe_to_topic_for_email(topicname, address) :
	arn = lt.convert_topic_name_to_arn(topicname)

	# Check for existing subscription for this combo ?

	if arn == "" :
		print("Topic", topicname, "not found")
	else :
		print("Subscribing", address, "to topic:", topicname, "arn =", arn)

		response = sns_client.subscribe(
			TopicArn = arn,
			Protocol = 'email',
			Endpoint = address,		# No restriction on what this is, could send to anyone!
			ReturnSubscriptionArn = True
		)

		print("Response:", response)

		# NB Confirmation message is sent as an email to the address above, containing a link to click to confirm the submission (with the confirmation token a URL
		# parameter). So the confirmation process is not completed here - the subscription is in a pending state.
		# If the module is re-run with the same topic/endpoint, another email is sent, and when confirmed it looks like the original subscription is replaced.

if __name__ == "__main__" :
	print(len(sys.argv))
	if len(sys.argv) < 2 :
		print("*** No email address argument specified")
	else :
		address = sys.argv[1]
		print(sns_client)
		print()
		subscribe_to_topic_for_email('test_topic_s3', address)
		print()
