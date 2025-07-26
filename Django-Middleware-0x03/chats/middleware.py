from datetime import datetime, timedelta
import logging
from django.http import HttpResponseForbidden
from collections import defaultdict

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.logger = logging.getLogger(__name__)
        self.handler = logging.FileHandler('requests.log')
        self.logger.addHandler(self.handler)

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else 'Anonymous'
        log_entry = f"{datetime.now()} - User: {user} - Path: {request.path}\n"
        self.logger.warning(log_entry)
        return self.get_response(request)

class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_hour = datetime.now().hour

        # Restrict access outside 6PM (18) to 9PM (21)
        if current_hour < 18 or current_hour >= 21:
            return HttpResponseForbidden("Access to the chat is only allowed between 6PM and 9PM.")

        return self.get_response(request)

class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.request_logs = defaultdict(list)  # IP -> [timestamps]

    def __call__(self, request):
        if request.method == "POST":
            ip_address = self.get_client_ip(request)
            current_time = datetime.now()

            # Remove timestamps older than 1 minute
            self.request_logs[ip_address] = [
                timestamp for timestamp in self.request_logs[ip_address]
                if current_time - timestamp < timedelta(minutes=1)
            ]

            if len(self.request_logs[ip_address]) >= 5:
                return HttpResponseForbidden("Rate limit exceeded. You can only send 5 messages per minute.")

            self.request_logs[ip_address].append(current_time)

        return self.get_response(request)

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")
        return ip
