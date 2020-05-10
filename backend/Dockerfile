FROM python:3.7

# python envs
ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100

# python dependencies
COPY ./requirements.txt /
RUN pip install -r ./requirements.txt

# Make port 8080 available for the app
#EXPOSE 8000

# upload scripts
COPY ./scripts/entrypoint.sh ./scripts/dev_start.sh ./scripts/gunicorn.sh ./scripts/gunicorn_stage.sh /

WORKDIR /backend/
