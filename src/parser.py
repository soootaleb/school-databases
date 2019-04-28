import os, json, time

from constants import BASE_DIR, DATA_DIR

USERS = dict()
CIRCLES = set()
CHARS_TO_REMOVE = ['.', ',', '!', ':']

def remove_userless_chars(string):
    strr = ''
    for c in CHARS_TO_REMOVE:
        strr = string.replace(c, '')
    return strr

def get_users_vector():
    startfun = time.time()
    for root, directory, files in os.walk(DATA_DIR):
        for current_file in filter(lambda f: f[-7:] == 'egofeat', files):
            actual = current_file.split('.')
            user_id = actual[0]
            with open(os.path.join(DATA_DIR, current_file), 'r') as feats:
                split = feats.read().split(' ')
                USERS[user_id] = list(map(lambda x: True if x == '1' else False, split))
        for current_file in filter(lambda f: f[-7:] == 'circles', files):
            actual = current_file.split('.')
            user_id = actual[0]
            with open(os.path.join(DATA_DIR, current_file), 'r') as circles:
                for circle in circles:
                    split = circle.split('\t')
                    split[0] = user_id #first is circle number in file, whereas it does not contain user_id so we replace it here
                    split[-1] = split[-1][:-1]
                    
                    circ = frozenset(split)
                    CIRCLES.add(circ)
    endfun = time.time()
    print ("Time to get users vector : ", endfun-startfun," s")

def get_users_hashmens():
    startfun = time.time()
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
    endfun = time.time()
    print ("Time to get users hashtags and mentions : ",endfun-startfun," s")

def export_to_json():
    print("Exporting parsing to json...")
    users = json.dumps(USERS)
    with open(os.path.join(BASE_DIR, 'parser.output.json'), 'w') as f:
        f.write(users)

    circles = json.dumps([ list(x) for x in list (CIRCLES) ] )
    with open(os.path.join(BASE_DIR, 'circles.json'), 'w') as f:
        f.write(circles)

def get_users_followings():
    startfun = time.time()
    with open(os.path.join(BASE_DIR, 'data', 'twitter_combined.txt'), 'r') as f:
        lines = f.read().split("\n")

        for line in filter(len, lines):

            user, followings = line.split(' ')

            if user in USERS.keys():
                if 'followings' in USERS[user].keys():
                    USERS[user]['followings'].append(followings)
                else:
                    USERS[user]['followings'] = [followings]
    endfun = time.time()
    print("Time to get users followings : ", endfun-startfun," s")

if __name__ == "__main__":

    startmain = time.time()

    get_users_vector()

    get_users_hashmens()

    get_users_followings()
    
    export_to_json()
    
    endmain = time.time()
    print ("Time spent to parse all users : ", endmain - startmain," s")
