FROM jupyter/base-notebook

USER root
RUN apt update && apt autoclean -y && apt autoremove -y && apt upgrade -y && apt install gcc python3-dev libgl1-mesa-glx ffmpeg libsm6 libxext6  -y \
&& apt-get install -y --no-install-recommends openssh-server \
&& echo "root:Docker!" | chpasswd


EXPOSE 8888



RUN pip install matplotlib docker #open3d laserchicken

COPY docker/helper_dummy/classifiers.ipynb /home/jovyan/work


COPY . src
WORKDIR src
RUN python setup.py install
RUN jupyter serverextension enable --py fair-cells
RUN jupyter nbextension install --py fair-cells
RUN jupyter nbextension enable fair-cells  --py
WORKDIR ../
RUN rm -r src

ENV SSH_PORT 2222
EXPOSE 2222 8080

# configure startup
RUN mkdir -p /tmp
COPY sshd_config /etc/ssh/

COPY ssh_setup.sh /tmp
RUN chmod -R +x /tmp/ssh_setup.sh \
   && (sleep 1;/tmp/ssh_setup.sh 2>&1 > /dev/null) \
   && rm -rf /tmp/*

ENV PORT 8080
ENV SSH_PORT 2222
EXPOSE 2222 8080


COPY init_container.sh /tmp/
RUN chmod 755 /tmp/init_container.sh
ENTRYPOINT ["/opt/startup/init_container.sh"]

# ENTRYPOINT jupyter notebook -y --port=8888 --no-browser --allow-root --debug

#
#ENTRYPOINT cd /src && \
#           python setup.py install &&\
#           jupyter serverextension enable --py fair-cells && \
#           jupyter nbextension install --py fair-cells && \
#           jupyter nbextension enable fair-cells  --py && \
#
#           jupyter notebook -y --port=8888 --no-browser --allow-root --debug
