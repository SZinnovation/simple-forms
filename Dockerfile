# Currently unused
# Copied from https://hub.docker.com/_/python/
FROM python:3.6-stretch

RUN apt-get update && apt-get install -y \
    nginx \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/sf_app

COPY sf_app .
# this is inefficient, would be better to have a requirements files that we copy over first
RUN pip install --no-cache-dir -e .

# Copy our rendered files into /var/www/html
COPY rendered /var/www/html
CMD [ "sf_app" ]