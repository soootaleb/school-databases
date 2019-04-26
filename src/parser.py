import os, json

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
PATH = os.path.join(os.getcwd(), "data", "twitter")
USERS = dict()

def get_users_vector():
    for root, directory, files in os.walk(PATH):
        for current_file in filter(lambda f: f[-7:] == 'egofeat', files):
            actual = current_file.split('.')
            user_id = actual[0]
            with open(os.path.join(PATH, current_file), 'r') as feats:
                split = feats.read().split(' ')
                USERS[user_id] = list(map(lambda x: True if x == '1' else False, split))

if __name__ == "__main__":


    get_users_vector()

    for user_id, links in USERS.items():

        with open(os.path.join(PATH, user_id + '.featnames'), 'r') as feats:
            content = filter(lambda x: len(x) > 0, feats.read().split('\n'))
            vector = {
                '#': [],
                '@': []
            }
            
            for line in content:
                hashmention = line[line.index(' ') + 1:]
                vector[hashmention[0]].append(hashmention[1:])

            hash_bool_list = USERS[user_id][:len(vector['#'])]
            mentions_bool_list = USERS[user_id][:len(vector['@'])]
            
            USERS[user_id] = {
                '#': [],
                '@': []
            }

            USERS[user_id]['#'] = list(filter(lambda x: x, [x and y for x, y in zip(hash_bool_list, vector['#'])]))
            USERS[user_id]['@'] = list(filter(lambda x: x, [x and y for x, y in zip(mentions_bool_list, vector['@'])]))

    js = json.dumps(USERS)

    with open(os.path.join(BASE_DIR, 'output.json'), 'w') as f:
        f.write(js)
