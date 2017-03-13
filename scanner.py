import unirest
import time
from Queue import Queue
import random, string
from threading import Thread, activeCount

#generates random words with a given length
def randomword(length):
	return ''.join(random.choice(string.lowercase) for i in range(length))
	
#generates a random number and converts it to a string	
def randomnum():
	return str(random.randint(1,5))

# get headers from urls in an input queue and stores them on an output queue
def get_header(url, OutQueue1):
	#sets unirest timeout to 10 seconds
	unirest.timeout(10)
	#sets headers
	headers = {"Accept": "application/json"}
	#gets url from Queue
	SingleUrl = url.get()
	# call get service with headers and params and store result
	result = unirest.get(SingleUrl, headers = headers)
	#put results in the output queue
	OutQueue1.put(result.headers)
	#signals task done
	url.task_done()
	

#function to generate test queues full of urls using httpbin to generate delayed responses
def enqueue(list):
	#create queue
	q = Queue()
	#fill queue with 100 urls from httpbin
	for row in range(0, 1000):
		#put generated urls in url queue
		q.put('https://httpbin.org/get?test='+randomnum())
	#returns url queue
	return q
	
#function that executes a threaded scan receives an input queue of urls and the max threads to use
def scann(UrlQueue,num_threads):
	OutQueue1 = Queue()
	while not UrlQueue.empty():
		while  activeCount() < num_threads:
			worker = Thread(target=get_header, args=(UrlQueue,OutQueue1))
			worker.start()
	UrlQueue.join()
	return OutQueue1

#measuring time for performance metrics
start_time = time.time()	

#generate queue full of urls
UrlQueue = enqueue(1)


print 'hey'
#set maximum number of simultaneous queues
num_threads = 10

OutQueue = scann(UrlQueue,num_threads)
for elem in list(OutQueue.queue):
	print elem
print 'fin'
print str(time.time() - start_time)
