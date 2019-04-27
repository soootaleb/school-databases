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
    for link in USERS:
      
        if USERS[link]["followings"] > followsThreshold:
        
            community.append(link)
        elif USERS[link]["#"] > hashtagThreshold:
            community.append(link)

        elif USERS[link]["@"] > mentionThreshold:
            community.append(link)

    print ("Community : ", community)
    print ("Size of the community : ",len(community))

if __name__ == "__main__":
    detect()

    counter = 0
    for com in community:
        left, right = com.split('-')
        counter = counter + 1 if same_circle(left, right) else counter

    print(EVAL_COMMU_DETECTOR_MESSAGE.format(len(community), counter))
