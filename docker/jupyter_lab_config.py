c = get_config()

c.ServerApp.base_url = '/'
c.ServerApp.ip = '0.0.0.0'
c.ServerApp.open_browser = False
c.ServerApp.port = 8888
c.ServerApp.allow_root = True
c.ServerApp.password = 'argon2:$argon2id$v=19$m=10240,t=10,p=8$xMPnfpR4mpA6V7zN3jIBSA$92WT4iExe4Sxj7PZtWLsXQxcx5eZOuVFgT3WZdVmmFY'
c.ServerApp.root_dir = '/app/notebooks'
c.ServerApp.certfile = '/etc/ssl/tls.crt'
c.ServerApp.keyfile = '/etc/ssl/tls.key'
c.ServerApp.use_https = True

# Additional security settings
c.ServerApp.disable_check_xsrf = False
c.ServerApp.csp = "default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self'"
c.ServerApp.tornado_settings = {
    'headers': {
        'Content-Security-Policy': "default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self'; connect-src 'self';",
        'X-XSS-Protection': '1; mode=block',
        'X-Content-Type-Options': 'nosniff',
        'Strict-Transport-Security': 'max-age=31536000; includeSubDomains; preload',
        'Server': ''
    },
    'cookie_options': {'secure': True, 'httponly': True}
}
c.ServerApp.session_idle_timeout = 600
from jupyter_server.auth import passwd_check_rate_limiter
c.ServerApp.password_check_rate_limiter = passwd_check_rate_limiter(limit=5, period=3600)
c.ServerApp.allow_origin = 'http://localhost:8888'
c.ServerApp.tornado_settings['headers']['Server'] = ''
