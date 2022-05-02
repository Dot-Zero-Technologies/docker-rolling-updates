DEBUG_MODE = False

# Enable debug mode
def enableDebugMode():
  global DEBUG_MODE
  DEBUG_MODE = True
  print('DEBUG_MODE: ' + str(DEBUG_MODE))

# Get the debug mode
def getDebugMode():
  return DEBUG_MODE

# Print debug message
def printDebugMessage(message):
  if getDebugMode():
    print(message)