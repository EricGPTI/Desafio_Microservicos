import types
from decouple import config
import sys
import time
import json
from pytest import mark

sys.path.append('services/module')

from manager_mq import Manager

_RABBITMQ_DEFAULT_USER = config('RABBITMQ_DEFAULT_USER')
_RABBITMQ_DEFAULT_PASS = config('RABBITMQ_DEFAULT_PASS')
_HOST = config('HOST')

mng = Manager(_RABBITMQ_DEFAULT_USER, _RABBITMQ_DEFAULT_PASS, _HOST)

def test_create_queue():
    queue = mng.create_queue('test')
    queue_name = queue.method.queue
    assert queue_name == 'test'
    
    time.sleep(5)
    mng.channel().queue_delete('test')


@mark.consuming
def test_consuming_message():
    message = 'Este é um teste'
    queue = mng.create_queue('test')
    name = queue.method.queue
    mng.declare_exchange(exchange='test', types='topic')
    mng.channel().queue_bind('test', 'test')
    mng.publish_message('test', 'test', message)
    

    def callback(ch, method, properties, body):
        ch.basic_act(delivery_tag = method.delivery_tag)
        callback_body = json.dumps(json.loads(body))
        print(type(callback_body))
        print(callback_body)
        assert callback_body == 'Este é um teste'

    mng.basic_consume(name, callback=callback)
    mng.channel().queue_delete('test')


