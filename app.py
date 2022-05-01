from authentication import login
import os
from dotenv import load_dotenv
from docker import getContainers, getImageDigest, getRepositories
from hub import getRepositoryImagesByTag
load_dotenv()

def authenticate():
  # Authenticate with Docker Hub
  success = login(os.getenv('DOCKER_USERNAME'), os.getenv('DOCKER_PASSWORD'))

  # Check if authentication was successful
  if success: print('Authentication successful')
  else: print('Authentication failed')

  return success

# Start by authenticating with Docker Hub
if authenticate() == False: exit()

# Get all containers and their repositories
CONTAINERS = getContainers()
REPOSITORIES = getRepositories(CONTAINERS)

# Go through each repository and get the latest image
REPO_NAMES = [*REPOSITORIES.keys()]
REPO_IMAGES = {}
for repo in REPO_NAMES:
  # Get the latest image for each tag
  REPO_IMAGES[repo] = getRepositoryImagesByTag(repo)
  print('Found ' + str(len(REPO_IMAGES[repo])) + ' images for ' + repo)

# Check all container images and see if they match the latest image
for container in CONTAINERS:
  # Only check running containers
  if container['inspect']['State']['Running'] != True: continue

  # Get the container image repository
  containerImageRepo = container['inspect']['Config']['Image']

  # Get the image digest
  CONTAINER_IMAGE_DIGEST = getImageDigest(container['inspect']['Image'])
  
  # Get the namespace, repository, and tag
  containerImageRepo = containerImageRepo.split('/')
  CONTAINER_NAMESPACE = containerImageRepo[0]
  CONTAINER_REPOSITORY = containerImageRepo[1].split(':')[0]
  CONTAINER_TAG = containerImageRepo[1].split(':')[1]

  # Get the newest image for the container tag
  REPOSITORY_IMAGE_DIGEST = REPO_IMAGES[CONTAINER_NAMESPACE + '/' + CONTAINER_REPOSITORY][CONTAINER_TAG]

  # Check if the container image matches the latest image
  IS_UP_TO_DATE = CONTAINER_IMAGE_DIGEST == REPOSITORY_IMAGE_DIGEST

  # Print update status
  if IS_UP_TO_DATE:
    print(container['names'] + ' is up to date!')
  else:
    print(container['names'] + ' is out of date!')