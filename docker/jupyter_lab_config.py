c = get_config() 

c.NotebookApp.certfile = u'/home/appuser/.jupyter/localhost.pem'
c.NotebookApp.keyfile = u'/home/appuser/.jupyter/localhost.key'
c.NotebookApp.ip = '0.0.0.0'
c.NotebookApp.open_browser = False
c.NotebookApp.allow_root = True
