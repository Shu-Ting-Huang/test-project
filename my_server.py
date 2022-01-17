import os
import time
import threading
import urllib.request
from urllib.parse import urlparse, parse_qs
from http.server import HTTPServer, BaseHTTPRequestHandler

external_ip = urllib.request.urlopen('https://api.ipify.org').read().decode('utf8')
deployment_port = 1234
remote_name = 'origin'

# define deployment handler
def run_deployment_handler():
    # MyHandler defines how deployment requests are handled
    class MyHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            # get path from url, expected to be "/update"
            path = urlparse(self.path).path

            # get params from url, expected be {"branch": <branch pushed to GitHub>}
            params = {k:v[0] for k,v in parse_qs(urlparse(self.path).query).items()}

            if path == '/update' and 'branch' in params.keys():
                # pull the newly update branch from GitHub
                pushed_branch = params['branch']
                checked_out_branch = os.popen('git branch --show-current').readlines()[0].strip('\n')
                os.system('git fetch ' + remote_name + ' ' + pushed_branch)
                if checked_out_branch == pushed_branch:
                    os.system('git reset --hard ' + remote_name + '/' + pushed_branch)
                else:
                    os.system('git branch --force ' + pushed_branch + ' ' + remote_name + '/' + pushed_branch)

                # send response
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(bytes('<h1>Successfully pulled branch ' + pushed_branch + ' from GitHub' + ' </h1>','utf-8'))
    
    # host deployment handler
    server = HTTPServer((external_ip, deployment_port), MyHandler)
    print('Deployment handler started on ' + external_ip + ':' + str(deployment_port))
    server.serve_forever()
    print('Deployment handler stopped')

# define deployment handler sub-thread
deployment_thread = threading.Thread(target = run_deployment_handler)

# run deployment handler sub-thread
deployment_thread.start()

# run the web hosting server
os.system("python3 manage.py runserver --insecure " + external_ip + ":80")

# wait for deployment handler sub-thread to finish
deployment_thread.join()
