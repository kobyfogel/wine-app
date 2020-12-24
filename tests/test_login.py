import pytest


HTTP_OK = 200
FORBIDDEN = 403


POSSIBLE_MISSING_FIELD = [
    ('', ''),
    ('BuliIshHasheleg', ''),
]


class TestLogin:
    LOGIN_PAGE = '/login'
    BAD_MESSAGE = b'unsuccessfull'
    MISSING_FIELDS = b'missing'

    @staticmethod
    def test_login_returns_ok(client):
        assert client.get(TestLogin.LOGIN_PAGE).status_code == HTTP_OK

    @staticmethod
    @pytest.mark.parametrize("username,password", POSSIBLE_MISSING_FIELD)
    def test_login_fields_are_empty(client, username, password):
        data = {'username': username, 'password': password}
        assert TestLogin.MISSING_FIELDS in client.post('/login', data=data).data

    @staticmethod
    def test_login_details_are_absolutly_wrong(client):
        data = {
            'username': 'BuliIshHasheleg',
            'password': '12345',
        }
        assert TestLogin.BAD_MESSAGE in client.post('/login', data=data).data

    @staticmethod
    def test_login_password_is_wrong(client, user):
        data = {
            'username': 'admin',
            'password': 'admin111',
        }
        assert TestLogin.BAD_MESSAGE in client.post('/login', data=data).data
        
    @staticmethod
    def test_login_successfully(client, user):
        data = {
            'username': 'admin',
            'password': 'admin',
        }
        assert TestLogin.BAD_MESSAGE not in client.post('/login', data=data).data
