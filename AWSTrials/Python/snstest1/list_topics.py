# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns.html

import time
import boto3

sns = boto3.resource('sns')

#def extractQueueNameFromArn(Arn) :
#	return Arn.split(':')[-1]

#def extractQueueNameFromUrl(Url) :
#	return Url.split('/')[-1]

def list_topics() :

	tlist = sns.topics.all()

	count = 0

	for t in tlist :
		count += 1
		print("Topic:", t.arn)
		a = t.attributes
		print("  ", a)

	if count > 0 :
		print()

	print(count, "topics" if count != 1 else "topic")

#def queue_exists(qname) :
#	qlist = sqs.queues.filter(QueueNamePrefix=qname)
#	for q in qlist :
#		if extractQueueNameFromUrl(q.url) == qname :
#			return True
#	return False

if __name__ == "__main__" :
	print(sns)
	print()
	list_topics()
	print()
