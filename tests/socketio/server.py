from aiohttp import web
import socketio
import socket
socket._LOCALHOST='192.168.43.162'

'''
OSError: [WinError 10049] 在其上下文中，该请求的地址无效。
Exception ignored in: <function BaseEventLoop.__del__ at 0x0000015903BD75E8>
Traceback (most recent call last):
  File "C:\QGB\Anaconda3\lib\asyncio\base_events.py", line 620, in __del__
    self.close()
  File "C:\QGB\Anaconda3\lib\asyncio\selector_events.py", line 86, in close
    self._close_self_pipe()
  File "C:\QGB\Anaconda3\lib\asyncio\selector_events.py", line 93, in _close_self_pipe
    self._remove_reader(self._ssock.fileno())
AttributeError: '_WindowsSelectorEventLoop' object has no attribute '_ssock'


'''

## creates a new Async Socket IO Server
sio = socketio.AsyncServer()
## Creates a new Aiohttp Web Application
app = web.Application()
# Binds our Socket.IO server to our Web App
## instance
sio.attach(app)

## we can define aiohttp endpoints just as we normally
## would with no change
async def index(request):
	with open('index.html') as f:
		return web.Response(text=f.read(), content_type='text/html')

## If we wanted to create a new websocket endpoint,
## use this decorator, passing in the name of the
## event we wish to listen out for
@sio.on('message')
async def print_message(sid, message):
	## When we receive a new event of type
	## 'message' through a socket.io connection
	## we print the socket ID and the message
	print("Socket ID: " , sid)
	print(message)

## We bind our aiohttp endpoint to our app
## router
app.router.add_get('/', index)

## We kick off our server
if __name__ == '__main__':
	web.run_app(app)