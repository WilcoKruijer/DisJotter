FROM jupyter/base-notebook

USER root

EXPOSE 8888

WORKDIR /notebooks/

COPY ./disjotter/requirements.txt /src/disjotter/requirements.txt
COPY ./disjotter/setup.py /src/disjotter/setup.py
COPY ./docker/jupyter_config/ /home/$NB_USER/.jupyter

RUN pip install -r /src/disjotter/requirements.txt && \
    pip install -e /src/disjotter && \
    mkdir -p /usr/local/share/jupyter/nbextensions && \
    mkdir -p /src/disjotter/disjotter/frontend/ && \
    ln -sfT /src/disjotter/disjotter/frontend/ /usr/local/share/jupyter/nbextensions/disjotter


# TODO: We would rather not run as root.
# https://vitorbaptista.com/how-to-access-hosts-docker-socket-without-root
# USER $NB_UID

COPY . /src/

ENTRYPOINT jupyter notebook -y --port=8888 --no-browser --allow-root
