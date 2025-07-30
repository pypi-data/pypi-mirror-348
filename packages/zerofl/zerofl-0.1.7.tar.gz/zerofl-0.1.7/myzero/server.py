import socket
import threading
import asyncio
from .request import parse_request
from .response import build_response

def run_server(app, host="127.0.0.1", port=8000):
    def _handle_client(conn, addr, app):
        data = conn.recv(4096)
        if not data:
            return

        request = parse_request(data)
        if not request:
            conn.sendall(b"HTTP/1.1 400 Bad Request\r\n\r\n")
            return

        loop = asyncio.new_event_loop()
        response_data = loop.run_until_complete(app.handle_request(request))
        conn.sendall(build_response(response_data))
        conn.close()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((host, port))
        sock.listen(100)
        print(f"Server running on http://{host}:{port}")

        while True:
            conn, addr = sock.accept()
            thread = threading.Thread(target=_handle_client, args=(conn, addr, app))
            thread.start()
