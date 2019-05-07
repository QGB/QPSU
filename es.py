#coding=utf-8   #only for python3
import elasticsearch
import elasticsearch.helpers
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import ConnectionTimeout

from . import py
U=py.importU()
T=U.T

es=Elasticsearch(['http://149.129.54.62:9200'])
es=Elasticsearch(['http://58.20.137.43:9200'])
gsIndex='w'
gsDocType='doc'


def log(on=True):
	import logging
	es_log=logging.getLogger('elasticsearch')
	if on:
		es_log.setLevel(logging.NOTSET) #0
	else:
		es_log.setLevel(logging.CRITICAL) #50
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
def deleteIndex(index):#必须提供名字参数，防止误删除
	return es.indices.delete(index)
	
@U.retry(ConnectionTimeout)
def getIndexAllData(index=gsIndex):
	''' Not return  
	'_version': 2,
 'found': True '''
	dsl={
		"query" : {
			"match_all" : {}
		}
	}
	return es.search(index=index,body=dsl)
	
@U.retry(ConnectionTimeout)
def iterIndex(index=gsIndex):
	''' Not return  '''
	resp = es.search(index=gsIndex, body={"query": {"match_all": {}}})
	for row in resp["hits"]["hits"]:
		yield row
		
	
@U.retry(ConnectionTimeout)	
def insert(source,id='',**ka):
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

def hash(a):
	a=T.regexReplace(a,r'\W','')
	
	
def initIndex(indexName=gsIndex):
	from elasticsearch_dsl import DocType, Date, Completion, Keyword, Text, Integer,Binary
	from elasticsearch_dsl.analysis import CustomAnalyzer as _CustomAnalyzer
	from elasticsearch_dsl.connections import connections
	
	connections.create_connection(hosts=['58.20.137.43'])#default 9200
	
# class CustomAnalyzer(_CustomAnalyzer):
    # def get_analysis_definition(self):
        # return {}
# ik_analyzer = CustomAnalyzer("ik_max_word", filter=["lowercase"])

	class Type(DocType):
		url= Keyword()
		title = Text(analyzer="ik_smart")
		content = Text(analyzer="ik_smart")
		description = Text(analyzer="ik_smart")
		err = Binary()
		# class Meta: 
			# index = indexName
			# doc_type = "doc"	
		
		
	Type.init(index=indexName)# 不加这个 出现 KeyError: '*'
	

def insertOne(url,title='',content='',description='',err=None):
	source= locals()
	for i in source:
		v=source[i]
		if i=='err' and not py.isbytes(v) :
			source[i]=U.F.dill_dump(v)
	es=globals()['es']
	
	return es.index(index=gsIndex,doc_type=gsDocType,body=source,id=url)
	
	
	import elasticsearch
	actions=[]
	actions.append(
			{
				'_id':url,
				'_op_type': 'index',
				'_index': "w",  
				'_type': "doc",
				'_source': source
			}
		)
	if U.isLinux():
		es=elasticsearch.Elasticsearch(['http://127.0.0.1:9200'])
	else:
		es=elasticsearch.Elasticsearch(['http://58.20.137.43:9200'])
	
	
	return elasticsearch.helpers.bulk( es, actions )  
	
	return insertMutil()

def insertMulti(data):
	es=globals()['es']

	return
	U=py.importU()
	F=U.F	
def spider(threads=99,TIMEOUT = 9):
	threads=99;TIMEOUT = 9
	
	dr={}
	de={}
	ru=F.pickle_load(file='./10201')
	
	import concurrent.futures,requests
	
	def load_url(domain):
		try:
			dr[domain]=requests.get('http://'+domain,timeout=TIMEOUT)
		except Exception as e:
			de[domain]=e
	
	with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
		future_to_url = (executor.submit(load_url, url) for url in ru)
		future_to_url=U.progressbar(future_to_url)
		for future in concurrent.futures.as_completed(future_to_url):
			pr
			try:
				data = future.result()
				if data:U.log(data)
			except Exception as exc:
				U.log(exc)
	
	

	
def initIndex_mifeng(indexName='mifeng_search'):
	from elasticsearch_dsl import DocType, Date, Completion, Keyword, Text, Integer,Binary
	from elasticsearch_dsl.analysis import CustomAnalyzer as _CustomAnalyzer
	from elasticsearch_dsl.connections import connections
	connections.create_connection(hosts=['58.20.137.43'])
	
	class Type(DocType):
		column_classify= Keyword()
		channel= Keyword()#
		datetime= Date()
		source = Keyword()
		url= Keyword()
		title = Text(analyzer="ik_smart")
		content = Text(analyzer="ik_smart")
		description = Text(analyzer="ik_smart")
		err = Binary()
		# class Meta: 
			# index = indexName
			# doc_type = "doc"	
		
		
	Type.init(index=indexName)# 不加这个 出现 KeyError: '*'
	
	
def insertMulti_mifeng(data):
	import elasticsearch
	actions=[]
	for i in data:
		source={}
		source['url']=i[0]
		source['title']=i[1]
		source['content']=i[2]
		source['channel']=i[3]
		source['column_classify']='网站'
		source['datetime']=U.time()
		actions.append(
				{
					'_id':source['url'],
					'_op_type': 'index',
					'_index': "mifeng_search",  
					'_type': "doc",
					'_source': source
				}
			)
	# if U.isLinux():
		# es=elasticsearch.Elasticsearch(['http://127.0.0.1:9200'])
	# else:
	es=elasticsearch.Elasticsearch(['http://58.20.137.43:9200'])

	return elasticsearch.helpers.bulk( es, actions )  
	
def decode(b):
	try:return b.decode('gb18030')
	except:return T.detectAndDecode(b)
	
	