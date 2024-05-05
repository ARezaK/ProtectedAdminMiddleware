from random import choice
from django.conf import settings
from django.http import HttpResponseRedirect
from re import compile


class ProtectedAdminMiddleware:
    """
    checks the path against settings.IP_PROTECTED_PATHS
    If it matches, checks against settings.INTERNAL_IPS,
    if THAT matches, allow, else, disallow
    """

    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.
        path_pattern = getattr(settings, 'IP_PROTECTED_PATHS', '^/admin/')
        self.protected_paths_regex = compile(path_pattern)
        self.banned_urls = getattr(settings, 'BANNED_URLS', ['https://www.google.com'])
        self.internal_ips = set(getattr(settings, 'INTERNAL_IPS', ['127.0.0.1']))


    def __call__(self, request):
        response = self.get_response(request)

        # if debug is true bypass this
        if settings.DEBUG:
            return response

        # Check if the requested path is a protected path
        if not self.protected_paths_regex.search(request.path):
            return response

        # Because of heroku have to use HTTP_X_FORWARDED_FOR.
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR', None)
        if x_forwarded_for:
            # check if HTTP_X_FORWARDED_FOR or is greater than 1
            # Because we use private VPN this should never occur so whoever is accessing with multiple ips is a spammer/hacker/spoofer
            if len(x_forwarded_for.split(',')) > 1:
                print("HTTP_X_FORWARDED_FOR: ", x_forwarded_for)
                return HttpResponseRedirect(choice(self.banned_urls))
            remote_addr = x_forwarded_for.split(',')[0].strip()
        else:
            remote_addr = request.META.get('REMOTE_ADDR', None)

        if remote_addr not in self.internal_ips:
            print(f"HTTP_X_FORWARDED_FOR{remote_addr}")
            if hasattr(request, 'user'):
                print("Forbidden User: ", request.user)
            return HttpResponseRedirect(choice(self.banned_urls))

        return response
