import time
import os
import psutil
from .collector import record

class WatchlogAPMMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.process = psutil.Process(os.getpid())

    def __call__(self, request):
        start = time.perf_counter()
        response = self.get_response(request)
        duration = (time.perf_counter() - start) * 1000

        mem = self.process.memory_info()

        record({
            "type": "request",
            "service": "django-app",
            "path": getattr(request, 'path', 'unknown'),
            "method": getattr(request, 'method', 'UNKNOWN'),
            "statusCode": getattr(response, 'status_code', 0),
            "duration": round(duration, 2),
            "timestamp": time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
            "memory": {
                "rss": mem.rss,
                "heapUsed": mem.vms,
                "heapTotal": mem.vms  # ✅ یا همون vms رو دوبار استفاده کن، چون data نداریم
            }
        })

        return response
