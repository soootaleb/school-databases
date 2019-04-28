import json, os, time

from constants import BASE_DIR

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
    startfun = time.time()
    for left in USERS.keys():

        keys_list = list(USERS.keys())
        interesting_keys = keys_list[keys_list.index(left) + 1:]
        
        # Filtering to skip the current user
        for right in filter(lambda x: x != left, interesting_keys):

            MAP[left + '-' + right] = {
                '#': len(set(USERS[left]['#']) & set(USERS[right]['#'])),
                '@': len(set(USERS[left]['@']) & set(USERS[right]['@'])),
                'followings': len(set(USERS[left]['followings']) & set(USERS[right]['followings']))
            }
    endfun = time.time()
    print("Time to score all users for common features : ", endfun-startfun," s")

def export_to_json():
    print ("Exporting scoring to json...")
    js = json.dumps(MAP)

    with open(os.path.join(BASE_DIR, 'scoring_alpha.output.json'), 'w') as f:
        f.write(js)

if __name__ == "__main__":

    score()

    export_to_json()
    

            
