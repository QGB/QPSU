#coding=utf-8
import requests,os,sys,pathlib   # .py/test  /qgb   / 
gsqp=pathlib.Path(__file__).absolute().parent.parent.parent.absolute().__str__()
if gsqp not in sys.path:sys.path.append(gsqp)#py3 works
from qgb import py
U,T,N,F=py.importUTNF()

import tantivy

def get_index():
	# Declaring our schema.
	schema_builder = tantivy.SchemaBuilder()
	schema_builder.add_text_field("title", stored=True)
	schema_builder.add_text_field("body", stored=True)
	schema_builder.add_integer_field("doc_id",stored=True)
	schema = schema_builder.build()

	# Creating our index (in memory)
	# index = tantivy.Index(schema)

	gp=F.mkdir(U.gst+'tantivy/')
	return tantivy.Index(schema, path=gp)

if __name__=='__main__':

	index=get_index()

	writer = index.writer()

	for n,f in enumerate(N.rpc_get_local('fs')):
		r=writer.add_document(tantivy.Document(
			doc_id=n,
			title=[T.sub_last(f,'\\')],
			body=[F.read(f)],
		))
		print(U.stime(),n,f)
	# ... and committing
	writer.commit()

