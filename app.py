import time
from authentication import login
import os
from dotenv import load_dotenv
from debug import enableDebugMode, printDebugMessage
from docker import getContainers, getImageDigest, getRepositories, pruneImages, pullImage, recreateContainers, removeContainer, startContainer, stopContainer
from filter import isValidRepository, loadFilters, repoIsAllowed, splitRepository
from hub import getRepositoryImagesByTag
load_dotenv()

# Check if debug mode is enabled
if os.getenv("DEBUG") == "TRUE": enableDebugMode()

# Authenticate with Docker Hub
def authenticate():
  # Authenticate with Docker Hub
  success = login(os.getenv('DOCKER_USERNAME'), os.getenv('DOCKER_PASSWORD'))

  # Check if authentication was successful
  if success: print('Authentication successful')
  else: print('Authentication failed')

  return success

# Load filters
loadFilters(os.getenv('FILTER_TYPE'), os.getenv('FILTER'))

# Start by authenticating with Docker Hub
if authenticate() == False: exit()

# Print welcome message
print('Welcome to Docker Rolling Updates')

# Start application loop
while True:
  try:
    # Get all containers and their repositories
    CONTAINERS = getContainers()
    REPOSITORIES = getRepositories(CONTAINERS)

    # Go through each repository and get the latest image
    REPO_NAMES = [*REPOSITORIES.keys()]
    REPO_IMAGES = {}
    for repo in REPO_NAMES:
      # Get the latest image for each tag
      REPO_IMAGES[repo] = getRepositoryImagesByTag(repo)
    printDebugMessage('Repository images: ' + str(REPO_IMAGES))

    # Variable to check if any updates were made
    UPDATES_MADE = False

    # Check all container images and see if they match the latest image
    printDebugMessage('Checking container versions')
    for container in CONTAINERS:
      printDebugMessage('Checking container: ' + container['names'])

      # Only check running containers
      if container['inspect']['State']['Running'] != True:
        printDebugMessage('  Skipping container because it is not running')
        continue

      # Get the container image repository
      containerImageRepo = container['inspect']['Config']['Image']
      printDebugMessage('  Container image: ' + containerImageRepo)

      # Check if the repo is valid
      if not isValidRepository(containerImageRepo):
        print('Invalid repository: ' + containerImageRepo)
        continue

      # Split the container image repository into its components
      NAMESPACE, REPOSITORY, TAG = splitRepository(containerImageRepo)

      # Check if the container image should be skipped
      if not repoIsAllowed(NAMESPACE, REPOSITORY, TAG):
        printDebugMessage('  Skipping container because it is not allowed by the filter')
        continue

      # Get the image digest
      CONTAINER_IMAGE_DIGEST = getImageDigest(container['inspect']['Image'])
      printDebugMessage('  Container image digest: ' + CONTAINER_IMAGE_DIGEST)
      
      # Get the namespace, repository, and tag
      containerImageRepo = containerImageRepo.split('/')
      CONTAINER_NAMESPACE = containerImageRepo[0]
      CONTAINER_REPOSITORY = containerImageRepo[1].split(':')[0]
      CONTAINER_TAG = containerImageRepo[1].split(':')[1]

      # Get the newest image for the container tag
      REPOSITORY_IMAGE_DIGEST = REPO_IMAGES[CONTAINER_NAMESPACE + '/' + CONTAINER_REPOSITORY][CONTAINER_TAG]
      printDebugMessage('  Repository image digest: ' + REPOSITORY_IMAGE_DIGEST)

      # Check if the container image matches the latest image
      IS_UP_TO_DATE = CONTAINER_IMAGE_DIGEST == REPOSITORY_IMAGE_DIGEST
      printDebugMessage('  Container is up to date: ' + str(IS_UP_TO_DATE))

      # Check if the container requires updating
      if IS_UP_TO_DATE == False:
        print(container['names'] + ' is out of date!')

        # Pull the latest image
        if pullImage(CONTAINER_NAMESPACE + '/' + CONTAINER_REPOSITORY + ':' + CONTAINER_TAG) != True:
          print('Failed to pull image for ' + container['names'])
          continue
        else: printDebugMessage('  Pulled image for ' + container['names'])

        # Stop the container
        print('Stopping ' + container['names'] + '...')
        if stopContainer(container['containerId']) != True:
          print('Failed to stop ' + container['names'])
          continue
        else: printDebugMessage('  Stopped ' + container['names'])
        
        # Remove the container
        print('Removing ' + container['names'] + '...')
        if removeContainer(container['containerId']) != True:
          print('Failed to remove ' + container['names'])
          continue
        else: printDebugMessage('  Removed ' + container['names'])

        # Recreate the container
        print('Recreating ' + container['names'] + '...')
        DOCKER_COMPOSE_PATH = container['inspect']['Config']['Labels']['com.docker.compose.project.working_dir']
        if recreateContainers(DOCKER_COMPOSE_PATH) != True:
          print('Failed to recreate ' + container['names'])
          continue
        else: printDebugMessage('  Recreated ' + container['names'])

        # Set UPDATES_MADE to true
        UPDATES_MADE = True
    
    # Prune unused images if any updates were made
    if UPDATES_MADE:
      print('Pruning unused images...')
      if pruneImages() == True:
        printDebugMessage('  Pruned unused images')
    
    # Wait for a bit before checking again
    printDebugMessage('Sleeping for ' + os.getenv('SLEEP_TIME') + ' seconds')
    time.sleep(int(os.getenv('SLEEP_TIME')))
  except Exception as error:
    # Print error message
    print('An error occurred during the application loop')
    printDebugMessage(error)
    print('Reauthenticating with Docker Hub...')
    
    # Try to authenticate again
    if authenticate() == False:
      print('Failed to reauthenticate with Docker Hub')
      print('Sleeping for one minute before trying again...')
      time.sleep(60)
    else:
      print('Reauthentication successful')
      print('Sleeping for ' + str(os.getenv('SLEEP_TIME')) + ' second(s) before trying again...')
      time.sleep(int(os.getenv('SLEEP_TIME')))