c = get_config()

# Set the base URL
c.ServerApp.base_url = '/'

# Set the IP address to localhost
c.ServerApp.ip = '127.0.0.1'

# Do not open a browser automatically
c.ServerApp.open_browser = False

# Set the port
c.ServerApp.port = 8888

# Allow root user (if absolutely necessary)
c.ServerApp.allow_root = True

# Set a hashed password
c.ServerApp.password = 'argon2:$argon2id$v=19$m=10240,t=10,p=8$xMPnfpR4mpA6V7zN3jIBSA$92WT4iExe4Sxj7PZtWLsXQxcx5eZOuVFgT3WZdVmmFY'

# Set the notebook directory
c.ServerApp.root_dir = '/app/notebooks'

# Use SSL certificate and key
c.ServerApp.certfile = '/home/appuser/ssl_cert/localhost.pem'
c.ServerApp.keyfile = '/home/appuser/ssl_cert/localhost.key'

# Enable HTTPS
c.ServerApp.use_https = True

# Additional security settings
# Disable terminal access to avoid potential security risks
c.ServerApp.disable_check_xsrf = False

# Enable Content Security Policy
c.ServerApp.csp = "default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self'"

# Set a stricter HTTP Content Security Policy (CSP)
c.ServerApp.tornado_settings = {
    'headers': {
        'Content-Security-Policy': "default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self'; connect-src 'self';"
    }
}

# Set session timeout
c.ServerApp.session_idle_timeout = 600  # in seconds, here 10 minutes

# Enable X-XSS-Protection
c.ServerApp.tornado_settings['headers']['X-XSS-Protection'] = '1; mode=block'

# Enable X-Content-Type-Options
c.ServerApp.tornado_settings['headers']['X-Content-Type-Options'] = 'nosniff'

# Enforce HTTPS and secure cookies
c.ServerApp.tornado_settings['headers']['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains; preload'
c.ServerApp.tornado_settings['cookie_options'] = {'secure': True, 'httponly': True}

# Rate limiting to prevent brute force attacks
from jupyter_server.auth import passwd_check_rate_limiter
c.ServerApp.password_check_rate_limiter = passwd_check_rate_limiter(limit=5, period=3600)  # 5 attempts per hour

# Allow connections only from localhost
c.ServerApp.allow_origin = 'http://localhost:8888'

# Hide server information from HTTP responses
c.ServerApp.tornado_settings['headers']['Server'] = ''
