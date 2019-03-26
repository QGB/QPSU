import elasticsearch
import elasticsearch.helpers
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import ConnectionTimeout

def log(on=True):
	import logging
	es_log=logging.getLogger('elasticsearch')
	if on:
		es_log.setLevel(logging.NOTSET) #0
	else:
		es_log.setLevel(logging.CRITICAL) #50
		

es=Elasticsearch(['http://149.129.54.62:9200'])
# log(False)

def analyze(text,analyzer='ik_smart'):
	return es.indices.analyze(body={'text':text,'analyzer':analyzer})
	
	
def getAllIndicesCount():
	r=[]
	for i in es.indices.get_mapping():
		r.append( [i,es.count(i) ] )     
		# yield  [i,es.count(i) ] 
	return r


def deleteIndex(index):
	return es.indices.delete(index)
	
def insert(source,id=''):
	
	
	return

def retry(times, exceptions):
    """
    Retry Decorator

    Retries the wrapped function/method `times` times if the exceptions listed
    in ``exceptions`` are thrown

    :param times: The number of times to repeat the wrapped function/method
    :type times: Int
    :param Exceptions: Lists of exceptions that trigger a retry attempt
    :type Exceptions: Tuple of Exceptions
    """
    def decorator(func):
        def newfn(*args, **kwargs):
            attempt = 0
            while attempt < times:
                try:
                    return func(*args, **kwargs)
                except exceptions:
                    logger.info(
                        'Exception thrown when attempting to run %s, attempt '
                        '%d of %d' % (func, attempt, times),
                        exc_info=True
                    )
                    attempt += 1
            return func(*args, **kwargs)
        return newfn
    return decorator
