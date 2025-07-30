import re
from functools import wraps
import asyncio
from .server import run_server
from .request import Request
from .response import build_response
from .middleware import MiddlewareManager
from .static import serve_static

class Zero:
    def __init__(self, static_folder="static"):
        self.routes = []
        self.error_handler = None
        self.middleware = MiddlewareManager()
        self.static_folder = static_folder

    def route(self, path, methods=["GET"]):
        def decorator(handler):
            pattern = self._convert_path_to_regex(path)
            self.routes.append({
                "pattern": pattern,
                "methods": methods,
                "handler": handler
            })
            return handler
        return decorator

    def _convert_path_to_regex(self, path):
        regex = re.sub(r'<(\w+)>', r'(?P<\1>[^/]+)', path)
        return re.compile(f"^{regex}$")

    def use(self, middleware_func):
        self.middleware.add(middleware_func)

    def run(self, host="127.0.0.1", port=8000):
        run_server(self, host, port)

    async def handle_request(self, request):
        for middleware in self.middleware.before_request:
            request = middleware(request) or request

        if request.path.startswith("/static/"):
            return await serve_static(request)

        for route in self.routes:
            match = route["pattern"].match(request.path)
            if match and request.method in route["methods"]:
                kwargs = match.groupdict()
                handler = route["handler"]

                try:
                    if asyncio.iscoroutinefunction(handler):
                        response = await handler(request, **kwargs)
                    else:
                        response = handler(request, **kwargs)
                    return response
                except Exception as e:
                    if self.error_handler:
                        return self.error_handler(e)
                    else:
                        return {"error": str(e)}, 500

        return "Not Found", 404

    def errorhandler(self, handler):
        self.error_handler = handler
