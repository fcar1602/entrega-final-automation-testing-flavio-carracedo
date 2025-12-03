import requests

class APIClient:
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()

    def post(self, endpoint, json=None, **kwargs):
        return self.session.post(f"{self.base_url}{endpoint}", json=json, **kwargs)

    def get(self, endpoint, **kwargs):
        return self.session.get(f"{self.base_url}{endpoint}", **kwargs)
    
    def login(self, username, password):
        payload = {"username": username, "password": password}
        res = self.session.post(f"{self.base_url}/auth/login", json=payload)
        res.raise_for_status()

        self.access_token = res.json()["accessToken"]

        # Set Authorization header automatically
        self.session.headers.update({
            "Authorization": f"Bearer {self.access_token}"
        })

        return res.json()

    def get(self, endpoint):
        return self.session.get(f"{self.base_url}{endpoint}")

    def get_me(self):
        return self.session.get(f"{self.base_url}/user/me")
    
    def add_user(self, user_data):
        return self.session.post(f"{self.base_url}/users/add", json=user_data)

    def update_user(self, user_id, update_data):
        return self.session.put(f"{self.base_url}/users/{user_id}", json=update_data)

    def delete_user(self, user_id):
        return self.session.delete(f"{self.base_url}/users/{user_id}")