
# Allow no updates by default
from debug import getDebugMode, printDebugMessage


FILTER_TYPE = 'WHITELIST'
FILTER_LIST = []

def loadFilters(type, filter):
  global FILTER_TYPE
  global FILTER_LIST

  # Print debug messages
  printDebugMessage('Read filter type: ' + type)
  printDebugMessage('Read filter: ' + filter)

  # Load filter type
  if type in ['WHITELIST', 'BLACKLIST', 'DISABLED']:
    FILTER_TYPE = type
  else: print('Invalid filter type: ' + type)

  # Load filter list
  filters = filter.split(',')
  for filter in filters:
    if isValidRepository(filter):
      NAMESPACE, REPOSITORY, TAG = splitRepository(filter)
      FILTER_LIST.append({
        'NAMESPACE': NAMESPACE,
        'REPOSITORY': REPOSITORY,
        'TAG': TAG
      })
    else:
      # Print error
      print('Invalid filter: ' + filter)
      print('No updates will be allowed!')

      # Disable updates
      FILTER_TYPE = 'WHITELIST'
      FILTER_LIST = []
      break
  
  # Print filter configuration
  print('Filter type: ' + FILTER_TYPE)
  print('Filter list: ' + str(FILTER_LIST))

# Check if a filter is valid
def isValidRepository(filter):
  try:
    # Print debug message
    printDebugMessage('Validating filter: ' + filter)

    NAMESPACE, REPOSITORY, TAG = splitRepository(filter)

    # Print debug messages
    printDebugMessage('  Namespace: ' + NAMESPACE)
    printDebugMessage('  Repository: ' + REPOSITORY)
    printDebugMessage('  Tag: ' + TAG)

    if len(NAMESPACE) == 0 or len(REPOSITORY) == 0 or len(TAG) == 0:
      return False
    
    return True
  except:
    return False

# Split a filter into its components
def splitRepository(filter):
  # Print debug message
  printDebugMessage('Splitting filter: ' + filter)

  NAMESPACE = filter.split('/')[0]
  REPOSITORY = filter.split('/')[1].split(':')[0]
  TAG = filter.split(':')[1]

  # Print debug messages
  printDebugMessage('  Namespace: ' + NAMESPACE)
  printDebugMessage('  Repository: ' + REPOSITORY)
  printDebugMessage('  Tag: ' + TAG)

  return NAMESPACE, REPOSITORY, TAG

# Check if a container should be updated
def repoIsAllowed(namespace, repository, tag):
  # Print debug message
  printDebugMessage('Checking if repository is allowed: ' + namespace + '/' + repository + ':' + tag)

  # Check if the filter is disabled
  if FILTER_TYPE == 'DISABLED':
    # Print debug message
    printDebugMessage('  Filter is disabled')

    return True
  
  # Check if any filter is applicable
  FOUND_IN_FILTER_LIST = False
  for filter in FILTER_LIST:
    NAMESPACE_MATCH = False
    REPOSITORY_MATCH = False
    TAG_MATCH = False

    # Check if the namespace matches
    if filter['NAMESPACE'] == '*' or filter['NAMESPACE'] == namespace:
      NAMESPACE_MATCH = True
      printDebugMessage('  Namespace matches')
    
    # Check if the repository matches
    if filter['REPOSITORY'] == '*' or filter['REPOSITORY'] == repository:
      REPOSITORY_MATCH = True
      printDebugMessage('  Repository matches')
    
    # Check if the tag matches
    if filter['TAG'] == '*' or filter['TAG'] == tag:
      TAG_MATCH = True
      printDebugMessage('  Tag matches')
    
    # Check if the filter matches
    if NAMESPACE_MATCH and REPOSITORY_MATCH and TAG_MATCH:
      FOUND_IN_FILTER_LIST = True
      printDebugMessage('  Filter matches')
      break
    else: printDebugMessage('  Filter does not match')
  
  # If filter is a whitelist, return true if the filter is found
  if FILTER_TYPE == 'WHITELIST':
    printDebugMessage('  Filter type is whitelist, result is ' + str(FOUND_IN_FILTER_LIST))
    return FOUND_IN_FILTER_LIST
  
  # If filter is a blacklist, return true if the filter is not found
  if FILTER_TYPE == 'BLACKLIST':
    printDebugMessage('  Filter type is blacklist, result is ' + str(not FOUND_IN_FILTER_LIST))
    return not FOUND_IN_FILTER_LIST
  
  printDebugMessage('  Filter type is invalid, result is False')
  return False