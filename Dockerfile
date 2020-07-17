FROM jupyter/base-notebook

USER root

#RUN pip install --upgrade pip
#RUN pip install jupyter
#RUN pip install fair-cells
#RUN jupyter serverextension enable --py fair-cells
#RUN jupyter nbextension install --py fair-cells
#RUN jupyter nbextension enable fair-cells --py


COPY ./setup.py /src/setup.py
COPY ./docker/jupyter_config/ /home/$NB_USER/.jupyter

RUN pip install -e /src/ && \
    mkdir -p /usr/local/share/jupyter/nbextensions && \
    mkdir -p /src/fair-cells/frontend/ && \
    ln -sfT /src/fair-cells/frontend/ /usr/local/share/jupyter/nbextensions/fair-cells


# TODO: We would rather not run as root.
# https://vitorbaptista.com/how-to-access-hosts-docker-socket-without-root
# USER $NB_UID

COPY . /src/

EXPOSE 8888


ENTRYPOINT jupyter notebook -y --port=8888 --no-browser --allow-root
