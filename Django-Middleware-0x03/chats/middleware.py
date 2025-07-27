import logging
from datetime import datetime
import time
from collections import defaultdict
from django.http import JsonResponse
from django.http import HttpResponseForbidden

class RequestLoggingMiddleware:
    """
    Middleware that logs each request with timestamp, user, and path.
    Logs are saved in `requests.log`.
    """

    def __init__(self, get_response):
        self.get_response = get_response
        # Configure logger
        self.logger = logging.getLogger("request_logger")
        handler = logging.FileHandler("requests.log")
        formatter = logging.Formatter('%(message)s')
        handler.setFormatter(formatter)
        self.logger.setLevel(logging.INFO)
        if not self.logger.handlers:
            self.logger.addHandler(handler)

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else "Anonymous"
        log_entry = f"{datetime.now()} - User: {user} - Path: {request.path}"
        self.logger.info(log_entry)

        response = self.get_response(request)
        return response

class RestrictAccessByTimeMiddleware:
    """
    Middleware that restricts access to the app outside of 6PM to 9PM.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_hour = datetime.now().hour

        # Allow access only between 18:00 (6PM) and 21:00 (9PM), inclusive
        if current_hour < 18 or current_hour > 21:
            return HttpResponseForbidden("Access is restricted to between 6PM and 9PM.")

        return self.get_response(request)
    

class OffensiveLanguageMiddleware:
    """
    Middleware to limit the number of POST messages per minute from a single IP address.
    Max: 5 messages per 60 seconds.
    """

    def __init__(self, get_response):
        self.get_response = get_response
        self.ip_log = defaultdict(list)
        self.rate_limit = 5  # messages
        self.window = 60  # seconds

    def __call__(self, request):
        # Apply only to POST requests to the message endpoint
        if request.method == "POST" and "/messages" in request.path:
            ip = self.get_client_ip(request)
            current_time = time.time()

            # Clean up timestamps older than 1 minute
            recent_timestamps = [
                ts for ts in self.ip_log[ip]
                if current_time - ts < self.window
            ]
            self.ip_log[ip] = recent_timestamps

            if len(recent_timestamps) >= self.rate_limit:
                return JsonResponse(
                    {"detail": "Rate limit exceeded: Max 5 messages per minute."},
                    status=429
                )

            # Log the current POST timestamp
            self.ip_log[ip].append(current_time)

        return self.get_response(request)

    def get_client_ip(self, request):
        """Get client IP address from request headers."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0].strip()
        return request.META.get('REMOTE_ADDR')
    

class RolepermissionMiddleware:
    """
    Middleware that restricts access to users based on role.
    Only 'admin' or 'moderator' roles are allowed to perform protected actions.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user

        # Allow only authenticated users with specific roles
        if user.is_authenticated:
            user_role = getattr(user, 'role', None)

            if user_role in ['admin', 'moderator']:
                return self.get_response(request)

        # Otherwise block access
        return HttpResponseForbidden("You do not have permission to perform this action.")