from loader import USERS, SCORES
from constants import DATA_DIR
import itertools
import os

'''
Returns True if the two users are in a circle
Returns False otherwise
'''
def same_circle(left, right):
    with open(os.path.join(DATA_DIR, left + '.circles'), 'r', encoding='utf8') as circles:
        for circle in filter(len, circles.read().split('\n')):
            users = circle.split('\t')[1:]
            if right in users:
                return True
    
    with open(os.path.join(DATA_DIR, right + '.circles'), 'r', encoding='utf8') as circles:
        for circle in filter(len, circles.read().split('\n')):
            users = circle.split('\t')[1:]
            if left in users:
                return True
        
    return False

def same_circle_community(community):
    communities_values = []
    for user_id in community:
        with open(os.path.join(DATA_DIR, user_id + '.circles'), 'r', encoding='utf8') as circles:
            for circle in filter(len,circles.read().split('\n')):
                users = circle.split('\t')[1:]
                test = [x in users for x in community]

                communities_values.append([sum(test) / len(community), sum(test) / len(users)])

    return max(communities_values)

def count_all_communities(communities):
    #Work In Progress

    #count all the communities of all users, but without doublons
    communities_test = []
    for community in communities:
        for user in community:
            with open(os.path.join(DATA_DIR, user + '.circles'), 'r', encoding='utf8') as circles:
                for circle in filter(len, circles.read().split('\n')):
                    users = circle.split('\t')[1:] #We dont want the number of that communty so [1:]
                    users.append(user) #circles does not contain the current user.
                    communities_test.append(users)

    communities_test = list(k for k,_ in itertools.groupby(communities_test))
    return len(communities_test)



if __name__ == "__main__":

    same_circle('532617990', '202674661') # True
    same_circle('532617990', '154070583') # False

    print('OK')