ARG BASE_IMAGE
ARG FROM=rayproject/ray:nightly"$BASE_IMAGE"
FROM "$FROM"

ARG REQUIREMENT_PATH=.
ARG DOCKER_REQUIREMENT_PATH=.
ARG ML_REQUIREMENT_PATH=.
ARG SCRIPT_PATH=.

# We have to uninstall wrapt this way for Tensorflow compatibility
COPY ${REQUIREMENT_PATH}/requirements.txt ./
COPY ${REQUIREMENT_PATH}/requirements_compiled.txt ./
COPY ${ML_REQUIREMENT_PATH}/dl-cpu-requirements.txt ./
COPY ${ML_REQUIREMENT_PATH}/dl-gpu-requirements.txt ./
COPY ${DOCKER_REQUIREMENT_PATH}/ray-docker-requirements.txt ./
COPY ${ML_REQUIREMENT_PATH}/core-requirements.txt ./
COPY ${ML_REQUIREMENT_PATH}/data-requirements.txt ./
COPY ${ML_REQUIREMENT_PATH}/rllib-requirements.txt ./
COPY ${ML_REQUIREMENT_PATH}/rllib-test-requirements.txt ./
COPY ${ML_REQUIREMENT_PATH}/tune-requirements.txt ./
COPY ${ML_REQUIREMENT_PATH}/tune-test-requirements.txt ./
COPY ${ML_REQUIREMENT_PATH}/train-requirements.txt ./
COPY ${ML_REQUIREMENT_PATH}/train-test-requirements.txt ./

COPY ${SCRIPT_PATH}/install-ml-docker-requirements.sh ./

RUN sudo chmod +x install-ml-docker-requirements.sh && ./install-ml-docker-requirements.sh

# Export installed packages
RUN $HOME/anaconda3/bin/pip freeze > /home/ray/pip-freeze.txt

# Make sure tfp is installed correctly and matches tf version.
RUN python -c "import tensorflow_probability"
