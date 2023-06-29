# FROM siutin/stable-diffusion-webui-docker:latest-cuda
FROM siutin/stable-diffusion-webui-docker:cuda-v1.3.2-2023-06-12

COPY ./0001-enable-change-model-in-API.patch /
WORKDIR /app/stable-diffusion-webui
RUN patch -p1 < /0001-enable-change-model-in-API.patch
# docker build . -t stable-diffusion-web-api-change-model
