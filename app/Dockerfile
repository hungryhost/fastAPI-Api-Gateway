FROM python:3.9.1 as builder

WORKDIR /usr/src/gateway-app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
COPY requirements.txt .

RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/gateway-app/wheels -r requirements.txt

# setup cron

#########
# FINAL #
#########

# pull official base image
FROM python:3.9.1

# installing netcat (nc) since we are using that to listen to postgres server in entrypoint.sh
RUN apt-get update && apt-get install -y --no-install-recommends netcat && \
    apt-get autoremove -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# install dependencies
COPY --from=builder /usr/src/gateway-app/wheels /wheels
COPY --from=builder /usr/src/gateway-app/requirements.txt .
RUN pip install --no-cache /wheels/*

# set work directory
WORKDIR /usr/src/gateway-app


COPY ./entrypoint.sh /usr/src/gateway-app/entrypoint.sh

COPY ./app .

RUN mkdir  ./logs/
RUN chmod +rwx ./logs/

RUN chmod +x /usr/src/gateway-app/entrypoint.sh
#RUN ["chmod", "+x", "/usr/src/gateway-app/entrypoint.sh"]
ENTRYPOINT ["sh", "/usr/src/gateway-app/entrypoint.sh"]