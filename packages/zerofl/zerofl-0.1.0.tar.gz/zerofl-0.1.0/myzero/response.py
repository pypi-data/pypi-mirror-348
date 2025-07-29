import json

def build_response(data):
    if isinstance(data, tuple):
        body, status_code = data
    else:
        body, status_code = data, 200

    if isinstance(body, dict):
        body_str = json.dumps(body)
        headers = "Content-Type: application/json\r\n"
    else:
        body_str = str(body)
        headers = "Content-Type: text/plain\r\n"

    status_line = f"HTTP/1.1 {status_code} OK\r\n"
    body_len = f"Content-Length: {len(body_str)}\r\n"
    response = status_line + headers + body_len + "\r\n" + body_str
    return response.encode()
