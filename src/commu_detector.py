import json, os, time

from analysis import same_circle, same_circle_community
from constants import BASE_DIR, EVAL_COMMU_DETECTOR_MESSAGE, EVAL_COMMU_DETECTOR2_MESSAGE

with open(os.path.join(BASE_DIR, 'scoring_alpha.output.json'), 'r') as input:
    USERS = json.loads(input.read())

followsThreshold = 80
hashtagThreshold = 10
mentionThreshold = 15


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

    output = EVAL_COMMU_DETECTOR_MESSAGE.format(len(community), counter)
    print(output)
    endfun = time.time()
    print ("Time to compute a community detection : ", endfun-startfun," s" )
    return output

# Detects a community by comparing all the users between them 
def detect_complex_commu():
    start_detection = time.time()
    communities = []
    for link in USERS: 
        print(USERS[link])
        if USERS[link]["followings"] > followsThreshold or USERS[link]["#"] > hashtagThreshold or USERS[link]["@"] > mentionThreshold :
            community = []
            left, right = link.split('-')
            for user in USERS:
                currleft, currright = user.split('-')
                if ((currleft == left) | (currleft == right) | (currright == left) | (currright == right)) and ( (USERS[user]["followings"] > followsThreshold) or (USERS[user]["#"] > hashtagThreshold) or (USERS[user]["@"] > mentionThreshold) ):
                    if currleft not in community:
                        community.append(currleft)
                    if currright not in community:
                        community.append(currright)
            if community not in communities:
                communities.append(community)
    for commu in communities:
        print(commu)
    end_detection = time.time()
    results = []
    for community in communities:
        for id in community:
            results.append(same_circle_community(community))
    obtained = [res[0] for res in results]
    truth = [res[1] for res in results]   

    mean = [sum(obtained)/len(results), sum(truth)/len(results)] #Our vs Our, Our vs Truth
    best = [max(obtained), max( truth )]
    worse = [min(obtained), min( truth)]

    end_compare = time.time()
    detection = end_detection-start_detection
    comparison = end_compare-end_detection

    output = EVAL_COMMU_DETECTOR2_MESSAGE.format(followsThreshold, hashtagThreshold, mentionThreshold, len(communities), len(results), best[0], best[1], worse[0],  worse[1], mean[0], mean[1], detection, comparison)
    print(output)

    print("complex community computed in : ", detection," s" )
    print("values comparatives computed in : ", comparison," s" )
    return output
    
if __name__ == "__main__":
    print("user couples in same circles")
    couples = detect()
    print("\ncommunities")
    name = "results_tresh_"+str(followsThreshold) +"_"+ str(hashtagThreshold) + "_"+str(mentionThreshold)+".txt"
    communities = detect_complex_commu()
    with open(os.path.join(BASE_DIR, name) , 'w') as f:
        f.write(couples)
        f.write(communities)

    
