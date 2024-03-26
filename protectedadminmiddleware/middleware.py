from random import choice
from django.conf import settings
from django.http import HttpResponseRedirect
from re import compile


class InternalIPsOnly:
    """
    checks the path against settings.IP_PROTECTED_PATHS
    If it matches, checks against settings.INTERNAL_IPS,
    if THAT matches, allow, else, disallow
    """

    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        response = self.get_response(request)

        # if debug is true bypass this
        if settings.DEBUG:
            return response

        IP_PROTECTED_PATHS = getattr(settings, 'IP_PROTECTED_PATHS',  compile('^' + '/' + 'admin' + '/'))
        BANNED_URLS = getattr(settings, 'BANNED_URLS', ['https://www.google.com'])
        INTERNAL_IPS = getattr(settings, 'INTERNAL_IPS', ['127.0.0.1'])

        should_continue = False
        for pattern in IP_PROTECTED_PATHS:
            if pattern.search(request.path):
                should_continue = True
                break
        if not should_continue:
            return response

        choice_ = choice(BANNED_URLS)

        # Because of heroku have to use HTTP_X_FORWARDED_FOR.
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR', None)
        if x_forwarded_for:
            # check if HTTP_X_FORWARDED_FOR or is greater than 1
            # Because we use private VPN this should never occur so whoever is accessing with multiple ips is a spammer/hacker/spoofer
            if len(x_forwarded_for.split(',')) > 1:
                print("HTTP_X_FORWARDED_FOR: ", x_forwarded_for)
                return HttpResponseRedirect(choice_)
            remote_addr = x_forwarded_for.split(',')[0].strip()
        else:
            remote_addr = request.META.get('REMOTE_ADDR', None)

        if not (remote_addr in INTERNAL_IPS):
            print(f"HTTP_X_FORWARDED_FOR{remote_addr}")
            try:
                print("Forbidden User: ", request.user)
            except:
                pass
            return HttpResponseRedirect(choice_)

        return response
