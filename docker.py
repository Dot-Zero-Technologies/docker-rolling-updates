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
    image = container['image']

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