import os
import mimetypes

from tcp_server import TCPServer
from http import HTTPRequest
from typing import Dict

class HTTPServer(TCPServer):
    status_codes = {
        200: 'OK',
        404: 'Not Found',
        501: 'Not Implemented',
    }

    headers = {
        'Server': 'SYNACKd server',
        'Content-Type': 'text/html',
    }

    def prepare_response_line(
        self,
        status_code: Dict
    ) -> str:
        """Returns response line"""
        reason = self.status_codes[status_code]
        return "HTTP/1.1 %s %s\r\n" % (status_code, reason)

    def prepare_response_headers(
        self,
        extra_headers=None) -> str:
        """Returns headers
        The `extra_headers` can be a dict for sending 
        extra headers for the current response
        """
        headers_copy = self.headers.copy() # make a local copy of headers

        if extra_headers:
            headers_copy.update(extra_headers)

        headers = ""

        for h in self.headers:
            headers += "%s: %s\r\n" % (h, self.headers[h])
        return headers

    def handle_request(self, data) -> str:
        request = HTTPRequest(data)

        try:
            handler = getattr(self, 'handle_%s' % request.method)
        except AttributeError:
            handler = self.handle_http_501
        
        response = handler(request)
        return response

    def handle_http_501(self, request) -> None:
        response_line = self.prepare_response_line(status_code=501)
        response_headers = self.prepare_response_headers()
        blank_line = "\r\n"

        response_body = "<h1>501 Not Implemented</h1>"

        return "%s%s%s%s" % (
            response_line, 
            response_headers, 
            blank_line, 
            response_body
        )

    def handle_GET(self, request):
        filename = request.uri.strip('/') # remove the slash from URI

        if os.path.exists(filename):
            response_line = self.prepare_response_line(200)
            content_type = mimetypes.guess_type(filename)[0] or 'text/html'
            extra_headers = {'Content-Type': content_type}
            response_headers = self.prepare_response_headers(extra_headers=extra_headers)

            with open(filename) as f:
                response_body = f.read()
        else:
            response_line = self.prepare_response_line(404)
            response_headers = self.prepare_response_headers()
            response_body = "<h1>404 Not Found</h1>"

        blank_line = "\r\n"

        return "%s%s%s%s" % (
                response_line,
                response_headers,
                blank_line,
                response_body
            )