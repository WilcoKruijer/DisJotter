FROM jupyter/minimal-notebook
USER root
WORKDIR /src/
COPY ./fair-cells/ /src/fair-cells/
RUN pip install -r /src/fair-cells/helper/helper_requirements.txt
COPY ./environment.yml /src/environment.yml
RUN conda env update --file environment.yml --name base
USER $NB_UID
COPY ./notebook.ipynb /src/notebook.ipynb
COPY ./nb_helper_config.json /src/nb_helper_config.json
ENTRYPOINT ["python", "-m", "fair-cells"]