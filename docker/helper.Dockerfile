FROM jupyter/base-notebook

USER root

EXPOSE 8888

WORKDIR /src/

COPY ./fair-cells/helper/helper_requirements.txt /src/fair-cells/helper/helper_requirements.txt
COPY ./docker/helper_dummy/ /src/

RUN pip install -r /src/fair-cells/helper/helper_requirements.txt && \
    conda env update --quiet --file environment.yml --name base


USER $NB_UID

COPY ./fair-cells/ /src/fair-cells/

ENTRYPOINT python -m fair-cells