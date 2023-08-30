from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# def test_create_user_successful():
#     user_data = {
#         "username": "testuser1",
#         "email": "test@example.cm",
#         "password": "testpassword"
#     }
#     response = client.post('/register', json=user_data)
#     assert response.status_code == 201
#     response_data = response.json()
#     assert response_data == {"message": "User registered successfully"}

access_token = None


def test_user_login():
    global access_token
    user_data = {
        "username": "testuser1",
        "password": "testpassword"
    }
    response = client.post('/login', data=user_data)
    assert response.status_code == 200
    access_token = response.json().get("access_token")


def test_user_login_invalid_user():
    user_data = {
        "username": "invaliduser",
        "password": "testpassword"
    }
    response = client.post('/login', data=user_data)
    assert response.status_code == 404


def test_get_all_posts():
    global access_token
    print(access_token)
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    query = '''
    query Posts {
    posts {
        id
        title
        content
        created_at
        updated_at
    }
    }
    '''
    data = {
        "query": query
    }

    response = client.post('/', headers=headers, json=data)
    print(response.json())
    assert response.status_code == 200


def test_get_post_by_id():
    global access_token
    print(access_token)
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    query = '''
    query Post {
    post(id: 1) {
        id
        title
        content
        created_at
        updated_at
    }
}

    '''
    data = {
        "query": query
    }
    response = client.post('/', headers=headers, json=data)
    print(response.json())
    assert response.status_code == 200
