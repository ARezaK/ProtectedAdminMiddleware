# ProtectedAdminMiddleware
For protecting django admin page (or other pages) by IP address

Add to requirements.txt
```
protectedadminmiddleware@ git+https://github.com/ARezaK/ProtectedAdminMiddleware.git


```

Add these to settings

```
ADMIN_URL = 'adminsecretpage'
```

```
IP_PROTECTED_PATHS = [
    re.compile('^' + '/' + ADMIN_URL + '/'),
]
```

```
# website to redirect to 
BANNED_URLS = [
    "https://donotcomehereagain.com"
]
```

```
INTERNAL_IPS = ['127.0.0.1', 'otherip_addresses']
```


Add to INSTALLED_APPS
```
INSTALLED_APPS = [
    ...
    'ProtectedAdminMiddleware',
    ...
]
```

Add to middleware
```
MIDDLEWARE = [
    ...
    'ProtectedAdminMiddleware.middleware.ProtectedAdminMiddleware',
    ...
]
```
