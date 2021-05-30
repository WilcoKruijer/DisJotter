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

ENV SSH_PASSWD "root:Docker!"
RUN apt-get update \
        && apt-get install -y --no-install-recommends dialog \
        && apt-get update \
	&& apt-get install -y --no-install-recommends openssh-server \
	&& echo "$SSH_PASSWD" | chpasswd 

COPY sshd_config /etc/ssh/
COPY init.sh /usr/local/bin/
	
RUN chmod u+x /usr/local/bin/init.sh
EXPOSE 8000 2222
ENTRYPOINT ["init.sh"]

# ENTRYPOINT jupyter notebook -y --port=8888 --no-browser --allow-root --debug

#
#ENTRYPOINT cd /src && \
#           python setup.py install &&\
#           jupyter serverextension enable --py fair-cells && \
#           jupyter nbextension install --py fair-cells && \
#           jupyter nbextension enable fair-cells  --py && \
#
#           jupyter notebook -y --port=8888 --no-browser --allow-root --debug
