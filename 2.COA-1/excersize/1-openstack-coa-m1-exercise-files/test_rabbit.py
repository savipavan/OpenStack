#!/usr/bin/env python
import socket
from kombu import Connection
url = 'amqp://guest:guest@localhost:5672//'
with Connection(url) as c:
    try:
        c.connect()
    except socket.error:
        raise ValueError("rabbitmq server probably isn't running")
    except IOError:
        raise ValueError("bad credentials")
    else:
        print "Credentials are valid"
