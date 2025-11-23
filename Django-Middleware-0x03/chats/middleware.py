from datetime import datetime, time
from django.urls import resolve
from django.utils import timezone
from django.http import HttpResponseForbidden
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.core import cache
from django.core.cache import cache
import re
from .models import User


def get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")

    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0].strip()
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip


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
            request.user = user
        response = self.get_response(request)
        return response


class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_local_time = timezone.localtime().time()
        start_time = time(18, 0)
        end_time = time(21, 0)

        if not (start_time <= current_local_time <= end_time):
            return HttpResponseForbidden(
                content=f"Office hours are strictly {start_time} to {end_time} and it is {current_local_time.strftime('%H:%M')}."  # pyright: ignore
            )
        with open("requests.log", "a", encoding="utf-8") as f:
            log_str = f"{datetime.now()} - User: {request.user} -Path: {request.path} -IP: {get_client_ip(request)}\n"
            f.write(log_str)
        response = self.get_response(request)
        return response


class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.message_limit = 5
        self.message_timeout = 20

    def __call__(self, request):
        if request.method == "POST":
            match = resolve(request.path)

            if match.url_name == "conversation-messages-list":
                print(match.url_name)
                ip = get_client_ip(request)
                cache_key = f"msg_limit_{ip}"
                count = cache.get(cache_key)

                if count is None:
                    cache.set(cache_key, 1, self.message_timeout)
                else:
                    if count >= self.message_limit:
                        return HttpResponseForbidden(
                            content=b"you've reached the limit of sending messages try again in another minute"
                        )
                    else:
                        try:
                            cache.incr(cache_key)
                        except ValueError:
                            cache.set(cache_key, 1, self.message_timeout)
        response = self.get_response(request)
        return response


class RolepermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user
        if user.role != User.Roles.ADMIN and user.role != User.Roles.HOST:
            return HttpResponseForbidden(
                content=b"you need to be an admin or host to access this page"
            )
        response = self.get_response(request)
        return response

