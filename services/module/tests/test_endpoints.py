import requests
from decouple import config
from fastapi.testclient import TestClient
from publisher.publisher import app

_USERNAME = config('USERNAME')
_PASSWORD = config('PASSWORD')

client = TestClient(app)

class TestApi:
    headers = {'username': _USERNAME, 'password': _PASSWORD}
    url = 'http://127.0.0.1:8000/api/notifications/'


    def test_get_status_code_200(self, id):
        response = client.get(self.url + id, headers=self.headers)
        assert response.status_code == 200


    def test_post_notification_status_code(self, notification):
        response = client.post(self.url, headers=self.headers, data=notification)
        assert response.status_code == 201
