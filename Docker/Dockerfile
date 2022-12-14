# This build on the Sagemaker tensorflow serving containers and add the ability to copy
# logs to a GELF endpoint

# Pull the base TFS container. see: https://github.com/aws/deep-learning-containers/blob/master/available_images.md
FROM 763104351884.dkr.ecr.eu-west-1.amazonaws.com/tensorflow-inference:2.10.0-cpu-py39-ubuntu20.04-sagemaker

# Build the reredirect untility to capture the stdout/stderr of a running process using ptrace 
RUN git clone https://github.com/jerome-pouiller/reredirect.git
RUN cd reredirect; make install

# Copy accross our modified container files
COPY python_service.py ./sagemaker/python_service.py
COPY gelf_client.py /usr/bin/gelf_client.py
COPY serve* ./sagemaker/

# Add a client to copy data from a named fifo and forward to the GELF endpoint
COPY gelf_client.py ./sagemaker/
RUN pip install pygelf