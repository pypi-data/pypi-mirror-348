import sys
import os

# Put the URL and port of the REST API server here.
url = "localhost"
port = 8080

file_name = sys.argv[1]

output = os.popen(
    'python execute_workflow_remotely.py "'
    + file_name
    + '" -a '
    + url
    + ' - p '
    + str(port)
).read()
print(output)
input("Press any key to close the window.")
