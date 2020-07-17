FROM jupyter/base-notebook

USER root

EXPOSE 8888

RUN pip install jupyter
RUN pip install fair-cells
RUN jupyter serverextension enable --py fair-cells 
RUN jupyter nbextension install --py fair-cells 
RUN jupyter nbextension enable fair-cells  --py

ENTRYPOINT jupyter notebook -y --port=8888 --no-browser --allow-root
