FROM jupyter/base-notebook

USER root

RUN pip install --upgrade pip
RUN pip install jupyter
RUN pip install fair-cells
RUN jupyter serverextension enable --py fair-cells
RUN jupyter nbextension install --py fair-cells
RUN jupyter nbextension enable fair-cells --py

EXPOSE 8888


ENTRYPOINT jupyter notebook -y --port=8888 --no-browser --allow-root
