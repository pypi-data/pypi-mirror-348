import os
import asyncio

async def serve_static(request):
    filename = request.path[len("/static/"):]
    filepath = os.path.join("static", filename)

    if not os.path.exists(filepath):
        return "File Not Found", 404

    _, ext = os.path.splitext(filename)
    content_types = {
        ".html": "text/html",
        ".css": "text/css",
        ".js": "application/javascript",
        ".png": "image/png",
        ".jpg": "image/jpeg",
    }

    content_type = content_types.get(ext, "application/octet-stream")

    with open(filepath, "rb") as f:
        data = f.read()

    return (f"HTTP/1.1 200 OK\r\nContent-Type: {content_type}\r\n"
            f"Content-Length: {len(data)}\r\n\r\n").encode() + data
