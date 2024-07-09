# Import necessary modules
from jupyterhub.auth import LocalAuthenticator
from passlib.hash import sha256_crypt

# Get the configuration object
c = get_config()

# JupyterHub settings
c.JupyterHub.ip = '0.0.0.0'
c.JupyterHub.port = 8000
c.JupyterHub.ssl_key = '/home/appuser/ssl_cert/localhost.key'
c.JupyterHub.ssl_cert = '/home/appuser/ssl_cert/localhost.pem'

# Use LocalAuthenticator and allow it to create system users
c.JupyterHub.authenticator_class = 'jupyterhub.auth.LocalAuthenticator'
c.LocalAuthenticator.create_system_users = True

# Allow all users to access the Hub (remove in production)
c.Authenticator.allow_all = True

# Suppress warning about allowed users
c.Authenticator.any_allow_config = True

# Grant admin access to specific users
c.Authenticator.admin_users = {'admin'}

# Spawn single-user servers as Docker containers
c.JupyterHub.spawner_class = 'dockerspawner.DockerSpawner'

# Specify the image to use for single-user servers
c.DockerSpawner.image = 'elijun831/qiskit-on-docker:1.0.0'

# Mount the host's Docker socket in the spawned containers
c.DockerSpawner.volumes = {'/var/run/docker.sock': '/var/run/docker.sock'}

# The directory in the container where the notebook files are located
c.DockerSpawner.notebook_dir = '/app/notebooks'

# Persist hub data
c.JupyterHub.db_url = 'sqlite:///jupyterhub.sqlite'

# Use HTTPS
c.JupyterHub.ssl_key = '/home/appuser/ssl_cert/localhost.key'
c.JupyterHub.ssl_cert = '/home/appuser/ssl_cert/localhost.pem'

# Initial password setup for the admin user (replace 'password' with a secure password)
def generate_hashed_password(password):
    hashed_password = sha256_crypt.hash(password)
    return hashed_password

# Set the hashed password for notebook access
c.NotebookApp.password_required = True
c.NotebookApp.password = generate_hashed_password('qiskit')

# Print the hashed password for reference (optional)
print(f"Hashed password: {generate_hashed_password('qiskit')}")
