from django.shortcuts import redirect
from django.urls import reverse
from django.conf import settings
import re


class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        exempt_urls = [re.compile(url) for url in settings.LOGIN_EXEMPT_URLS]
        if not request.user.is_authenticated:
            path = request.path_info.lstrip('/')
            if not any(url.match(path) for url in exempt_urls):
                return redirect(reverse('login:login'))

        response = self.get_response(request)
        return response
