FROM python:3.9.1 as builder

WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
COPY requirements.txt .

RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r requirements.txt

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
COPY --from=builder /usr/src/app/wheels /wheels
COPY --from=builder /usr/src/app/requirements.txt .
RUN pip install --no-cache /wheels/*

# set work directory
WORKDIR /usr/src/app


COPY ./entrypoint.sh /usr/src/app/entrypoint.sh

COPY * /usr/src/app/

RUN mkdir  ./logs/
RUN chmod +rwx ./logs/
ENV PYTHONPATH "${PYTHONPATH}:/usr/src/app"
RUN chmod +x /usr/src/app/entrypoint.sh
#RUN ["chmod", "+x", "/usr/src/app/entrypoint.sh"]
ENTRYPOINT ["sh", "/usr/src/app/entrypoint.sh"]