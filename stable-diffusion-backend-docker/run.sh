#!/bin/bash

# https://github.com/siutin/stable-diffusion-webui-docker

SDHOME=/sn640/ai-apps/stable-diffusion

mkdir -p ${SDHOME}/models
mkdir -p ${SDHOME}/outputs

chmod -R 777 ${SDHOME}

# siutin/stable-diffusion-webui-docker:latest-cuda
# stable-diffusion-web-api-change-model \
docker run -d --name sdw --gpus all --restart=unless-stopped \
  -v ${SDHOME}/models:/app/stable-diffusion-webui/models \
  -v ${SDHOME}/outputs:/app/stable-diffusion-webui/outputs \
  -p 8085:7860 \
  stable-diffusion-web-api-change-model \
  bash webui.sh --listen --no-half --no-half-vae --xformers --api

# docker stop sdw && docker rm sdw && docker image rm stable-diffusion-web-api-change-model
# docker build . -t stable-diffusion-web-api-change-model
