
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
  FILTER_LIST = filter.split(',')
  for filter in FILTER_LIST:
    if not isValidFilter(filter):
      # Print error
      print('Invalid filter: ' + filter)
      print('No updates will be allowed!')

      # Disable updates
      FILTER_TYPE = 'WHITELIST'
      FILTER_LIST = []
  
  # Print filter configuration
  print('Filter type: ' + FILTER_TYPE)
  print('Filter list: ' + str(FILTER_LIST))

# Check if a filter is valid
def isValidFilter(filter):
  try:
    NAMESPACE = filter.split('/')[0]
    REPOSITORY = filter.split('/')[1].split(':')[0]
    TAG = filter.split(':')[1]

    if len(NAMESPACE) == 0 or len(REPOSITORY) == 0 or len(TAG) == 0:
      return False
    
    return True
  except:
    return False