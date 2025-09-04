import os
from datetime import datetime
from django.utils.deprecation import MiddlewareMixin

LOG_DIR = 'logs'
LOG_FILE = os.path.join(LOG_DIR, 'app.log')
os.makedirs(LOG_DIR, exist_ok=True)

def write_log_line(line: str):
    timestamp = datetime.utcnow().isoformat()
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(f"{timestamp} - {line}\n")

class LoggingMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request._start_time = datetime.utcnow()

    def process_response(self, request, response):
        method = request.method
        path = request.get_full_path()
        status_code = getattr(response, 'status_code', 'unknown')
        client = request.META.get('REMOTE_ADDR', 'unknown')
        duration_ms = int((datetime.utcnow() - getattr(request, '_start_time', datetime.utcnow())).total_seconds() * 1000)
        write_log_line(f"METHOD={method} PATH={path} STATUS={status_code} CLIENT={client} TIME_MS={duration_ms}")
        if hasattr(request, '_log_event'):
            write_log_line(request._log_event)
        return response
