# Docker
## Prerequisites
You should install [Docker](https://docs.docker.com/desktop/) on your machine.

## Getting Started
1. In your terminal, run the Docker container:
```
docker run -p 8888:8888 elijun831/qiskit-on-docker:1.0.0
```

2. After running the Docker container, you should see a URL in the terminal output as following:
```
To access the server, open this file in a browser:
    file:///root/.local/share/jupyter/runtime/jpserver-1-open.html
Or copy and paste one of these URLs:
    https://127.0.0.1:8888/lab?token=token#
```
Go to ```https://127.0.0.1:8888``` in your browser. Make sure to include ```https```!

3. View and verify a website’s digital certificate in your web browser. Check [this guide](https://www.idownloadblog.com/2020/01/21/how-to-view-digital-certificates-safari-firefox-chrome/) for more information.

4. Copy and paste ```token#``` into your Jupyter login webpage to access the Jupyter Notebook server.
