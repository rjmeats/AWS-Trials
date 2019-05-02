import time
import boto3

sqs = boto3.resource('sqs')

def extractQueueNameFromArn(Arn) :
	return Arn.split(':')[-1]

def extractQueueNameFromUrl(Url) :
	return Url.split('/')[-1]

def list_queues() :
	qlist = sqs.queues.all()
	for q in qlist :
		a = q.attributes
		print("Queue:", q.url)
		print("- ARN:", a['QueueArn'])
		# Looks like queue name has to be extracted from the end of the URL or Arn, no separate attribute/get call
		qname = extractQueueNameFromArn(a['QueueArn'])
		print("- name:", qname)
		print("- msgs:", a['ApproximateNumberOfMessages'])
		print("- not vis msgs:", a['ApproximateNumberOfMessagesNotVisible'])
		#print("- ", a)

if __name__ == "__main__" :
	print(sqs)
	print()
	list_queues()
	print()
