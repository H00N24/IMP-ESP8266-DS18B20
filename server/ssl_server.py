"""File with SSL server

Author:
    Ondrej Kurak
"""
from datetime import datetime as dt
import json
import socket
import ssl
import re
import os


def get_date_time():
    """Actual time in string

    Returns:
        Actual date and time in list
    """
    form = "%d.%m.%Y %H:%M:%S"
    return dt.now().strftime(form).split()


def run_ssl_server(known):
    """Running SSL server

    Function runs SSL server, handles incomming messages
    and adds new entries to history files.

    Args:
        known (set): known devices
    """
    sock = socket.socket()
    sock.bind(('', 44444))
    sock.listen(10)
    main_dir = os.path.dirname(os.path.abspath(__file__))
    print("SSL server: OK")

    while True:
        new_sock, in_addr = sock.accept()
        ssl_stream = ssl.wrap_socket(new_sock,
                                     server_side=True,
                                     certfile=main_dir + "/certf/server.crt",
                                     keyfile=main_dir + "/certf/server.key")
        try:
            data = json.loads(ssl_stream.read().decode("utf-8"))
            data['DATE'], data['TIME'] = get_date_time()
            if (data['NAME'], data['MAC'], data['OVR']) not in known:
                print("Unrecognized device!", in_addr)
                continue
            regex = "<td>{0}.*{0}-->".format(data['MAC'])
            repl = ("<td>{0}</td><td>{1}</td>"
                    "<td>{2}</td><td>{3}</td><!--{0}-->").format(data['MAC'],
                                                                 data['DATE'],
                                                                 data['TIME'],
                                                                 data['TEMP'])
            with open(main_dir + '/index.html') as inp:
                text = inp.read()
            new_t = re.sub(regex, repl, text)
            with open(main_dir + '/index.html', 'w') as out:
                out.write(new_t)
            hst = '/history/{0}.html'.format(data['MAC'].replace(':', '-'))
            with open(main_dir + hst) as inp:
                text = inp.read()
            repl = ('<!--NEW ENTRY-->\n'
                    '<tr><td>{0}</td>'
                    '<td>{1}</td>'
                    '<td>{2}</td></tr>').format(data['DATE'],
                                                data['TIME'],
                                                data['TEMP'])

            new_text = re.sub('<!--NEW ENTRY-->', repl, text)
            with open(main_dir + hst, 'w') as out:
                out.write(new_text)
        finally:
            ssl_stream.shutdown(socket.SHUT_RDWR)
            ssl_stream.close()
