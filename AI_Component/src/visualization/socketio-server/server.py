#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# NOTE: see versions compatibility here: 
# https://python-socketio.readthedocs.io/en/latest/intro.html#version-compatibility
# current versions:
#   python-socketio == 4.0.0
#   python-engineio == 3.2.0

import time
import eventlet
import socketio

eventlet.monkey_patch()

mgr = socketio.KombuManager("amqp://")

sio = socketio.Server(cors_allowed_origins="*", client_manager=mgr)
app = socketio.WSGIApp(sio, static_files={
    '/': {'content_type': 'text/html', 'filename': 'index.html'}
})

@sio.on("connect")
def connect(sid, environ):
    print('connect ', sid)

@sio.on("my message")
def my_message(sid, data):
    print('message ', data)

@sio.on("disconnect")
def disconnect(sid):
    print('disconnect ', sid)

if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('', 9081)), app)
