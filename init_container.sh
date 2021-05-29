#!/bin/bash
service ssh start


jupyter notebook -y --port=8888 --no-browser --allow-root --debug

