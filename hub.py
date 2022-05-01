import requests
from authentication import getToken

# Get all images from a repository
def getRepositoryImages(repository):
  # Split the repository name
  repository = repository.split('/')
  NAMESPACE = repository[0]
  REPOSITORY = repository[1]

  # Request the repository images
  url = 'https://hub.docker.com/v2/namespaces/' + NAMESPACE + '/repositories/' + REPOSITORY + '/images'
  url += '?status=active&currently_tagged=true&ordering=last_activity&page_size=100'
  headers = {'Authorization': 'Bearer ' + getToken()}
  response = requests.get(url, headers=headers)
  return response.json()['results']
