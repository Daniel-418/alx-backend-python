from datetime import datetime, time
from django.utils import timezone
from django.http import HttpResponseForbidden
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


class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_local_time = timezone.localtime().time()
        start_time = time(18, 0)
        end_time = time(21, 0)

        print("middleware ran hurray!!!")
        if not (start_time <= current_local_time <= end_time):
            return HttpResponseForbidden(
                content=f"Office hours are strictly {start_time} to {end_time} and it is {current_local_time.strftime('%H:%M')}."  # pyright: ignore
            )
        else:
            response = self.get_response(request)
            return response
