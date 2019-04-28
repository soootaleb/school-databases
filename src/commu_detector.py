import json,os, time

from analysis import same_circle,same_circle_community
from constants import BASE_DIR, EVAL_COMMU_DETECTOR_MESSAGE,EVAL_COMMU_DETECTOR2_MESSAGE

with open(os.path.join(BASE_DIR, 'scoring_alpha.output.json'), 'r') as input:
    USERS = json.loads(input.read())

followsThreshold = 80
hashtagThreshold = 15
mentionThreshold = 7


def detect():
    startfun = time.time()
    community = []
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
    print("out of ", len(user), "with in total", len(USERS))
    counter = 0
    for com in community:
        left, right = com.split('-')
        counter = counter + 1 if same_circle(left, right) else counter

    print(EVAL_COMMU_DETECTOR_MESSAGE.format(len(community), counter))
    endfun = time.time()
    print ("Time to compute a community detection : ", endfun-startfun," s" )


# Detects a community by comparing all the users between them 
def detect_complex_commu():
    startfun = time.time()
    communities = []
    for link in USERS: 
        if USERS[link]["followings"] > followsThreshold:
            community = []
            left, right = link.split('-')
            for user in USERS:
                currleft, currright = user.split('-')
                if ((currleft == left) | (currleft == right) | (currright == left) | (currright == right)) and (USERS[user]["followings"] > followsThreshold):
                    if currleft not in community:
                        community.append(currleft)
                    if currright not in community:
                        community.append(currright)
            if community not in communities:
                communities.append(community)
    for commu in communities:
        print(commu)
    results = []
    for community in communities:
        for id in community:
            results.append(same_circle_community(community))
    endfun = time.time()
    print(EVAL_COMMU_DETECTOR2_MESSAGE.format(len(communities), len(counts),0.7,0.8))
    print(counts)
    print("complex community computed in : ", endfun-startfun," s" )

if __name__ == "__main__":
    print("user couples in same circles")
    detect()
    print("\ncommunities")
    detect_complex_commu()
