from authentication import login
import os
from dotenv import load_dotenv
load_dotenv()

print(login(
  os.getenv('DOCKER_USERNAME'),
  os.getenv('DOCKER_PASSWORD')
))