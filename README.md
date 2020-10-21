![Upload Python Package](https://github.com/QCDIS/FAIRCells/workflows/Upload%20Python%20Package/badge.svg)
# FAIR-Cells

FAIR-Cells is a Jupyter Notebook extension that allows the user to interactively create a Docker image from a Jupyter Notebook. Our tool can be used to generate Docker images from single cells of a Jupyter Notebook. The generated image will run a web service that will output the specified cell. This includes image outputs like plots. Code introspection for Python enables the services to change cell output at service run-time.

Among other things, FAIR-Cells is useful for reusing notebook components in workflows that support web services. 

... More information to follow ...


#### Installation
FAIR-Cells
 can be downloaded using pip. It then needs to be enabled using three Jupyter commands. Docker is required for the extension 
 to have any effect.

```bash
$ [sudo] pip install jupyter --user
$ [sudo] pip install fair-cells --user
$ jupyter serverextension enable --py fair-cells --user
$ jupyter nbextension install --py fair-cells --user
$ jupyter nbextension enable fair-cells --user --py
```


#### Run with Docker
```bash
docker run -it -p 8888:8888  -e GEN_CERT=yes -v /var/run/docker.sock:/var/run/docker.sock qcdis/fair-cells 
```

#### Development
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
