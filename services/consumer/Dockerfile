FROM python:3
WORKDIR /usr/src/app
COPY requirements.txt ./
COPY requirements-dev.txt ./
RUN pip install --no-cache-dir -r requirements.txt
ENV PYTHONUNBUFFERED=1
COPY consumer.py ./usr/src/app
RUN cd /usr/src/app
CMD ["uvicorn consumer:app --port 8001 --reload"]

