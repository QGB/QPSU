import sys;'qgb.U' in sys.modules or sys.path.append('C:/QGB/babun/cygwin/bin/');
from qgb import U,T,N,F,py
# app.jinja_loader.searchpath.append(U.pwd())
# N.rpcServer(locals=globals(),globals=globals(),app=application,key='-')

from flask import Flask, render_template, session, request,copy_current_request_context
from flask_socketio import SocketIO, emit, join_room, leave_room,close_room, rooms, disconnect

application = Flask(__name__)
application.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(application, async_mode=None)

@application.route("/")
def index():
	return '''
<body>
    <button onClick="sendMsg()">Hit Me</button>
		
	<script src="https://cdn.jsdelivr.net/npm/socket.io@latest/client-dist/socket.io.js"></script>
	<script>
	  const socket = io("http://192.168.43.162:8080");

	  function sendMsg() {
		socket.emit("message", "HELLO WORLD");
	  }
	</script>	
</body>
'''	

@socketio.on('message')
def print_message(*a,**ka):
	## When we receive a new event of type
	## 'message' through a socket.io connection
	## we print the socket ID and the message
	print(request.sid,"len:%s "%U.len(a,ka) ,a,ka)
	emit('r', {'data': 'qgb print', 'count': 0})
	print('='*88)


@socketio.event
def connect():
	emit('my_response', {'data': 'Connected',})
	
if __name__ == '__main__':
	from gevent.pywsgi import WSGIServer
	http_server = WSGIServer(('0.0.0.0', 1122), application)
	http_server.serve_forever()	


def background_thread():
	"""Example of how to send server generated events to clients."""
	count = 0
	while True:
		socketio.sleep(10)
		count += 1
		socketio.emit('my_response',
					  {'data': 'Server generated event', 'count': count})


@socketio.event
def connect():
	global thread
	with thread_lock:
		if thread is None:
			thread = socketio.start_background_task(background_thread)
	emit('my_response', {'data': 'Connected', 'count': 0})

@socketio.on('disconnect')
def test_disconnect():
	print('Client disconnected', request.sid)

@socketio.on('echo')
def echo(msg):
	emit('r',msg)
	print("msg:" ,U.execResult(msg,locals=locals(),globals=globals()) )
	
@socketio.on('message')
def print_message(*a,**ka):
	## When we receive a new event of type
	## 'message' through a socket.io connection
	## we print the socket ID and the message
	print(request.sid,"len:%s "%U.len(a,ka) ,a,ka)
	emit('r', {'data': 'qgb print', 'count': 0})
	print('='*88)
	
if __name__ == '__main__':
	# socketio.run(app,host='192.168.43.162',port=8080)
	application=app
	from gevent.pywsgi import WSGIServer
	http_server = WSGIServer(('0.0.0.0', 8080), application)
	http_server.serve_forever()