# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sqs.html

import time
import boto3
import botocore
import list_queues as lq

sqs = boto3.resource('sqs')

def delete_queue(qname) :
	print("Deleting queue called:", qname)

	# Does our queue already exist ? NB this throws an exception if a queue of this name does not exist.
	if not lq.queue_exists(qname) :
		print(".. queue does not exist")
	else :
		q = sqs.get_queue_by_name(QueueName=qname)
		q.delete()
		print(".. queue being deleted ...", end="", flush=True)
	
		# Wait for the new queue to stop being listed
		waiting = True
		while waiting :
			time.sleep(2)
			if not lq.queue_exists(qname) :
				waiting = False
				print()
			else :
				print('.', end="", flush=True)

if __name__ == "__main__" :
	print(sqs)
	print()
	qname='test_lambda_sqs'
	lq.list_queues(qname)
	print()
	delete_queue(qname)
	print()
	lq.list_queues(qname)
