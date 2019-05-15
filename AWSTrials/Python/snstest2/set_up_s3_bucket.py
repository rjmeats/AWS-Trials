# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html

import sys
import time
import boto3
import botocore

import list_topics as lt

s3 = boto3.resource('s3')
s3_client = boto3.client('s3')

def set_up_bucket(bucketname, topicname) :

    bucket = s3.create_bucket(
        Bucket=bucketname,
        CreateBucketConfiguration = {
            'LocationConstraint' : 'eu-west-1'
        }
    )

    print("Created bucket ", bucketname)
    print(bucket)
    print()

    topicarn = lt.convert_topic_name_to_arn(topicname)

    print("Configuring notifications for bucket", bucketname, "topic:", topicname, "topicarn:", topicarn)

    notification_config_dict = {
        'TopicConfigurations' : [
            {
                'Id' : 'S3_SNS_topic_config',
                'TopicArn' : topicarn,
                'Events' : [ 's3:ObjectCreated:*', 's3:ObjectRemoved:*']
            }
        ]
    }

    response = s3_client.put_bucket_notification_configuration(
        Bucket = bucketname,
        NotificationConfiguration = notification_config_dict
    )

    print(response)

if __name__ == "__main__" :
	#print(len(sys.argv))
	if len(sys.argv) < 2 :
		print("*** No bucket name argument specified")
	else :
		bucketname = sys.argv[1]
		print(s3)
		print()
		set_up_bucket(bucketname, 'test_topic_s3')
		print()

