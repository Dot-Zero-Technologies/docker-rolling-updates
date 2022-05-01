from authentication import login
import os
from dotenv import load_dotenv
from docker import getContainers, getRepositories
from hub import getRepositoryImages
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
for repo in REPO_NAMES:
  print('Getting images for repository: ' + repo)
  images = getRepositoryImages(repo)
  print(images)