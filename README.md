# Qiskit-on-docker: A Qiskit and Quantum Computing Docker Environment

## About
This Dockerized environment sets up JupyterLab with a comprehensive suite of Qiskit and quantum computing-related Python packages, ensuring a robust setup for research and development. The Dockerfile not only installs essential dependencies and configures JupyterLab but also automatically generates SSL certificates, allowing JupyterLab to run in a secure HTTPS environment. Docker Compose simplifies service orchestration, while Poetry manages all Python dependencies efficiently. This configuration provides a secure, convenient, and fully-equipped environment for quantum computing projects.

## Prerequisites
You should install [Docker](https://docs.docker.com/desktop/) on your machine.

## Getting Started
1. In your terminal on your machine, run the Docker container:
```
docker run -p 8888:8888 elijun831/qiskit-on-docker:1.0.0
```

2. After running the Docker container, you should see a URL in the terminal output that looks like this:
```
To access the server, open this file in a browser:
    file:///root/.local/share/jupyter/runtime/jpserver-1-open.html
Or copy and paste one of these URLs:
    https://1b296314e2a4:8888/lab?token=[[token]]
    https://127.0.0.1:8888/lab?token=[[token]]
``` 
Copy the [[token]] and paste it into your Jupyter login webpage to access the Jupyter Notebook server.

## References for Learning Qiskit
- [IBM Quantum Experience](https://quantum-computing.ibm.com/)
- [IBM Quantum Learning](https://learning.quantum.ibm.com)
- [Qiskit GitHub Repository](https://github.com/Qiskit)
- [Qiskit YouTube Channel](https://www.youtube.com/Qiskit)
