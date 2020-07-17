FROM jupyter/base-notebook

USER root

RUN pip install --upgrade pip
RUN pip install jupyter --user
RUN pip install fair-cells --user
RUN jupyter serverextension enable --py fair-cells --user
RUN jupyter nbextension install --py fair-cells --user
RUN jupyter nbextension enable fair-cells --user --py

EXPOSE 8888


ENTRYPOINT jupyter notebook -y --port=8888 --no-browser --allow-root
