import sys

sys.path.append('../module')

from model.rico import Rico
from fastapi import FastAPI
from decouple import config
from manager_mq import Manager

_RABBITMQ_DEFAULT_USER = config('RABBITMQ_DEFAULT_USER')
_RABBITMQ_DEFAULT_PASS = config('RABBITMQ_DEFAULT_PASS')
_HOST = config('HOST')

mng = Manager(_RABBITMQ_DEFAULT_USER, _RABBITMQ_DEFAULT_PASS, _HOST)
channel = mng.channel()
mng.declare_exchange('rico', 'topic')
mng.create_queue('rico')

app = FastAPI(debug=True)

@app.post('/ricos/')
async def post_notification(msg: Rico):
    notice = msg.json()
    mng.publish_message('rico', 'rico', notice)
    return "Sucesso"

#@app.get("/notification/{id}")
#async def get_notification(id: int):
#    return {"message": "Hello World"}
