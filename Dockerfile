FROM python:3.12.3-bookworm

RUN apt update; \
 apt install -y sudo; \
 useradd --home /app -M app -K UID_MIN=10000 -K GID_MIN=10000 -s /bin/bash;\
 mkdir /app; \
 chown app:app -R /app; \
 usermod -aG sudo app; \
 echo 'app ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers

# USER app
WORKDIR /app/
ADD . /app/

RUN python3 -m pip install -r requirements.txt
CMD ["python3", "main.py"]