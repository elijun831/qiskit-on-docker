import etcd3

# Initialize etcd client
etcd = etcd3.client(host='etcd', port=2379)

# Fetch settings from etcd
def get_etcd_value(key, default):
    value = etcd.get(key)[0]
    return value.decode('utf-8') if value else default

base_url = get_etcd_value('/jupyterlab/base_url', '/')
ip = get_etcd_value('/jupyterlab/ip', '0.0.0.0')
port = int(get_etcd_value('/jupyterlab/port', '8888'))
allow_root = get_etcd_value('/jupyterlab/allow_root', 'True').lower() == 'true'
password = get_etcd_value('/jupyterlab/password', 'argon2:$argon2id$v=19$m=10240,t=10,p=8$xMPnfpR4mpA6V7zN3jIBSA$92WT4iExe4Sxj7PZtWLsXQxcx5eZOuVFgT3WZdVmmFY')
root_dir = get_etcd_value('/jupyterlab/root_dir', '/app/notebooks')
certfile = get_etcd_value('/jupyterlab/certfile', '/home/appuser/ssl_cert/localhost.pem')
keyfile = get_etcd_value('/jupyterlab/keyfile', '/home/appuser/ssl_cert/localhost.key')
use_https = get_etcd_value('/jupyterlab/use_https', 'True').lower() == 'true'
disable_check_xsrf = get_etcd_value('/jupyterlab/disable_check_xsrf', 'False').lower() == 'true'

c = get_config()

c.ServerApp.base_url = base_url
c.ServerApp.ip = ip
c.ServerApp.port = port
c.ServerApp.allow_root = allow_root
c.ServerApp.password = password
c.ServerApp.root_dir = root_dir
c.ServerApp.certfile = certfile
c.ServerApp.keyfile = keyfile
c.ServerApp.use_https = use_https
c.ServerApp.disable_check_xsrf = disable_check_xsrf

# Additional security settings
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

c.ServerApp.session_idle_timeout = 600  # 10 minute session timeout

from jupyter_server.auth import passwd_check_rate_limiter
c.ServerApp.password_check_rate_limiter = passwd_check_rate_limiter(limit=5, period=3600)  # 5 attempts per hour limit

c.ServerApp.allow_origin = 'http://localhost:8888'
