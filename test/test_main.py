import pytest as pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


@pytest.fixture
def auth_headers():
    global access_token
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    return headers


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
post_id = None


def test_user_login():
    global access_token
    user_data = {
        "username": "user1",
        "password": "password1"
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


def test_get_all_posts(auth_headers):
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

    response = client.post('/', headers=auth_headers, json=data)
    assert response.status_code == 200


def test_get_post_by_id(auth_headers):
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
    response = client.post('/', headers=auth_headers, json=data)
    assert response.status_code == 200


def test_create_post(auth_headers):
    global post_id
    query = '''
    mutation CreatePost {
    createPost(title: "new post", content: "content") {
        success
        message
        post {
            id
            title
            content
            created_at
            updated_at
        }
        }
        }

    '''

    data = {
        "query": query
    }
    response = client.post('/', headers=auth_headers, json=data)
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["data"]["createPost"]["success"] == True
    created_post = response_json["data"]["createPost"]["post"]
    post_id = created_post["id"]


def test_delete_valid_post(auth_headers):
    global post_id
    query = f'''mutation DeletePost {{
        deletePost(id: {post_id}) {{
            success
            message
        }}
    }}'''
    data = {
        "query": query
    }
    response = client.post('/', headers=auth_headers, json=data)
    response_json = response.json()
    assert response.status_code == 200
    assert response_json["data"]["deletePost"]["success"] is True
    assert response_json["data"]["deletePost"]["message"] == "Post deleted successfully"


def test_delete_invalid_post(auth_headers):
    global post_id
    query = f'''mutation DeletePost {{
        deletePost(id: {post_id + 1}) {{
            success
            message
        }}
    }}'''

    data = {
        "query": query
    }
    response = client.post('/', headers=auth_headers, json=data)
    response_json = response.json()
    assert response.status_code == 200
    assert response_json["data"]["deletePost"]["success"] is False
    assert response_json["data"]["deletePost"]["message"] == "Post not found"


def test_delete_unauthorized_post(auth_headers):
    global post_id
    query = f'''mutation DeletePost {{
        deletePost(id: 50) {{
            success
            message
        }}
    }}'''

    data = {
        "query": query
    }
    response = client.post('/', headers=auth_headers, json=data)
    response_json = response.json()
    assert response_json["data"]["deletePost"]["success"] is False
    assert response_json["data"]["deletePost"]["message"] == "You are not authorized to delete this post"
