import json
import threading
import unittest
import urllib.request
import urllib.error
from bastion.web import make_server

class WebTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = make_server(0)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.url = f'http://127.0.0.1:{cls.server.server_port}'
    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join()
    def test_generation_is_deterministic(self):
        with urllib.request.urlopen(self.url+'/api/generate?seed=2&count=3') as response:
            first = json.load(response)
        with urllib.request.urlopen(self.url+'/api/generate?seed=2&count=3') as response:
            self.assertEqual(first, json.load(response))
    def test_unbounded_requests_are_rejected(self):
        with self.assertRaises(urllib.error.HTTPError) as caught:
            urllib.request.urlopen(self.url+'/api/generate?count=999')
        self.assertEqual(caught.exception.code, 400)
    def test_static_assets_and_security_headers(self):
        for asset in ['/', '/app.js', '/style.css']:
            with urllib.request.urlopen(self.url+asset) as response:
                self.assertEqual(response.status, 200)
                self.assertEqual(response.headers['X-Content-Type-Options'], 'nosniff')
                self.assertIn("frame-ancestors 'none'", response.headers['Content-Security-Policy'])
    def test_duplicate_parameters_and_bad_seed_fail_cleanly(self):
        for query in ['count=1&count=2', 'seed=oops', 'career=404']:
            with self.assertRaises(urllib.error.HTTPError) as caught:
                urllib.request.urlopen(self.url+'/api/generate?'+query)
            self.assertEqual(caught.exception.code, 400)
    def test_traversal_cannot_read_catalog_files(self):
        with self.assertRaises(urllib.error.HTTPError) as caught:
            urllib.request.urlopen(self.url+'/../data/careers.json')
        self.assertEqual(caught.exception.code, 404)
    def test_foreign_host_is_rejected(self):
        request = urllib.request.Request(self.url+'/api/careers', headers={'Host':'evil.example'})
        with self.assertRaises(urllib.error.HTTPError) as caught:
            urllib.request.urlopen(request)
        self.assertEqual(caught.exception.code, 403)
