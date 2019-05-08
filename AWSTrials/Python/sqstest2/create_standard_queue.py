# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sqs.html

import time
import boto3
import list_queues as lq

sqs = boto3.resource('sqs')

def create_queue(qname) :
	print("Creating new queue called:", qname)

	# Does our queue already exist ? NB this throws an exception if a queue of this name does not exist.
	if lq.queue_exists(qname) :
		print(".. queue already exists")
		q = sqs.get_queue_by_name(QueueName=qname)
	else :
		attrs = {}
		q = sqs.create_queue(QueueName=qname, Attributes=attrs)
		print(".. new queue being created ...", end="", flush=True)
	
		# Wait for the new queue to become listed
		waiting = True
		while waiting :
			time.sleep(2)
			if lq.queue_exists(qname) :
				waiting = False
				print()
			else :
				print('.', end="", flush=True)

	print()
	print("Queue available:", q)

if __name__ == "__main__" :
	print(sqs)
	print()
	qname='test_lambda_sqs'
	lq.list_queues(qname)
	print()
	create_queue(qname)
	print()
	lq.list_queues(qname)
