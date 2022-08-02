#coding=utf-8
import logging
# import tornado.web,tornado.wsgi,tornado.ioloop
from tornado import ioloop,web,wsgi
import tornado

import sys,pathlib				 # .py/test  /qgb   / 
gsqp=pathlib.Path(__file__).absolute().parent.parent.parent.absolute().__str__()
if gsqp not in sys.path:sys.path.append(gsqp)#py3 works
from qgb import py
U,T,N,F=py.importUTNF()

# from flask import app # AttributeError: module 'flask.app' has no attribute 'errorhandler' 'route'
from flask import Flask
app=Flask(__name__)

@app.errorhandler(404)
def mirror_cache(*a,**ka):
	return '404\n'+U.stime()
N.rpcServer(locals=globals(),globals=globals(),app=app,key='-',)


class MainHandler(tornado.web.RequestHandler):
	def get(self):
		self.write("This message comes from Tornado ^_^")

class Application_qgb(tornado.web.Application):
    is_closing = False

    def signal_handler(self, signum, frame):
        logging.info('exiting...')
        self.is_closing = True

    def try_exit(self):
        if self.is_closing:
            # clean up here
            tornado.ioloop.IOLoop.instance().stop()
            logging.info('exit success')

tr = tornado.wsgi.WSGIContainer(app)

application = Application_qgb([
(r"/tornado", MainHandler),
(r".*", tornado.web.FallbackHandler, dict(fallback=tr)),
])

if __name__ == "__main__":
	import signal
	signal.signal(signal.SIGINT, application.signal_handler)
	tornado.ioloop.PeriodicCallback(application.try_exit, 100).start()

	application.listen(8000)
	tornado.ioloop.IOLoop.instance().start()