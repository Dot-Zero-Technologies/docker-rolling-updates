from authentication import login
import os
from dotenv import load_dotenv
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