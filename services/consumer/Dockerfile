  
FROM python:3

ENV PYTHONUNBUFFERED=1

WORKDIR /usr/src/app

COPY requirements.txt ./

COPY requirements-dev.txt ./

COPY publisher.py ./usr/src/app

RUN cd /usr/src/app

RUN pip install --no-cache-dir -r requirements.txt

# CMD ["uvicorn consumer:app --port 8001 --reload"]
RUN uvicorn consumer:app --reload --port 8000