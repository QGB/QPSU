import elasticsearch
import elasticsearch.helpers
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import ConnectionTimeout

from . import py
U=py.importU()

def log(on=True):
	import logging
	es_log=logging.getLogger('elasticsearch')
	if on:
		es_log.setLevel(logging.NOTSET) #0
	else:
		es_log.setLevel(logging.CRITICAL) #50

es=Elasticsearch(['http://149.129.54.62:9200'])
# log(False)


@U.retry(ConnectionTimeout)
def analyze(text,analyzer='ik_smart'):
	return es.indices.analyze(body={'text':text,'analyzer':analyzer})
	
@U.retry(ConnectionTimeout)	
def getAllIndicesCount():
	r=[]
	for i in es.indices.get_mapping():
		r.append( [i,es.count(i) ] )     
		# yield  [i,es.count(i) ] 
	return r

@U.retry(ConnectionTimeout)
def deleteIndex(index):
	return es.indices.delete(index)
	
@U.retry(ConnectionTimeout)	
def insert(source,id=''):
	source= {
		'column_classify': get_classify(article_origin),
		'channel': article_origin,
		#'classify': '晚间新闻',  #l爬虫监测
		'content':summary,
		'datetime': time_publish,
		#'nid': 54215,
		'source': xyqy,
		#'time': '2018-12-22',# 废弃
		'title': title,
		#'type': 'jdbc',
		'url': article_url,
	}
	
	return

