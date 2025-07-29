import sys
import os

file_name = sys.argv[1]
path = '/mnt/' + (file_name[0].lower() + file_name[2:]).replace('\\', '/')

output = os.popen(
    'bash -c "export DISPLAY=:0; '
    + 'source ~/ep-bolfi/bin/activate; '
    + 'python3 ~/execute_workflow_locally.py \''
    + path
    + '\'"'
).read()
print(output)
input("Press any key to close the window.")
