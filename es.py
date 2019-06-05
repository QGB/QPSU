#coding=utf-8   #only for python3
import elasticsearch
import elasticsearch.helpers
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import ConnectionTimeout

from . import py # 如果在 ipy 中执行 %edit es，会导入 <ApiModule 'py' >
U=py.importU()
T=U.T

import sys

# es=Elasticsearch([b'\x88\xa3\xa3\x97zaa\xf1\xf4\xf9K\xf1\xf2\xf9K\xf5\xf4K\xf6\xf2z\xf9\xf2\xf0\xf0'.decode('cp424')]) # sg
es=Elasticsearch([  b'\x88\xa3\xa3\x97zaa\xf5\xf8K\xf2\xf0K\xf1\xf3\xf7K\xf4\xf3z\xf9\xf2\xf0\xf0'.decode('cp424')]) # 58...43


#TODO: git sync tools  ,save config to github | config level module,current python env(sys),current system(test file),global(github)
gsIndex=''
def setIndex(indexName):
	'''#始终加载在此进程中第一次设置（或手动 sys.gsIndex=''）
	'''
	if not py.istr(indexName):raise py.ArgumentError('must str')
	import sys
	if not getattr(sys,'gsIndex',''):
		sys.gsIndex=indexName
	if getattr(sys,'gsIndex',''):
		globals()['gsIndex']=sys.gsIndex
setIndex(b'\x94\x89\x86\x85\x95\x87m\xa2\x85\x81\x99\x83\x88'.decode('cp424') ) # mf_s
		
		
gsDocType='_doc'


def setLog(on=True):
	import logging
	es_log=logging.getLogger('elasticsearch')
	if on:
		es_log.setLevel(logging.NOTSET) #0
	else:
		es_log.setLevel(logging.CRITICAL) #50
log=setLog
# log(False)


def setResultWindow(size=654321,index=gsIndex):
	return es.indices.put_settings(index=index,body={ "index" : { "max_result_window" : size}}   ) 

def getTopWords(text, n=11):
	# from qgb import U, es
	U=py.importU()
	ws = {}
	for i in analyze(text)['tokens']:
		if i['type'] != 'CN_WORD':
			continue
		w = i['token']
		if w in ws:
			ws[w] += 1
		else:
			ws[w] = 1
	ws = U.getDict(ws, len(ws))
	ws = U.sort(ws, 1, reverse=True)
	for i, v in enumerate(ws):
		if v[1] == 1:
			break
	ws = ws[:i] + U.sort(ws[i:], key=lambda i: 0 - len(i[0]))
	return ws[:n]                                      
	
# @U.retry(ConnectionTimeout)
def getAll(index=gsIndex,*range):
	''' 
TransportError: TransportError(500, 'search_phase_execution_exception', 'Result window is too large, from + size must be less than or equal to: [10000] but was [20000]. See the scroll api for a more efficient way to request large data sets. This limit can be set by changing the [index.max_result_window] index level setting.')

'''
	
	return es.search(index,body={"query": {"match_all": {}},'from':0,'size':count(index)+1 }  )['hits']['hits']

@U.retry(ConnectionTimeout)	
def simpleQuery(a,fields=["title"],index=gsIndex):
	'''  a='长沙 + 的 '
	'''
	return es.search(index=index,body={
		"query": {
		 "simple_query_string" : {
			 "query": a,
			 "fields": fields,
			 "default_operator": "and"
		 }
		}
	} )

		
@U.retry(ConnectionTimeout)
def index(**kw):
	return es.index(**kw)
	
@U.retry(ConnectionTimeout)
def analyze(text,analyzer='ik_smart'):
	return es.indices.analyze(body={'text':text,'analyzer':analyzer})
	
@U.retry(ConnectionTimeout)
def count(index=gsIndex):
	return es.count(index=index)['count']
	
@U.retry(ConnectionTimeout)	
def getAllIndicesCount(_shards=False):
	r=[]
	for i in es.indices.get_mapping():
		c=es.count(index=i) 
		if not _shards:c.pop('_shards')
		r.append( [i,c] )     
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
	# connections.create_connection(hosts=['58.20.137.43'])#default 9200
	connections._conns['default']=globals()['es']
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
		class Meta: 
			index = indexName
			doc_type = "_doc"	
		
		
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
	'''body= {
  # "mifeng_search" : {
    # "aliases" : { },
    # "mappings" : {
      # "_doc" : {
		### 根据原始PUT 请求 从这里开始才对
        "properties" : { 
          "channel" : {
            "type" : "keyword"
          },
          "column_classify" : {
            "type" : "keyword"
          },
          "content" : {
            "type" : "text",
            "analyzer" : "ik_smart"
          },
          "datetime" : {
            "type" : "date"
          },
          "description" : {
            "type" : "text",
            "analyzer" : "ik_smart"
          },
          "err" : {
            "type" : "binary"
          },
          "source" : {
            "type" : "keyword"
          },
          "title" : {
            "type" : "text",
            "analyzer" : "ik_smart"
          },
          "url" : {
            "type" : "keyword"
          }
        }
      # }
    # },
    # "settings" : {
      # "index" : {
	    # 'max_result_window':"654321",
        # "creation_date" : "1557847177882",
        # "number_of_shards" : "5",
        # "number_of_replicas" : "1",
        # "uuid" : "i_b8CQ5ARw2Hpw3q0yFBGQ",
        # "version" : {
          # "created" : "6050099"
        # },
        # "provided_name" : "mifeng_search"
      # }
    # }
  # }
# }

	return es.indices.create(index=indexName,body=body)
'''
	
	from elasticsearch_dsl import DocType, Date, Completion, Keyword, Text, Integer,Binary
	from elasticsearch_dsl.analysis import CustomAnalyzer as _CustomAnalyzer
	from elasticsearch_dsl.connections import connections
	# connections.create_connection(hosts=['58.20.137.43'])
	connections._conns['default']=globals()['es']
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
		main= Text(analyzer="ik_smart")
		class Meta: 
			index = indexName
			doc_type = "_doc"	
		
		
	Type.init(index=indexName)# 不加这个 出现 KeyError: '*'
	
	
def insertMulti_mifeng(data):
	import elasticsearch
	actions=[]
	for i in data:
		source={}
		source['url']='http://'+i[0]
		source['title']=i[1] or ( i[0]+i[2][:11] )
		source['content']=i[2]
		source['channel']=i[3]
		source['column_classify']='网站'
		source['datetime']=U.time()
		actions.append(
				{
					'_id':i[0],
					'_op_type': 'index',
					'_index': "mifeng_search",  
					'_type': "_doc",
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

class StrV:
	def __init__():
		pass