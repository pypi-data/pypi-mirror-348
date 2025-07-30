def parse_request(raw_data):
    try:
        # Convert raw bytes to string
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

        method, path, _ = lines[0].split(" ", 2)

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
                data = None

        return Request(method, path, headers, body, data)

    except Exception as e:
        print(f"Request parsing error: {e}")
        return None