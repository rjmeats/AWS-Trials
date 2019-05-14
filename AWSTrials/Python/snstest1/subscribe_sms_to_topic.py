# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns.html

import sys
import time
import boto3
import list_topics as lt

sns_client = boto3.client('sns')

def subscribe_to_topic_for_sms(topicname, phone_number) :

	# NB sms only supported in certain regions. https://docs.aws.amazon.com/sns/latest/dg/sms_supported-countries.html
	# Only Ireland (eu-west-1) for Europe! Throws an 'Invalid Parameter' error for London region. Can set region in a number of ways:
	# - via a setting in ~/.aws/config
	# - using the AWS_DEFAULT_REGION environment variable
	# - in Python code, pass a region_name='xxxx' parameter to boto3.client or boto3.resource 
	# - in Python code, call boto3.setup_default_session(region_name='xxxxxx') before other boto3 calls

	test_session = boto3.session.Session()
	my_region = test_session.region_name
	allowed_region = 'eu-west-1' 
	if my_region != allowed_region :
		print("*** Region is", my_region, "but this module expects the region to be", allowed_region)
		return	

	arn = lt.convert_topic_name_to_arn(topicname)

	# Check for existing subscription for this combo ?

	if arn == "" :
		print("Topic", topicname, "not found")
	else :
		print("Subscribing", phone_number, "to topic:", topicname, "arn =", arn)

		response = sns_client.subscribe(
			TopicArn = arn,
			Protocol = 'sms',
			Endpoint = phone_number,		# No restriction on what this is, could send to anyone!
			ReturnSubscriptionArn = True
		)

		print("Response:", response)

		# NB FOr SMS (unlike email) there is no confirmation workflow - the subscription immediately enters the 'confirmed' state without any sort of
		# notification to the phone number. Can the use 'publish' to the topic causing an SMS message to be sent to the phone number.

if __name__ == "__main__" :
	print(len(sys.argv))
	if len(sys.argv) < 2 :
		print("*** No phone number argument specified")
	else :
		phone_number = sys.argv[1]	# Should be E.164 formatted, e.g. for UK  "+44" + number-without-initial-0.  
		print(sns_client)
		print()
		subscribe_to_topic_for_sms('test_topic2', phone_number)
		print()
