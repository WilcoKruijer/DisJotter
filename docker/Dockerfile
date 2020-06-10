FROM jupyter/base-notebook

USER root

EXPOSE 8888

WORKDIR /notebooks/

COPY ./setup.py /src/setup.py
COPY ./docker/jupyter_config/ /home/$NB_USER/.jupyter

RUN pip install -e /src/ && \
    mkdir -p /usr/local/share/jupyter/nbextensions && \
    mkdir -p /src/disjotter/frontend/ && \
    ln -sfT /src/disjotter/frontend/ /usr/local/share/jupyter/nbextensions/disjotter


# TODO: We would rather not run as root.
# https://vitorbaptista.com/how-to-access-hosts-docker-socket-without-root
# USER $NB_UID

COPY . /src/

ENTRYPOINT jupyter notebook -y --port=8888 --no-browser --allow-root
