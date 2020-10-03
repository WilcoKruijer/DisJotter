FROM jupyter/base-notebook

USER root

EXPOSE 8888

COPY . src
RUN pip install jupyter
#RUN pip install fair-cells
WORKDIR src
RUN python setup.py install
RUN jupyter serverextension enable --py fair-cells
RUN jupyter nbextension install --py fair-cells
RUN jupyter nbextension enable fair-cells  --py
WORKDIR ../
RUN rm -r src

ENTRYPOINT jupyter notebook -y --port=8888 --no-browser --allow-root
