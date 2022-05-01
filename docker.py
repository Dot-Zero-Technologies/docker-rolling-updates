import json
from terminal import run

# Get all current containers
def getContainers():
  # Get the list of running containers
  output = run(['docker', 'ps', '-a', '--no-trunc'])
  header = output.pop(0)

  # Find the length of the longest line
  maxLength = 0
  for line in output:
    if (len(line) > maxLength):
      maxLength = len(line)

  # Get the index of the columns
  CONTAINER_ID_INDEX = header.index('CONTAINER ID')
  IMAGE_INDEX = header.index('IMAGE')
  COMMAND_INDEX = header.index('COMMAND')
  CREATED_INDEX = header.index('CREATED')
  STATUS_INDEX = header.index('STATUS')
  PORTS_INDEX = header.index('PORTS')
  NAMES_INDEX = header.index('NAMES')

  # Calculate the length of columns
  CONTAINER_ID_LENGTH = IMAGE_INDEX - CONTAINER_ID_INDEX
  IMAGE_LENGTH = COMMAND_INDEX - IMAGE_INDEX
  COMMAND_LENGTH = CREATED_INDEX - COMMAND_INDEX
  CREATED_LENGTH = STATUS_INDEX - CREATED_INDEX
  STATUS_LENGTH = PORTS_INDEX - STATUS_INDEX
  PORTS_LENGTH = NAMES_INDEX - PORTS_INDEX
  NAMES_LENGTH = maxLength - NAMES_INDEX

  # Go through each line and parse the data
  containers = []
  for line in output:
    # Get the data
    containerId = line[CONTAINER_ID_INDEX:CONTAINER_ID_INDEX + CONTAINER_ID_LENGTH].strip()
    image = line[IMAGE_INDEX:IMAGE_INDEX + IMAGE_LENGTH].strip()
    command = line[COMMAND_INDEX:COMMAND_INDEX + COMMAND_LENGTH].strip()
    created = line[CREATED_INDEX:CREATED_INDEX + CREATED_LENGTH].strip()
    status = line[STATUS_INDEX:STATUS_INDEX + STATUS_LENGTH].strip()
    ports = line[PORTS_INDEX:PORTS_INDEX + PORTS_LENGTH].strip()
    names = line[NAMES_INDEX:NAMES_INDEX + NAMES_LENGTH].strip()
    inspect = getContainerDetails(containerId)

    # Add the container to the list
    containers.append({
      'containerId': containerId,
      'image': image,
      'command': command,
      'created': created,
      'status': status,
      'ports': ports,
      'names': names,
      'inspect': inspect
    })
  
  return containers

# Get container repositories
def getRepositories(containers):
  repositories = {}
  for container in containers:
    # Get the image name
    image = container['inspect']['Config']['Image']

    # Get the repository name
    repository = image.split(':')
    repository = repository[0]

    # Add the repository to the list
    if repository not in repositories:
      repositories[repository] = []
    repositories[repository].append(container['containerId'])

  return repositories

# Get container details
def getContainerDetails(containerId):
  # Get the container details
  output = run(['docker', 'inspect', containerId])
  
  # Join the output into a single string
  output = ''.join(output)

  # Convert the output to a JSON object
  output = json.loads(output)[0]
  
  return output

# Get an image digest
def getImageDigest(image):
  # Get the image details
  output = run(['docker', 'inspect', image])
  
  # Join the output into a single string
  output = ''.join(output)

  # Convert the output to a JSON object
  output = json.loads(output)[0]

  # Get the digest
  digest = output['RepoDigests'][0]
  digest = digest.split('@')[1]

  return digest

# Pull an image
def pullImage(image):
  # Get the image details
  output = run(['docker', 'pull', image])
  output = ''.join(output)

  # Check if the image was pulled
  if 'Pull complete' in output or 'Image is up to date' in output:
    return True
  else:
    return False

# Try to stop a container
def stopContainer(containerId):
  # Stop the container
  output = run(['docker', 'stop', containerId])
  output = ''.join(output)

  # Check if the container was stopped
  if output == containerId:
    return True
  else:
    return False

# Try to start a container
def startContainer(containerId):
  # Start the container
  output = run(['docker', 'start', containerId])
  output = ''.join(output)

  # Check if the container was started
  if output == containerId:
    return True
  else:
    return False

# Try to remove a container
def removeContainer(containerId):
  # Remove the container
  output = run(['docker', 'rm', containerId])
  output = ''.join(output)

  # Check if the container was removed
  if output == containerId:
    return True
  else:
    return False

# Try to recreate a stopped compose containers
def recreateContainers(composePath):
  # Run docker compose up
  run(['docker', 'compose', 'up', '-d', '--no-recreate'], composePath)

  return True