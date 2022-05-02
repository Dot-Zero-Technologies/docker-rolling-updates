import os

# Check if the script is running as root
if os.geteuid() != 0:
  print('This script must be run as root')
  exit()

# Get current working directory
WORKING_DIRECTORY = os.getcwd()

# Write service file
with open('/etc/systemd/system/docker-rolling-updates.service', 'w') as f:
  f.write('[Unit]\n')
  f.write('Description=Docker Rolling Updates\n')
  f.write('\n')
  f.write('[Service]\n')
  f.write('WorkingDirectory=' + WORKING_DIRECTORY + '\n')
  f.write('Type=simple\n')
  f.write('ExecStart=/usr/bin/python3 ./app.py\n')
  f.write('StandardInput=tty-force\n')
  f.write('\n')
  f.write('[Install]\n')
  f.write('WantedBy=multi-user.target\n')
print('Service file written')

# Install pip packages
os.system('pip3 install -r requirements.txt')

# Enable service
os.system('systemctl enable docker-rolling-updates.service')

print('To start the service, run: systemctl start docker-rolling-updates.service')