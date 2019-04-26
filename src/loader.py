import os, json

from constants import BASE_DIR

with open(os.path.join(BASE_DIR, 'parser.output.json'), 'r') as output:
    USERS = json.loads(output.read())

with open(os.path.join(BASE_DIR, 'scoring_alpha.output.json'), 'r') as output:
    SCORES = json.loads(output.read())