#!/bin/bash 


usr/bin/tensorflow_model_server --port=8500 --rest_api_port=8501 --model_name=${MODEL_NAME} --model_base_path=${MODEL_BASE_PATH}/${MODEL_NAME} "$@" 

PID=`ps -A | grep tensorflow_mode | awk '//{print $1}'`
reredirect -m /sagemaker/gelf_fifo $PID
