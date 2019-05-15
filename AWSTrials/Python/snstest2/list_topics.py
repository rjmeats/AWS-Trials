# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns.html

import time
import boto3

sns = boto3.resource('sns')

def convert_topic_name_to_arn(topicname) :
	tlist = sns.topics.all()
	arn = ""
	for t in tlist :
		arn = t.attributes['TopicArn']
		tname = arn.split(':')[-1]
		if tname == topicname :
			return arn

	return ""

def list_topics() :

	tlist = sns.topics.all()

	count = 0

	for t in tlist :
		count += 1
		print()
		print("Topic:", t.arn)
		a = t.attributes
		print("  ", a)

		subscriptions_list = sns.meta.client.list_subscriptions_by_topic(TopicArn=t.arn)
		#print(subscriptions_list)
		print("  ", len(subscriptions_list['Subscriptions']), " subscription(s):")
		for s in subscriptions_list['Subscriptions'] :
			print("    ", s['Protocol'], ":", s['Endpoint'], ":", s['SubscriptionArn'])

	if count > 0 :
		print()

	print(count, "topics" if count != 1 else "topic")

if __name__ == "__main__" :
	print(sns)
	print()
	test_session = boto3.session.Session()
	my_region = test_session.region_name
	print("Region is", my_region)
	print()
	list_topics()
	print()
	foundarn = convert_topic_name_to_arn("test_topic_s3")
	print("Found arn", foundarn)
