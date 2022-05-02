import requests
from authentication import getToken
from debug import printDebugMessage

# Get all images from a repository
def getRepositoryImages(repository):
  # Split the repository name
  repository = repository.split('/')
  NAMESPACE = repository[0]
  REPOSITORY = repository[1]
  printDebugMessage('Getting images from repository: ' + NAMESPACE + '/' + REPOSITORY)

  # Request the repository images
  url = 'https://hub.docker.com/v2/namespaces/' + NAMESPACE + '/repositories/' + REPOSITORY + '/images'
  url += '?status=active&currently_tagged=true&ordering=last_activity&page_size=100'
  headers = {'Authorization': 'Bearer ' + getToken()}
  response = requests.get(url, headers=headers)
  printDebugMessage('Response: ' + str(response.status_code))
  return response.json()['results']

# Get images in a repository and return the latest for each tag
def getRepositoryImagesByTag(repository):
  # Fetch all current images from the repository
  images = getRepositoryImages(repository)

  # Create repo in image dictionary
  REPO_IMAGES = {}
  
  # Go through each image and get the latest
  for image in images:
    # Get the image tags
    imageTags = image['tags']
    i = 0
    while i < len(imageTags):
      # Check if the image tag is current
      if (imageTags[i]['is_current'] == False):
        # Remove the current tag
        del imageTags[i]
        i -= 1
      i += 1
    
    # Add digests to the image tags
    for tag in imageTags:
      REPO_IMAGES[tag['tag']] = image['digest']
  
  return REPO_IMAGES