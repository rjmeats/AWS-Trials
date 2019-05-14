
# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns.html

import sys
import time
import boto3
import list_topics as lt

sns_client = boto3.client('sns')

def subscribe_to_topic_for_sqs(topicname, sqs_arn) :
	arn = lt.convert_topic_name_to_arn(topicname)

	# Check for existing subscription for this combo ?

	if arn == "" :
		print("Topic", topicname, "not found")
	else :
		print("Subscribing SQS ARN", sqs_arn, "to topic:", topicname, "arn =", arn)

		attributes = {}
		attributes['RawMessageDelivery'] = "true"
		response = sns_client.subscribe(
			TopicArn = arn,
			Protocol = 'sqs',
			Endpoint = sqs_arn,		# No restriction on what this is, could send to anyone!
			ReturnSubscriptionArn = True,
			Attributes = attributes
		)

		print("Response:", response)

		# NB No confirmation stage, automatically confirmed immediately. However, the SQS does not receive notifications published to the topic unless the 
		# appropriate policy is defined on the SQS queue to allow the SNS topic to write to it. For now, did this using the SQS console. Policy applied
		# had the following text:
		#	{
  		#		"Version": "2012-10-17",
  		#		"Id": "<sqs arn>/SQSDefaultPolicy",
  		#		"Statement": [
    	#		{
      	#			"Sid": "MySQSPolicyForSNS",
      	#			"Effect": "Allow",
      	#			"Principal": "*",
      	#			"Action": "sqs:SendMessage",
      	#			"Resource": "<sqs arn",
      	#			"Condition": {
        #				"ArnEquals": {
        #					"aws:SourceArn": "<sns arn>"
        #				}
      	#			}
    	#		}
  		#		]
		#	}
		#
		# 	'Id' field may nnot be needed, or value may be arbitrary.

if __name__ == "__main__" :
	print(len(sys.argv))
	if len(sys.argv) < 2 :
		print("*** No SQS ARN argument specified")
	else :
		sqs_arn = sys.argv[1]
		print(sns_client)
		print()
		subscribe_to_topic_for_sqs('test_topic2', sqs_arn)
		print()
