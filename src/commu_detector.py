import json,os

from analysis import same_circle
from constants import BASE_DIR, EVAL_COMMU_DETECTOR_MESSAGE

with open(os.path.join(BASE_DIR, 'scoring_alpha.output.json'), 'r') as input:
    USERS = json.loads(input.read())

followsThreshold = 80
hashtagThreshold = 15
mentionThreshold = 7
community = []

def detect():
    user= set()
    for link in USERS:
        usa, usb = link.split('-')
        user.add(usa)
        user.add(usb)
        if USERS[link]["followings"] > followsThreshold:
        
            community.append(link)
        elif USERS[link]["#"] > hashtagThreshold:
            community.append(link)

        elif USERS[link]["@"] > mentionThreshold:
            community.append(link)

    print ("Community : ", community)
    print ("Size of the community : ",len(community))
    print("out of ", len(user), "with in total", len(USERS), "couples of user")
if __name__ == "__main__":
    detect()

'''
#THIS FUNCTION IS NO LONGER USED DUE TO BAD RESULTS

# Detects a community by comparing all the users between them 
def detect_complex_commu():
    communities = []
    for link in USERS: 
        if USERS[link]["followings"] > followsThreshold:
            community = set()
            left, right = link.split('-')
            for user in USERS:
                currleft, currright = user.split('-')
                for commu in communities:
                    if ((currleft == left) | (currleft == right) | (currright == left) | (currright == right)) and (USERS[user]["followings"] > followsThreshold):
                        if currleft not in commu:
                            commu.add(currleft)
                        if currright not in commu:
                            commu.add(currright)
            if community not in communities:
                communities.append(community)
    for commu in communities:
        print(commu)
    counter = 0
     for community in communities:
        for id in community:
            counter = counter + 1 if same_circle_one(id) else counter

    print(EVAL_COMMU_DETECTOR_MESSAGE.format(len(community), counter))

if __name__ == "__main__":
    detect_complex_commu()
'''