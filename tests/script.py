import requests
import json

API_URL = "http://127.0.0.1:8000/api/"
STATUS_ENDPOINT = API_URL + "status/"
AUTH_ENDPOINT = API_URL + "auth/"
AUTH_TOKEN = ""

headers = {
    "Content-Type": "application/json"
}

def register():
    new_user = {
        "username": "thisistheboi",
        "email": "theboi@tmail.lol",
        "password": "cooldude123"
    }
    return requests.post(AUTH_ENDPOINT + "register/", data=json.dumps(new_user), headers=headers).json()

def login():
    login_data = {
        "username": "dev_ayaan",
        "password": "cooldude123"
    }
    return requests.post(AUTH_ENDPOINT, data=json.dumps(login_data), headers=headers).json()

def get_token():
    auth_user = login()
    if auth_user and auth_user.get('token'):
        return login()['token']
    print(auth_user.get('detail'))
    return ""

def create_post():
    post_data = {
        "content": "Lorem Ipsum..."
    }
    return requests.post(STATUS_ENDPOINT, data=json.dumps(post_data), headers=headers)

def update_post(post):
    post_data = {
        "content": str(post.get('content')) + " LOLL"
    }
    return requests.put(STATUS_ENDPOINT + str(post.get('id')) + "/", data=json.dumps(post_data), headers=headers)

def delete_post(post):
    return requests.delete(STATUS_ENDPOINT + str(post.get('id')) + "/", headers=headers)

""" user = register()
print(user) """

AUTH_TOKEN = get_token()

headers = {
    "Content-Type": "application/json",
    "Authorization": "JWT " + AUTH_TOKEN
}

""" post = create_post().json()
print(post) """

post = {
    'id': 30
}

updated_post = update_post(post).json()
print(updated_post)

# deleted_post = delete_post(post)