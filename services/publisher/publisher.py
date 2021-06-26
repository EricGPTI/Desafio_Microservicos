import sys

sys.path.append('../module')

from model.notification import Notification
from fastapi import FastAPI, status
from decouple import config
import json
from manager_mq import Manager
from s3 import S3

_RABBITMQ_DEFAULT_USER = config('RABBITMQ_DEFAULT_USER')
_RABBITMQ_DEFAULT_PASS = config('RABBITMQ_DEFAULT_PASS')
_HOST = config('HOST')
_AWS_DEFAULT_REGION = config('AWS_DEFAULT_REGION')
_AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
_AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
_BUCKET_NAME = config('BUCKET_NAME')


s3 = S3('s3', _AWS_DEFAULT_REGION, _AWS_ACCESS_KEY_ID, _AWS_SECRET_ACCESS_KEY)
mng = Manager(_RABBITMQ_DEFAULT_USER, _RABBITMQ_DEFAULT_PASS, _HOST)

channel = mng.channel()
mng.declare_exchange('notification', 'topic')
mng.create_queue('notification')

app = FastAPI(debug=True)

@app.post('/api/notifications/', status_code=status.HTTP_201_CREATED)
async def post_notification(msg: Notification):
    notice = msg.json()
    mng.publish_message('notification', 'notification', notice)
    return {'Notification': notice}


@app.get("/api/notifications/{id}")
async def get_notification(id: str):
    obj = json.loads(s3.get_object(_BUCKET_NAME, id))
    return obj
