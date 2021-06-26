import sys
import json
import pika
from fastapi import FastAPI
from fastapi.logger import logger
from decouple import config

sys.path.append('../module')

from manager_mq import Manager
from s3 import S3


_RABBITMQ_DEFAULT_USER = config('RABBITMQ_DEFAULT_USER')
_RABBITMQ_DEFAULT_PASS = config('RABBITMQ_DEFAULT_PASS')
_HOST = config('HOST')
_AWS_DEFAULT_REGION = config('AWS_DEFAULT_REGION')
_AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
_AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
_BUCKET_NAME = config('BUCKET_NAME')

mng = Manager(_RABBITMQ_DEFAULT_USER, _RABBITMQ_DEFAULT_PASS, _HOST)
channel = mng.channel()
#mng.declare_exchange('notification', 'direct')
#mng.create_queue('notification')

app = FastAPI(debug=True)

async def callback(ch, method, properties, body):
    notification = json.dumps(json.loads(body))
    ch.basic_act(delivery_tag = method.delivery_tag)
    s3 = S3('s3', _AWS_DEFAULT_REGION, _AWS_ACCESS_KEY_ID, _AWS_SECRET_ACCESS_KEY)
    latest = s3.get_latest_created_file(_BUCKET_NAME)
    last_id = int(latest['Key'].split('.')[0])
    id = last_id + 1
    name = str(id)+'.json'
    obj = s3.save_object(_BUCKET_NAME, name, notification)
    return obj

mng.basic_qos(1)
mng.basic_consume(queue_name='notification', callback=callback)
mng.consuming()
