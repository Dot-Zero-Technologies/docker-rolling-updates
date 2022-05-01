from requests import head
from terminal import run

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

    # Add the container to the list
    containers.append({
      'containerId': containerId,
      'image': image,
      'command': command,
      'created': created,
      'status': status,
      'ports': ports,
      'names': names
    })
  
  return containers