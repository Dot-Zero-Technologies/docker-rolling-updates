import subprocess

# Run a command in the terminal and return the output
def run(cmd):
  # Run the command
  output = subprocess.check_output(cmd)
  output = output.decode('utf-8').split('\n')

  # Remove the last empty line
  lastIndex = len(output) - 1
  if (len(output[lastIndex]) == 0):
    output.pop(lastIndex)

  return output