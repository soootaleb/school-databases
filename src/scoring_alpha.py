import json, os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

with open(os.path.join(BASE_DIR, 'parser.output.json'), 'r') as output:
    USERS = json.loads(output.read())

'''
MAP = {
    'left-right': {
        '#': 13,
        '@': 25,
        'followings': 3
    }
}
'''
MAP = dict() 

'''
Objective: compute eache couple of users couting their common hashtags or mentions

dim parameter can be

- "#"
- "@"
- "followings"
'''
def score():

    for left in USERS.keys():

        # Filtering to skip the current user
        for right in filter(lambda x: x != left, USERS.keys()):

            MAP[left + '-' + right] = {
                '#': len(set(USERS[left]['#']) & set(USERS[right]['#'])),
                '@': len(set(USERS[left]['@']) & set(USERS[right]['@'])),
                'followings': len(set(USERS[left]['followings']) & set(USERS[right]['followings']))
            }

def export_to_json():
    js = json.dumps(MAP)

    with open(os.path.join(BASE_DIR, 'scoring_alpha.output.json'), 'w') as f:
        f.write(js)

if __name__ == "__main__":

    score()

    export_to_json()
    

            
