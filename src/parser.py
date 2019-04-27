import os, json

from constants import BASE_DIR, DATA_DIR

USERS = dict()

CHARS_TO_REMOVE = ['.', ',', '!', ':']

def remove_userless_chars(string):
    strr = ''
    for c in CHARS_TO_REMOVE:
        strr = string.replace(c, '')
    return strr

def get_users_vector():
    for root, directory, files in os.walk(DATA_DIR):
        for current_file in filter(lambda f: f[-7:] == 'egofeat', files):
            actual = current_file.split('.')
            user_id = actual[0]
            with open(os.path.join(DATA_DIR, current_file), 'r') as feats:
                split = feats.read().split(' ')
                USERS[user_id] = list(map(lambda x: True if x == '1' else False, split))

def get_users_hashmens():
    for user_id, links in USERS.items():

        with open(os.path.join(DATA_DIR, user_id + '.featnames'), 'r', encoding = 'utf8') as feats:
            content = filter(lambda x: len(x) > 0, feats.read().split(os.linesep))
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

            USERS[user_id]['#'] = list(set(map(remove_userless_chars, USERS[user_id]['#'])))
            USERS[user_id]['@'] = list(set(map(remove_userless_chars, USERS[user_id]['@'])))

def export_to_json():
    js = json.dumps(USERS)

    with open(os.path.join(BASE_DIR, 'parser.output.json'), 'w') as f:
        f.write(js)

def get_users_followings():
    with open(os.path.join(BASE_DIR, 'data', 'twitter_combined.txt'), 'r') as f:
        lines = f.read().split("\n")

        for line in filter(len, lines):

            user, followings = line.split(' ')

            if user in USERS.keys():
                if 'followings' in USERS[user].keys():
                    USERS[user]['followings'].append(followings)
                else:
                    USERS[user]['followings'] = [followings]

if __name__ == "__main__":

    get_users_vector()

    get_users_hashmens()

    get_users_followings()

    export_to_json()
    
