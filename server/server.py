#!/usr/bin/env python3
"""Server

Script runs 2 servers, SSL server for ESP8266 and
HTTP server.

Author:
    Ondrej Kurak
"""
import sys
from multiprocessing import Process
from loader import Loader
from http_server import run_http_server
from ssl_server import run_ssl_server


ld = Loader()
ld.load_known()

http_p = Process(target=run_http_server)
ssl_p = Process(target=run_ssl_server, args=(ld.known,))

http_p.start()
ssl_p.start()

for line in sys.stdin:
    ld.proc_line(line)

http_p.terminate()
ssl_p.terminate()
