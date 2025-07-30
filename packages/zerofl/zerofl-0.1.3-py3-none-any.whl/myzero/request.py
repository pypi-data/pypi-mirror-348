# myzero/request.py

import json
from urllib.parse import parse_qs

class Request:
    """
    A simple HTTP request object that wraps parsed data.
    """
    def __init__(self, method, path, headers, body, data=None):
        self.method = method       # HTTP method (GET, POST)
        self.path = path           # URL path
        self.headers = headers     # Parsed headers
        self.body = body           # Raw body bytes
        self.data = data           # Parsed JSON or form data


def parse_request(raw_data):
    """
    Parses raw HTTP request bytes into a Request object.
    """
    try:
        # Decode raw data safely
        raw_text = raw_data.decode('utf-8', errors='ignore')
        headers_end = raw_text.find("\r\n\r\n")

        if headers_end == -1:
            print("No headers/body separator found")
            return None

        header_part = raw_text[:headers_end]
        lines = header_part.split("\r\n")

        if len(lines) < 1:
            print("Malformed request line")
            return None

        # Parse method, path, HTTP version
        method, path, _ = lines[0].split(" ", 2)

        # Parse headers
        headers = {}
        for line in lines[1:]:
            if ": " in line:
                key, value = line.split(": ", 1)
                headers[key.strip()] = value.strip()

        # Extract body
        body_start = headers_end + 4
        body = raw_data[body_start:] if len(raw_data) > body_start else b""

        content_type = headers.get("Content-Type", "").lower()
        data = None

        # Handle JSON
        if content_type == "application/json":
            try:
                data = json.loads(body.decode('utf-8'))
            except (json.JSONDecodeError, UnicodeDecodeError) as e:
                print(f"JSON decode error: {e}")
                data = None

        # Handle URL-encoded form
        elif content_type.startswith("application/x-www-form-urlencoded"):
            try:
                data = parse_qs(body.decode('utf-8'))
            except Exception as e:
                print(f"Form decode error: {e}")

        # Return Request object
        return Request(method, path, headers, body, data)

    except Exception as e:
        print(f"Request parsing error: {e}")
        return None