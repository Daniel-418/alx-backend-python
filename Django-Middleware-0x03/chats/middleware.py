from datetime import datetime
from rest_framework_simplejwt.authentication import JWTAuthentication


class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user

        if not user.is_authenticated:
            try:
                auth_result = JWTAuthentication().authenticate(request)
                if auth_result:
                    user, _ = auth_result
            except Exception:
                pass

        with open("requests.log", "a", encoding="utf-8") as f:
            log_str = f"{datetime.now()} - User: {user} -Path: {request.path}\n"
            f.write(log_str)
        response = self.get_response(request)
        return response

