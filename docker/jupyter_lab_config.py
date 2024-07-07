c = get_config()

# Set the base URL
c.ServerApp.base_url = '/'

# Set the IP address
c.ServerApp.ip = '0.0.0.0'

# Do not open a browser
c.ServerApp.open_browser = False

# Set the port
c.ServerApp.port = 8888

# Allow root user
c.ServerApp.allow_root = True

# Set a password instead of using a token
c.ServerApp.password = 'argon2:$argon2id$v=19$m=10240,t=10,p=8$xMPnfpR4mpA6V7zN3jIBSA$92WT4iExe4Sxj7PZtWLsXQxcx5eZOuVFgT3WZdVmmFY'

# Set the notebook directory
c.ServerApp.root_dir = '/app/notebooks'

# Use SSL certificate and key
c.ServerApp.certfile = '/home/appuser/ssl_cert/localhost.pem'
c.ServerApp.keyfile = '/home/appuser/ssl_cert/localhost.key'

# Enable HTTPS
c.ServerApp.use_https = True
