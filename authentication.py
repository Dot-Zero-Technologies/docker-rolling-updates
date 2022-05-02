import requests

from debug import getDebugMode, printDebugMessage

# Docker Hub authentication token
docker_hub_token = ''

# Request a token from Docker Hub
def login(username, password):
  try:
    global docker_hub_token
    url = 'https://hub.docker.com/v2/users/login/'
    data = {'username': username, 'password': password}

    # Print debug message
    printDebugMessage('Requesting token from Docker Hub for user: ' + username)

    response = requests.post(url, data=data)
    docker_hub_token = response.json()['token']

    # Print debug message
    printDebugMessage('Token received!')

    return True
  except:
    # Print debug message
    printDebugMessage('Failed to get token from Docker Hub')

    return False

# Get Docker Hub token
def getToken():
  global docker_hub_token
  return docker_hub_token