import requests

# Request a token from Docker Hub
def login(username, password):
  url = 'https://hub.docker.com/v2/users/login/'
  data = {'username': username, 'password': password}
  response = requests.post(url, data=data)
  return response.json()['token']