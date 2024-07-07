c = get_config()
c.ServerApp.base_url = '/'
c.ServerApp.ip = '0.0.0.0'
c.ServerApp.open_browser = False
c.ServerApp.port = 8888
c.ServerApp.allow_root = True

import secrets
c.ServerApp.token = secrets.token_hex(32)
c.ServerApp.root_dir = '/app/notebooks'
c.ServerApp.certfile = '/home/appuser/ssl_cert/localhost.pem'
c.ServerApp.keyfile = '/home/appuser/ssl_cert/localhost.key'
c.ServerApp.use_https = True
