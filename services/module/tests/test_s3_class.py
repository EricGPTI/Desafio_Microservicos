import boto3
from decouple import config
import json
import sys

sys.path.append('services/module')

from s3 import S3

_AWS_DEFAULT_REGION = config('AWS_DEFAULT_REGION')
_AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
_AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
_BUCKET_NAME = config('BUCKET_NAME')


s3_resource = S3('s3', _AWS_DEFAULT_REGION, _AWS_ACCESS_KEY_ID, _AWS_SECRET_ACCESS_KEY)


def test_s3_list_buckets():
    buckets = s3_resource.list_buckets()
    assert isinstance(buckets, list)


def test_save_object():
    message = {
        'message': 'Teste Salvo'
    }
    body = json.dumps(message)
    latest = s3_resource.get_latest_created_file(_BUCKET_NAME)
    last_id = int(latest['Key'].split('.')[0])
    id = last_id + 1
    name = str(id) + '.json'
    obj = s3_resource.save_object(_BUCKET_NAME, name, body)
    new_latest = s3_resource.get_latest_created_file(_BUCKET_NAME)['Key'].split('.')[0]
    assert new_latest == str(id)


