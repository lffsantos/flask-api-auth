import json


def test_index_response_200(client):
    response = client.get('/')
    assert response.status_code == 200


def test_index_response_status(client):
    response = client.get('/')
    data = json.loads(response.data.decode('utf-8'))
    assert data['status'] == True
