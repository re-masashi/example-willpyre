import willpyre
import socketio
from routes import router

app = willpyre.App(router)


sio = socketio.AsyncServer(async_mode='asgi')

@sio.event
async def connect(sid, environ, auth):
	await sio.emit('ping')
	print('connect ', sid)

@sio.event
async def pong(sid):
    print('pong ', sid)

app = socketio.ASGIApp(sio, other_asgi_app=app)
