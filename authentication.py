import requests

# Docker Hub authentication token
docker_hub_token = ''

# Request a token from Docker Hub
def login(username, password):
  try:
    url = 'https://hub.docker.com/v2/users/login/'
    data = {'username': username, 'password': password}
    response = requests.post(url, data=data)
    docker_hub_token = response.json()['token']
    return True
  except:
    return False