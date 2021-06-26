FROM python:3
WORKDIR /usr/src/app
COPY requirements.txt ./
COPY requirements-dev.txt ./
RUN pip install --no-cache-dir -r requirements.txt
ENV PYTHONUNBUFFERED=1
COPY consumer.py ./usr/src/app
RUN cd /usr/src/app
CMD uvicorn consumer:app --port 8001 --reload


# first stage
FROM python:3.8 AS builder
COPY requirements.txt .

# install dependencies to the local user directory (eg. /root/.local)
RUN pip install --user -r requirements.txt

# second unnamed stage
FROM python:3.8-slim
WORKDIR /code

# copy only the dependencies installation from the 1st stage image
COPY --from=builder /root/.local /root/.local
COPY ./src .

# update PATH environment variable
ENV PATH=/root/.local:$PATH

CMD ["uvicorn consumer:app --port 8001 --reload"]
