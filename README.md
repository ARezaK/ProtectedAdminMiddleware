# ProtectedAdminMiddleware
For protecting django admin page by IP address

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
