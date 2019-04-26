import json, os

from parser import BASE_DIR

with open(os.path.join(BASE_DIR, 'output.json'), 'r') as output:
    USERS = json.loads(output.read())

print('OK')