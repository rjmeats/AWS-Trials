# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sqs.html

import boto3
import list_queues as lq

sqs = boto3.resource('sqs')

def read_messages(qname) :

	q = sqs.get_queue_by_name(QueueName=qname)
	
	wts = 20  # 0 - 20
	print("Reading queue", qname, "with a WaitTimeSeconds of", wts, "...")

	keepReading = True
	readCount = 0
	while keepReading :
		msgs = q.receive_messages(AttributeNames=['all'], MaxNumberOfMessages=10, WaitTimeSeconds=wts)
		print()
		print("Read", len(msgs), "messages from queue")
		for msg in msgs:
			print(msg.body)
			if readCount != 100 :
				msg.delete()
			else :
				print("*** Not deleting msg:", msg.body)
			readCount += 1
		if len(msgs) == 0 :
			keepReading = False

	print()
	print("Read", readCount, "messages")
	return

if __name__ == "__main__" :
	print(sqs)

	qname = 'test_std_q1'
	#qname = 'test_fifo_q1.fifo'

	if not lq.queue_exists(qname) :
		print()
		print("Queue", qname, "does not exist")
	else :
		print()
		lq.list_queues(qname)
		print()
		read_messages(qname)
		print()
		lq.list_queues(qname)
