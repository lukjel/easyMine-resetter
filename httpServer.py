from systemInfo import getSystemInfo
from http.server import BaseHTTPRequestHandler, HTTPServer
from apiRequests import commandRegister

class RESTHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        print('Get call received')
        self.send_response(200)
        self.send_header('Content-type', 'image/jpeg')
        self.end_headers()
        if '/register' in self.path:
            tmp = self.path[10:]
            token = tmp.split('=')[1]
            print('Register with token: ' + token)
            commandRegister(token)

def startServer():
    sysInfo = getSystemInfo()
    http = HTTPServer((sysInfo.network.ip_local, 28080), RESTHandler)
    print('Server ready to start')
    http.serve_forever()
    print('Server started')
