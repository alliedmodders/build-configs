# vim: set ts=8 sts=4 sw=4 tw=99 et:
import pprint
import os, sys
import re, json
import argparse
import subprocess
import hmac, hashlib
import BaseHTTPServer as base_http

TIMEOUT = 10.0
REPO_ROOT = '/hgshare'

class Server(base_http.HTTPServer):
    def __init__(self, *args, **kwargs):
        base_http.HTTPServer.__init__(self, *args, **kwargs)

    def server_bind(self):
        base_http.HTTPServer.server_bind(self)
        self.socket.settimeout(TIMEOUT)

class RequestHandler(base_http.BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        base_http.BaseHTTPRequestHandler.__init__(self, *args, **kwargs)

    def setup(self):
        base_http.BaseHTTPRequestHandler.setup(self)
        self.request.settimeout(TIMEOUT)

    def log_request(self, code = '-', size = '-'):
        with open(os.path.join(self.options.logs, 'access.log'), 'a') as fp:
            client, _ = self.client_address
            fp.write('{0} - - [{1}] "{2} {3} {4}" {5} -\n'.format(
                client,
                self.log_date_time_string(),
                self.command,
                self.path,
                self.request_version,
                code
            ))

    def log_line(self, fp, message):
        client, _ = self.client_address
        fp.write('{0} - - [{1}] "{2} {3} {4}" stdout -\n'.format(
            client,
            self.log_date_time_string(),
            self.command,
            self.path,
            self.request_version
        ))
        fp.write(message)
        fp.write('\n')

    def log_error(self, format, *args):
        output = format % args
        with open(os.path.join(self.options.logs, 'error.log'), 'a') as fp:
            self.log_line(fp, output)

    def log_message(self, format, *args):
        output = format % args
        with open(os.path.join(self.options.logs, 'access.log'), 'a') as fp:
            self.log_line(fp, output)

    def send_empty_response(self, code):
        self.send_response(code)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        algorithm, digest = self.headers['X-Hub-Signature'].split('=')
        if algorithm not in hashlib.algorithms:
            return self.send_empty_response(403)

        content = self.rfile.read(content_length)
        check = hmac.new(self.options.secret, content, getattr(hashlib, algorithm))
        if digest != check.hexdigest():
            return self.send_empty_response(403)

        obj = json.loads(content)

        try:
            _, _, branch = obj['ref'].split('/')
        except:
            return self.send_empty_response(200)

        if not re.match('^[A-Za-z0-9_-]+$', branch):
            return self.send_empty_response(400)

        if obj['repository']['name'] == 'hl2sdk':
            cwd = os.path.join(REPO_ROOT, 'hl2sdk-{0}'.format(branch))
        elif obj['repository']['name'] == 'hlsdk':
            if branch != 'master':
                return self.send_empty_response(200)
            cwd = os.path.join(REPO_ROOT, 'hlsdk')

        if not os.path.isdir(cwd):
            print(cwd)
            return self.send_empty_response(200)

        self.send_empty_response(202)

        result = subprocess.check_output(
            args = ['git', 'pull'],
            cwd = cwd
        )

        self.log_message(result)

def start(args):
    RequestHandler.options = args

    server_address = ('', args.port)
    httpd = Server(server_address, RequestHandler)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.socket.close()

def main():
    parser = argparse.ArgumentParser('Start the change listener.')
    parser.add_argument('-p', '--port', dest='port', type=int, default=10500,
                        help='Port number')
    parser.add_argument('-s', '--secret', dest='secret', type=str, default=None,
                        help='File containing secret key')
    parser.add_argument('--logs', dest='logs', type=str, default=None,
                        help='Path to store log files.')
    args = parser.parse_args()
    if not args.secret:
        sys.stderr.write('Secret is required.\n')
        sys.exit(1)
    with open(args.secret, 'r') as fp:
        args.secret = fp.readline().strip()

    start(args)

if __name__ == '__main__':
    main()
