import time
import boto3

sqs = boto3.resource('sqs')

def extractQueueNameFromArn(Arn) :
	return Arn.split(':')[-1]

def extractQueueNameFromUrl(Url) :
	return Url.split('/')[-1]

def list_queues() :
	qlist = sqs.queues.all()
	count = 0

	retry = True
	while retry :
		count = 0
		retry = False
		for q in qlist :
			count += 1
			print("Queue:", q.url)
			try :
				a = q.attributes
			except :
				# If we've just deleted a queue, then it seems that it can still be listed as a queue for little while, but with
				# attributes not loadable. 
				print("*** queue attributes not found, checking listings again ***")
				print()
				retry = True
				time.sleep(2)
				continue

			print("- ARN:", a['QueueArn'])
			# Looks like queue name has to be extracted from the end of the URL or Arn, no separate attribute/get call
			qname = extractQueueNameFromArn(a['QueueArn'])
			print("- name:", qname)
			if 'FifoQueue' in a and a['FifoQueue'] == "true" :
				print("- type:", "FIFO")
			else :
				print("- type:", "Standard")
			print("- msgs:", a['ApproximateNumberOfMessages'])
			print("- msgs not visible:", a['ApproximateNumberOfMessagesNotVisible'])			
			#print("- ", a)

	if count > 0 :
		print()

	print(count, "queues" if count != 1 else "queue")

def queue_exists(qname) :
	qlist = sqs.queues.filter(QueueNamePrefix=qname)
	for q in qlist :
		if extractQueueNameFromUrl(q.url) == qname :
			return True
	return False

if __name__ == "__main__" :
	print(sqs)
	print()
	list_queues()
	print()
