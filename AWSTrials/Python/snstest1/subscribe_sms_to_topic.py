# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns.html

import sys
import time
import boto3
import list_topics as lt

sns_client = boto3.client('sns')

def subscribe_to_topic_for_sms(topicname, phone_number) :
	arn = lt.convert_topic_name_to_arn(topicname)

	# Check for existing subscription for this combo ?

	if arn == "" :
		print("Topic", topicname, "not found")
	else :
		print("Subscribing", phone_number, "to topic:", topicname, "arn =", arn)

		# NB sms only supported in certain regions. https://docs.aws.amazon.com/sns/latest/dg/sms_supported-countries.html
		# Only Ireland (eu-west-1) for Europe! Throws an 'Invalid Parameter' error for London region.

		response = sns_client.subscribe(
			TopicArn = arn,
			Protocol = 'sms',
			Endpoint = phone_number,		# No restriction on what this is, could send to anyone!
			ReturnSubscriptionArn = True
		)

		print("Response:", response)

		# NB Confirmation message is sent as an email to the address above, containing a link to click to confirm the submission (with the confirmation token a URL
		# parameter). So the confirmation process is not completed here - the subscription is in a pending state.
		# If the module is re-run with the same topic/endpoint, another email is sent, and when confirmed it looks like the original subscription is replaced.

if __name__ == "__main__" :
	print(len(sys.argv))
	if len(sys.argv) < 2 :
		print("*** No phone number argument specified")
	else :
		phone_number = sys.argv[1]	# Should be E.164 formatted, e.g. for UK  "+44" + number without initial 0.  
		print(sns_client)
		print()
		subscribe_to_topic_for_sms('test_topic2', phone_number)
		print()
