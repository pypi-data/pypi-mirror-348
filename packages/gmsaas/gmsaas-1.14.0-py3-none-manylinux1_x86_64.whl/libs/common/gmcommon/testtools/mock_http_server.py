# Standard library imports...
from http.server import BaseHTTPRequestHandler, HTTPServer
import socket
from contextlib import contextmanager
from threading import Thread


class MockServerRequestHandler(BaseHTTPRequestHandler):
    """
    A simple BaseHTTPRequestHandler implementation returning always the same page
    """

    def do_GET(self):
        # Process an HTTP GET request and return a response with an HTTP 200 status.
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        response = (
            b"<html>\n"
            b"<head><title>This is a sample page</title></head>\n"
            b"<body><p>Hello from Genymotion</p></body>\n"
            b"</html>\n"
        )
        self.wfile.write(response)


def start_http_server():
    """
    Start a mock HTTP server on its proper thread.
    :return: returns the local port where the server is running
    """
    mock_server_port = get_free_port()
    mock_server = HTTPServer(("localhost", mock_server_port), MockServerRequestHandler)

    mock_server_thread = Thread(target=mock_server.serve_forever)
    mock_server_thread.setDaemon(True)
    mock_server_thread.start()

    return mock_server_port


@contextmanager
def busy_port(port):
    sock = socket.socket(socket.AF_INET6, type=socket.SOCK_STREAM)
    sock.bind(("::", port))
    yield sock
    sock.close()


def get_free_port():
    sock = socket.socket(socket.AF_INET6, type=socket.SOCK_STREAM)
    sock.bind(("::", 0))
    _, port, *rest = sock.getsockname()
    sock.close()
    return port
