
# Allow no updates by default
FILTER_TYPE = 'WHITELIST'
FILTER_LIST = []

def loadFilters(type, filter):
  global FILTER_TYPE
  global FILTER_LIST

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
    NAMESPACE, REPOSITORY, TAG = splitRepository(filter)

    if len(NAMESPACE) == 0 or len(REPOSITORY) == 0 or len(TAG) == 0:
      return False
    
    return True
  except:
    return False

# Split a filter into its components
def splitRepository(filter):
  NAMESPACE = filter.split('/')[0]
  REPOSITORY = filter.split('/')[1].split(':')[0]
  TAG = filter.split(':')[1]
  return NAMESPACE, REPOSITORY, TAG

# Check if a container should be updated
def repoIsAllowed(namespace, repository, tag):
  # Check if the filter is disabled
  if FILTER_TYPE == 'DISABLED':
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
    
    # Check if the repository matches
    if filter['REPOSITORY'] == '*' or filter['REPOSITORY'] == repository:
      REPOSITORY_MATCH = True
    
    # Check if the tag matches
    if filter['TAG'] == '*' or filter['TAG'] == tag:
      TAG_MATCH = True
    
    # Check if the filter matches
    if NAMESPACE_MATCH and REPOSITORY_MATCH and TAG_MATCH:
      FOUND_IN_FILTER_LIST = True
      break
  
  # If filter is a whitelist, return true if the filter is found
  if FILTER_TYPE == 'WHITELIST':
    return FOUND_IN_FILTER_LIST
  
  # If filter is a blacklist, return true if the filter is not found
  if FILTER_TYPE == 'BLACKLIST':
    return not FOUND_IN_FILTER_LIST
  
  return False