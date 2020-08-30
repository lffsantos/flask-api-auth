from json import dumps

from apps.messages import MSG_INVALID_DATA, MSG_FIELD_REQUIRED, MSG_INVALID_CREDENTIALS, MSG_DOES_NOT_EXIST
from apps.users.business import register_user


class TestAuth:

    def setup_method(self):
        self.data = {}
        self.CREATE_ENDPOINT = '/users'
        self.AUTH_ENDPOINT = '/auth'
        self.ENDPOINT = '/protected'

    def test_responses_ok(self, client):
        register_user(dict(full_name='auth', email='auth@auth.com', password='123456'))
        resp = client.post(
            self.AUTH_ENDPOINT,
            data=dumps(dict(email='auth@auth.com', password='123456')),
            content_type='application/json'
        )

        url = '{}'.format(self.ENDPOINT.format(1))

        token = resp.json.get('token')

        headers = {'Authorization': 'Bearer {}'.format(token)}

        resp = client.get(url, content_type='application/json', headers=headers)

        assert resp.status_code == 200
        assert resp.json.get('user') == 'auth@auth.com'

    def test_responses_exception_field_not_exist(self, client):
        resp = client.post(
            self.AUTH_ENDPOINT,
            data=dumps(dict(password='123456')),
            content_type='application/json'
        )

        assert resp.status_code == 422
        assert resp.json.get('message') == MSG_INVALID_DATA
        assert resp.json.get('errors').get('email')[0] == MSG_FIELD_REQUIRED

    def test_responses_invalid_password(self, client):
        register_user(dict(full_name='user', email='user@user.com', password='123456'))
        resp = client.post(
            self.AUTH_ENDPOINT,
            data=dumps(dict(email='user@user.com', password='12342222')),
            content_type='application/json'
        )

        assert resp.status_code == 401
        assert resp.json.get('message') == MSG_INVALID_CREDENTIALS

    def test_responses_user_not_exists(self, client):
        resp = client.post(
            self.AUTH_ENDPOINT,
            data=dumps(dict(email='teste@user.com', password='123456')),
            content_type='application/json'
        )

        assert resp.status_code == 404
        assert resp.json.get('message') == MSG_DOES_NOT_EXIST.format('Usuário')
