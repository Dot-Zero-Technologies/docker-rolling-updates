import time
from authentication import login
import os
from dotenv import load_dotenv
from docker import getContainers, getImageDigest, getRepositories, pullImage, recreateContainers, removeContainer, startContainer, stopContainer
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

# Start application loop
while True:
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

    # Check if the container requires updating
    if IS_UP_TO_DATE == False:
      print(container['names'] + ' is out of date!')

      # Pull the latest image
      if pullImage(CONTAINER_NAMESPACE + '/' + CONTAINER_REPOSITORY + ':' + CONTAINER_TAG) != True:
        print('Failed to pull image for ' + container['names'])
        continue

      # Stop the container
      print('Stopping ' + container['names'] + '...')
      if stopContainer(container['containerId']) != True:
        print('Failed to stop ' + container['names'])
        continue
      
      # Remove the container
      print('Removing ' + container['names'] + '...')
      if removeContainer(container['containerId']) != True:
        print('Failed to remove ' + container['names'])
        continue

      # Recreate the container
      print('Recreating ' + container['names'] + '...')
      DOCKER_COMPOSE_PATH = container['inspect']['Config']['Labels']['com.docker.compose.project.working_dir']
      if recreateContainers(DOCKER_COMPOSE_PATH) != True:
        print('Failed to recreate ' + container['names'])
        continue
  
  # Wait for a bit before checking again
  time.sleep(int(os.getenv('SLEEP_TIME')))