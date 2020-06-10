FROM jupyter/base-notebook

USER root

EXPOSE 8888

WORKDIR /src/

COPY ./disjotter/helper_requirements.txt /src/disjotter/helper_requirements.txt
COPY ./disjotter/setup.py /src/disjotter/setup.py
COPY ./docker/helper_dummy/ /src/

RUN pip install -r /src/disjotter/helper_requirements.txt && \
    pip install -r /src/requirements.txt && \
    pip install -e /src/disjotter


USER $NB_UID

COPY . /src/

ENTRYPOINT python -m disjotter