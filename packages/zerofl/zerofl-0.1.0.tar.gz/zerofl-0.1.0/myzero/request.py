import json
from urllib.parse import parse_qs

class Request:
    def __init__(self, method, path, headers, body, data=None):
        self.method = method
        self.path = path
        self.headers = headers
        self.body = body
        self.data = data

def parse_request(raw_data):
    try:
        headers_end = raw_data.find(b"\r\n\r\n")
        header_part = raw_data[:headers_end].decode()
        lines = header_part.split("\r\n")
        method, path, _ = lines[0].split(" ", 2)

        headers = {}
        for line in lines[1:]:
            if ": " in line:
                key, value = line.split(": ", 1)
                headers[key] = value

        body = raw_data[headers_end + 4:] if len(raw_data) > headers_end + 4 else b""
        content_type = headers.get("Content-Type", "")

        data = None
        if content_type == "application/json":
            try:
                data = json.loads(body.decode())
            except json.JSONDecodeError:
                pass
        elif content_type.startswith("application/x-www-form-urlencoded"):
            data = parse_qs(body.decode())

        return Request(method, path, headers, body, data)
    except Exception as e:
        print(f"Request parsing error: {e}")
        return None
