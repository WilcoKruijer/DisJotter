FROM jupyter/base-notebook

USER root

RUN apt update && apt upgrade -y && apt autoclean -y && apt autoremove -y


EXPOSE 8888

WORKDIR /src/

COPY ./fair-cells/helper/helper_requirements.txt /src/fair-cells/helper/helper_requirements.txt
COPY ./docker/helper_dummy/ /src/


RUN pip install --use-feature=2020-resolver -r /src/fair-cells/helper/helper_requirements.txt
RUN conda env update --quiet --file environment.yml --name base


USER $NB_UID

COPY ./fair-cells/ /src/fair-cells/

ENTRYPOINT python -m fair-cells