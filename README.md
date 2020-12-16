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
 docker run --privileged -e "DISPLAY=unix:0.0" -v="/tmp/.X11-unix:/tmp/.X11-unix:rw"  -it -p 8888:8888  -v /var/run/docker.sock:/var/run/docker.sock qcdis/fair-cells:develop-snapshot
```

With your browser (preferably chrome or chromium) open http://127.0.0.1:8888/


