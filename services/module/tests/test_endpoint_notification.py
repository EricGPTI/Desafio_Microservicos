from tests.test_endpoints import TestApi

class TestNotification:

    def test_post_status_201(self):
        notification = {
	        "notification": "Notificação de teste"
        }
        response = TestApi().test_post_notification_status_code(notification)
        assert response == 201

    def test_get_status_200(self):
        id = 5
        response = TestApi().test_get_status_code_200(id)
        assert response == 200

