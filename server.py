#!/usr/bin/env python3

from http.server import (
    BaseHTTPRequestHandler,
    HTTPServer,
)
import itertools
import json
import shutil
from urllib.parse import (
    parse_qs,
    urlparse,
)


HOST, PORT = '', 9000
JSON_CTYPE = 'application/json'


class Handler(BaseHTTPRequestHandler):

    count = itertools.count()

    def do_GET(self):
        print('-' * 120)
        print('request: #{}'.format(next(self.count)))
        print('path:\n{}'.format(self.path))
        print('headers:\n{}'.format(dict(self.headers)))
        url = urlparse(self.path)
        query = parse_qs(url.query)
        print('query:\n{}'.format(query))

        # Process request.
        if (
            '/meta/any' in url.path and
            set(query.get('include', [])) == set(['id', 'supported-series', 'published'])
        ):
            # /v5/~juju-gui/bionic/jujushell/meta/any?include=id&include=supported-series&include=published
            self.resolve_charm(url)
            return

        if '/archive' in url.path:
            # /v5/~juju-gui/jujushell-15/archive?channel=stable
            self.download_charm(url)
            return

        if url.path.endswith('/meta/resources'):
            # /v5/~juju-gui/jujushell-15/meta/resources?channel=stable
            self.get_all_resources_info(url)
            return

        if '/meta/resources/' in url.path:
            # /v5/~juju-gui/jujushell-15/meta/resources/jujushell/14?channel=stable
            self.get_resource_info(url)
            return

        if '/resource/' in url.path:
            # /v5/~juju-gui/jujushell-15/resource/jujushell/14?channel=stable
            self.download_resource(url)
            return


        self.send_response(404)
        self.end_headers()

    def resolve_charm(self, url):
        print('resolve charm')
        self.send_response(200)
        self.send_header('Content-type', JSON_CTYPE)
        self.end_headers()
        response = {
            "Id": "cs:~juju-gui/jujushell-15",
            "Meta": {
                "id": {
                    "Id": "cs:~juju-gui/jujushell-15",
                    "Name": "jujushell",
                    "Revision": 15,
                    "User": "juju-gui",
                },
                "published": {
                    "Info": [
                        {
                            "Channel": "stable",
                            "Current": True
                        }
                    ]
                },
                "supported-series": {
                    "SupportedSeries": [
                        "bionic"
                    ]
                }
            }
        }
        self.wfile.write(json.dumps(response).encode('utf-8'))

    def download_charm(self, url):
        print('download charm')
        self.send_response(200)
        self.send_header('Content-type', 'application/zip')
        self.send_header('Content-Length', 7988571)
        self.send_header('Content-Sha384', '7be11052466b4ba3cad1c23bc14aebb6c1b9ae9c43d04d80efee870a0895828d746da4b25887f3e8903a38f6776e055d')
        self.send_header('Entity-Id', 'cs:~juju-gui/jujushell-15')
        self.end_headers()
        with open('jujushell.zip', 'rb') as zipfile:
            shutil.copyfileobj(zipfile, self.wfile)

    def get_all_resources_info(self, url):
        print('get all resources info')
        self.send_response(200)
        self.send_header('Content-type', JSON_CTYPE)
        self.end_headers()
        response = [resource]
        self.wfile.write(json.dumps(response).encode('utf-8'))

    def get_resource_info(self, url):
        print('get resource info')
        self.send_response(200)
        self.send_header('Content-type', JSON_CTYPE)
        self.end_headers()
        response = resource
        self.wfile.write(json.dumps(response).encode('utf-8'))

    def download_resource(self, url):
        print('download resource')
        self.send_response(200)
        self.send_header('Content-type', 'application/octet-stream')
        self.send_header('Content-Length', 19397280)
        self.send_header('Content-Sha384', '5a987129cd0835c0df426fbbf23dae980d6936903c6ca2aea68da96ec8bb2beb1fee974b3bafc523ea88eea8e564b590')
        self.end_headers()
        with open('jujushell.resource', 'rb') as zipfile:
            shutil.copyfileobj(zipfile, self.wfile)


resource = {
    "Description": "The jujushell application binary.",
    "Fingerprint": "WphxKc0INcDfQm+78j2umA1pNpA8bKKupo2pbsi7K+sf7pdLO6/FI+qI7qjlZLWQ",
    "Name": "jujushell",
    "Path": "jujushell",
    "Revision": 14,
    "Size": 19397280,
    "Type": "file"
}


def main():
    srv = HTTPServer((HOST, PORT), Handler)
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass
    srv.server_close()


if __name__ == '__main__':
    main()
