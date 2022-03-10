# OS
FROM alpine:3.15

# ARGUMENTS
ARG GITLAB_HOST=https://gitlab.com
ARG GITLAB_TOKEN=''
ARG GROUP_ID=1

# ENV VARIABLES
ENV GITLAB_HOST=$GITLAB_HOST
ENV GITLAB_TOKEN=$GITLAB_TOKEN
ENV GROUP_ID=$GROUP_ID
ENV PYTHONWARNINGS="ignore:Unverified HTTPS request"
ENV APP_ROOT=/var/run

RUN mkdir -p /root/.ssh/
RUN mkdir -p ${APP_ROOT}

USER root

WORKDIR ${APP_ROOT}

COPY . ${APP_ROOT}

RUN apk add --update --no-cache curl python3 py-pip openssh-client git && ln -sf python3 /usr/bin/python
RUN pip install requests python-gitlab gitpython urllib3

ENTRYPOINT ["python", "run.py"]