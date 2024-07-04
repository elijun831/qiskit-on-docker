# Import the necessary modules
from notebook.auth import passwd
import os

# Get configuration object
c = get_config()

# Set the default password (hashed)
c.NotebookApp.password = passwd(os.environ.get('JUPYTER_PASSWORD', 'password'))  # Replace 'password' with your desired password

# Disable token-based authentication
c.NotebookApp.token = ''

# Disable opening the browser by JupyterLab
c.NotebookApp.open_browser = False

# Set the notebook directory
c.NotebookApp.notebook_dir = '/app/notebooks'
