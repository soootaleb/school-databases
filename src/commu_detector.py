import json,os

from constants import BASE_DIR

with open(os.path.join(BASE_DIR, 'scoring_alpha.output.json'), 'r') as input:
    USERS = json.loads(input.read())

followsThreshold = 75
#hashtagThreshold = 2
#mentionThreshold = 2
community = []

def detect():
    for link in USERS:
      
        if USERS[link]["followings"] > followsThreshold:
        
            community.append(link)

    print ("Community : ", community)
    print ("Size of the community : ",len(community))

if __name__ == "__main__":
    detect()

