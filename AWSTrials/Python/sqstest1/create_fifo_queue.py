import time
import boto3
import list_queues as lq

sqs = boto3.resource('sqs')

def create_queue(qname) :

	if not qname.endswith(".fifo") :
		print("*** Queue name must end with .fifo - no queue created")
		return

	print("Creating new fifo queue called:", qname)

	# Does our queue already exist ? NB this throws an exception if a queue of this name does not exist.
	if lq.queue_exists(qname) :
		print(".. queue already exists")
		q = sqs.get_queue_by_name(QueueName=qname)
	else :
		attrs = {}
		attrs['FifoQueue'] = "true"
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
	lq.list_queues()
	print()
	create_queue('test_fifo_q3.fifo')
	print()
	lq.list_queues()
