![Upload Python Package](https://github.com/QCDIS/FAIRCells/workflows/Upload%20Python%20Package/badge.svg)
# FAIR-Cells

FAIR-Cells is a Jupyter Notebook extension that allows the user to interactively create a Docker image from a Jupyter Notebook. Our tool can be used to generate Docker images from single cells of a Jupyter Notebook. The generated image will run a web service that will output the specified cell. This includes image outputs like plots. Code introspection for Python enables the services to change cell output at service run-time.

 
 [![FAIR-Cells Demo](https://raw.githubusercontent.com/QCDIS/FAIRCells/master/images/Screenshot%20from%202020-11-12%2013-17-47.png)](https://player.vimeo.com/video/478435713 "FAIR-Cells Demo")



Among other things, FAIR-Cells is useful for reusing notebook components in workflows that support web services. 

... More information to follow ...


## Installation
FAIR-Cells can be downloaded using pip. It then needs to be enabled using three Jupyter commands. Docker is required for the extension 
 to have any effect.
 
 Optionally, you may want to set up a virtual python environment:
 
```bash
$ python3 -m venv venv
$ source ./venv/bin/activate
```

```bash
$ [sudo] pip install jupyter --user
$ [sudo] pip install fair-cells --user
$ jupyter serverextension enable --py fair-cells --user
$ jupyter nbextension install --py fair-cells --user
$ jupyter nbextension enable fair-cells --user --py
```
Start jupyter notebook with:

```bash
$ jupyter notebook
```
You can now open http://localhost:8888 

## Run with Docker
```bash
docker run -it -p 8888:8888  -e GEN_CERT=yes -v /var/run/docker.sock:/var/run/docker.sock qcdis/fair-cells 
```

## Development
To keep your system clean it is recommended to develop using Docker. The following command will run a Jupyter Notebook 
server with FAIR-Cells enabled at http://localhost:8888. Autoreload is enabled for Python files, you will need to reload 
your browser to see changes in the front-end.

```bash
$ docker-compose up --build main
```

To test the helper server that runs inside of the container run the following command. This uses a dummy notebook that 
can be found in `docker/helper_dummy`. The notebook will be available at http://localhost:10000

```bash
$ docker-compose up --build helper
```


## Tutorial 

Make sure you have Docker installed. To verify you may run:
```bash
$ [sudo] docker run hello-world
```

Start the docker container with jupyter and FAIR-Cells enabled:
```bash
docker run -it -p 8888:8888  -v /var/run/docker.sock:/var/run/docker.sock qcdis/fair-cells:develop-snapshot
```

In your output you will see something similar to this:
```bash
[D 16:27:28.614 NotebookApp] Searching ['/home/jovyan', '/home/jovyan/.jupyter', '/opt/conda/etc/jupyter', '/usr/local/etc/jupyter', '/etc/jupyter'] for config files
[D 16:27:28.615 NotebookApp] Looking for jupyter_config in /etc/jupyter
[D 16:27:28.615 NotebookApp] Looking for jupyter_config in /usr/local/etc/jupyter
[D 16:27:28.615 NotebookApp] Looking for jupyter_config in /opt/conda/etc/jupyter
[D 16:27:28.616 NotebookApp] Looking for jupyter_config in /home/jovyan/.jupyter
[D 16:27:28.616 NotebookApp] Looking for jupyter_config in /home/jovyan
[D 16:27:28.617 NotebookApp] Looking for jupyter_notebook_config in /etc/jupyter
[D 16:27:28.618 NotebookApp] Loaded config file: /etc/jupyter/jupyter_notebook_config.py
[D 16:27:28.618 NotebookApp] Looking for jupyter_notebook_config in /usr/local/etc/jupyter
[D 16:27:28.618 NotebookApp] Looking for jupyter_notebook_config in /opt/conda/etc/jupyter
[D 16:27:28.618 NotebookApp] Looking for jupyter_notebook_config in /home/jovyan/.jupyter
[D 16:27:28.619 NotebookApp] Loaded config file: /home/jovyan/.jupyter/jupyter_notebook_config.py
[D 16:27:28.619 NotebookApp] Loaded config file: /home/jovyan/.jupyter/jupyter_notebook_config.json
[D 16:27:28.620 NotebookApp] Looking for jupyter_notebook_config in /home/jovyan
[D 16:27:28.626 NotebookApp] Paths used for configuration of jupyter_notebook_config: 
    	/etc/jupyter/jupyter_notebook_config.json
[D 16:27:28.627 NotebookApp] Paths used for configuration of jupyter_notebook_config: 
    	/usr/local/etc/jupyter/jupyter_notebook_config.json
[D 16:27:28.628 NotebookApp] Paths used for configuration of jupyter_notebook_config: 
    	/opt/conda/etc/jupyter/jupyter_notebook_config.d/jupyterlab.json
    	/opt/conda/etc/jupyter/jupyter_notebook_config.json
[D 16:27:28.629 NotebookApp] Paths used for configuration of jupyter_notebook_config: 
    	/home/jovyan/.jupyter/jupyter_notebook_config.json
[I 16:27:28.721 NotebookApp] Writing notebook server cookie secret to /home/jovyan/.local/share/jupyter/runtime/notebook_cookie_secret
[I 16:27:29.335 NotebookApp] FAIR-Cells loaded.
[I 16:27:29.892 NotebookApp] JupyterLab extension loaded from /opt/conda/lib/python3.8/site-packages/jupyterlab
[I 16:27:29.892 NotebookApp] JupyterLab application directory is /opt/conda/share/jupyter/lab
[I 16:27:29.896 NotebookApp] Serving notebooks from local directory: /home/jovyan
[I 16:27:29.896 NotebookApp] Jupyter Notebook 6.1.5 is running at:
[I 16:27:29.896 NotebookApp] http://589d485a459b:8888/?token=705e9dc1f39c581a74e4d616e7f699992de0c0697fa9da46
[I 16:27:29.896 NotebookApp]  or http://127.0.0.1:8888/?token=705e9dc1f39c581a74e4d616e7f699992de0c0697fa9da46
[I 16:27:29.896 NotebookApp] Use Control-C to stop this server and shut down all kernels (twice to skip confirmation).
[C 16:27:29.900 NotebookApp] 
    
    To access the notebook, open this file in a browser:
        file:///home/jovyan/.local/share/jupyter/runtime/nbserver-1-open.html
    Or copy and paste one of these URLs:
        http://589d485a459b:8888/?token=705e9dc1f39c581a74e4d616e7f699992de0c0697fa9da46
     or http://127.0.0.1:8888/?token=705e9dc1f39c581a74e4d616e7f699992de0c0697fa9da46
```

With your browser (preferably chrome or chromium) open http://127.0.0.1:8888/?token=<TOKEN> .

You may find the token in the output of the docker container. In this case the token is 705e9dc1f39c581a74e4d616e7f699992de0c0697fa9da46 
for you, it may be different. 

