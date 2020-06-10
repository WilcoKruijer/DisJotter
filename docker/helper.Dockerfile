FROM jupyter/base-notebook

USER root

EXPOSE 8888

WORKDIR /src/

COPY ./disjotter/helper/helper_requirements.txt /src/disjotter/helper/helper_requirements.txt
COPY ./docker/helper_dummy/ /src/

RUN pip install -r /src/disjotter/helper/helper_requirements.txt && \
    conda env update --quiet --file environment.yml --name base


USER $NB_UID

COPY ./disjotter/ /src/disjotter/

ENTRYPOINT python -m disjotter