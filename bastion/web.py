"""A loopback-only, dependency-free character generation server."""
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
from urllib.parse import parse_qs, urlsplit
from .party import generate_party
from .catalog import load_catalog

ASSETS = Path(__file__).with_name('web')

def make_server(port=8765):
    catalog = load_catalog()
    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *args):
            pass
        def respond(self, status, body, content_type='application/json; charset=utf-8'):
            content = body if isinstance(body, bytes) else body.encode('utf-8')
            self.send_response(status)
            self.send_header('Content-Type', content_type)
            self.send_header('Content-Length', str(len(content)))
            self.send_header('Cache-Control','no-store')
            self.send_header('X-Content-Type-Options','nosniff')
            self.send_header('Content-Security-Policy', "default-src 'self'; object-src 'none'; frame-ancestors 'none'; base-uri 'none'")
            self.end_headers()
            self.wfile.write(content)
        def do_GET(self):
            host = self.headers.get('Host', '').split(':')[0]
            if host not in ('localhost','127.0.0.1'):
                return self.respond(403, '{"error":"Local access only"}')
            target = urlsplit(self.path)
            try:
                if len(target.query) > 4096:
                    raise ValueError('Request is too long')
                query = parse_qs(target.query)
                if any(len(values) != 1 for values in query.values()):
                    raise ValueError('Repeated query parameters are not supported')
                if target.path == '/api/careers':
                    return self.respond(200, json.dumps([{'id':e['id'],'title':e['title']} for e in catalog.values()]))
                if target.path == '/api/generate':
                    count = int(query.get('count',['1'])[0])
                    if not 1 <= count <= 20:
                        raise ValueError('Choose 1–20 characters')
                    seed = int(query['seed'][0]) if 'seed' in query else None
                    values = generate_party(count, seed=seed, name=query.get('name',['Adventurer'])[0],
                        career=query.get('career',[None])[0], catalog=catalog,
                        random_name=query.get('random_name',['false'])[0] == 'true')
                    return self.respond(200, json.dumps([c.to_dict() for c in values], ensure_ascii=False))
                assets = {'/':('index.html','text/html'),'/app.js':('app.js','text/javascript'),'/style.css':('style.css','text/css')}
                if target.path in assets:
                    name, mime = assets[target.path]
                    return self.respond(200, (ASSETS/name).read_bytes(), mime+'; charset=utf-8')
                self.respond(404, '{"error":"Not found"}')
            except (ValueError, OSError) as error:
                self.respond(400, json.dumps({'error':str(error)}))
    return ThreadingHTTPServer(('127.0.0.1', port), Handler)

def serve(port=8765):
    with make_server(port) as server:
        print(f'Bastion generator: http://127.0.0.1:{server.server_port}', flush=True)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass
