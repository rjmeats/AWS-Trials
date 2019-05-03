import boto3
import list_queues as lq

sqs = boto3.resource('sqs')

def add_messages(qname, count) :

	q = sqs.get_queue_by_name(QueueName=qname)

	addedCount = 0
	isFifoQueue = qname.endswith(".fifo")
	for i in range(0, count) :
		msgBody = 'Test message body ' + str(i+1)

		try :
			if isFifoQueue :
				# NB Need to improve the dedup ID to allow this script to be re-run over a short period of time, otherwise repeated msgs are dropped.
				response = q.send_message(MessageBody=msgBody, MessageDeduplicationId="X"+str(i), MessageGroupId="fifogroup1")
			else :
				response = q.send_message(MessageBody=msgBody)
			addedCount += 1
			#print(response)
		except Exception as e:
			print("****")
			print(e)
			print()
			print("**** Failed to send message to queue")
			return

	print()
	print("Added", addedCount, "message" if addedCount == 1 else "messages", " to queue", qname)
	print()
	#return 
	# Read them here for trial purposes
	keepReading = True
	readCount = 0
	while keepReading :
		msgs = q.receive_messages(AttributeNames=['all'], MaxNumberOfMessages=10)
		print()
		print("Read", len(msgs), "messages from queue")
		for msg in msgs:
			print(msg.body)
			msg.delete()
			readCount += 1
		if len(msgs) == 0 :
			keepReading = False

	print()
	print("Read", readCount, "messages")
	return

if __name__ == "__main__" :
	print(sqs)

	qname = 'test_std_q1'
	qname = 'test_fifo_q1.fifo'

	if not lq.queue_exists(qname) :
		print()
		print("Queue", qname, "does not exist")
	else :
		print()
		lq.list_queues(qname)
		print()
		add_messages(qname, 100)
		print()
		lq.list_queues(qname)
