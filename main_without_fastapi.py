import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse

data = {
    'users': [
        'Alice',
        'Bob',
        'Charlie',
        'David',
        'Eve',
        'Frank',
        'Grace']
}

class RequestHandler(BaseHTTPRequestHandler):
    def _set_headers(self, status=200):
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_GET(self):
        if self.path == "/users":
            self._set_headers()
            self.wfile.write(json.dumps({'data': data}).encode())

        elif self.path == "/health":
            self._set_headers()
            self.wfile.write(json.dumps({'status': 'healthy'}).encode())

        elif self.path == "/version":
            self._set_headers()
            self.wfile.write(json.dumps({'version': '1.0.0'}).encode())

        elif self.path == "/metrics":
            self._set_headers()
            self.wfile.write(json.dumps({
                'total_users': len(data['users']),
                'example_metric': 12345
            }).encode())

        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({'message': 'Not Found'}).encode())

    def do_POST(self):
        if self.path == "/users":
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            user = parse_qs(post_data.decode())['user'][0]

            if user in data['users']:
                self._set_headers()
                self.wfile.write(json.dumps({'data': data, 'message': "the user already exists"}).encode())
            else:
                data['users'].append(user)
                self._set_headers()
                self.wfile.write(json.dumps({'data': data, 'message': "the user has been added"}).encode())

    def do_DELETE(self):
        parsed_path = urlparse(self.path)
        if parsed_path.path == "/user":
            query = parse_qs(parsed_path.query)
            user = query.get('user', [None])[0]

            if user in data['users']:
                data['users'].remove(user)
                self._set_headers()
                self.wfile.write(json.dumps({'data': data, 'message': 'the user has been deleted'}).encode())
            else:
                self._set_headers()
                self.wfile.write(json.dumps({'data': data, 'message': "the user does not exist"}).encode())

        elif parsed_path.path == "/users":
            data['users'].clear()
            self._set_headers()
            self.wfile.write(json.dumps({'data': data, 'message': 'all users have been deleted'}).encode())

    def do_PUT(self):
        if self.path == "/users":
            content_length = int(self.headers['Content-Length'])
            put_data = self.rfile.read(content_length)
            params = parse_qs(put_data.decode())
            old_user = params['old_user'][0]
            new_user = params['new_user'][0]

            if old_user in data['users']:
                index = data['users'].index(old_user)
                data['users'][index] = new_user
                self._set_headers()
                self.wfile.write(json.dumps({'data': data, 'message': "the user has been updated"}).encode())
            else:
                self._set_headers()
                self.wfile.write(json.dumps({'data': data, 'message': "the user does not exist"}).encode())

def run(server_class=HTTPServer, handler_class=RequestHandler, port=8002):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting httpd server on port {port}')
    httpd.serve_forever()

if __name__ == "__main__":
    run()
