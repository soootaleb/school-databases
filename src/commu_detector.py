import json, os, time

from analysis import same_circle, same_circle_community
from constants import BASE_DIR, EVAL_COMMU_DETECTOR_MESSAGE, EVAL_COMMU_DETECTOR2_MESSAGE

with open(os.path.join(BASE_DIR, 'scoring_alpha.output.json'), 'r') as input:
    USERS = json.loads(input.read())



def detect(ft, ht, mt):
    followsThreshold = ft
    hashtagThreshold = ht
    mentionThreshold = mt

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
def detect_complex_commu(follows, hashtags, mentions):
    start_detection = time.time()

    followsThreshold = follows
    hashtagThreshold = hashtags
    mentionThreshold = mentions

    communities = []
    for link in USERS: 
        if USERS[link]["followings"] > followsThreshold or USERS[link]["#"] > hashtagThreshold or USERS[link]["@"] > mentionThreshold :
            community = []
            left, right = link.split('-')
            for couple in USERS:
                currleft, currright = couple.split('-')
                
                checked_treshold = (USERS[couple]["followings"] > followsThreshold) or (USERS[couple]["#"] > hashtagThreshold) or (USERS[couple]["@"] > mentionThreshold)       
                if checked_treshold and (currleft == left or currleft == right or currright == left or currright == right)  :
                #Doublons will be checked.
                    community.append(currleft)
                    community.append(currright)
                    community.append(left)
                    community.append(right)
            if list(frozenset(community)) not in communities:
                #list -> Fronzenset -> list
                #  we sort it and delete doublons, and add only if it does not already exist in the set
                communities.append(list(frozenset(community)))
    for commu in communities:
        print(commu)
    end_detection = time.time()
    results = []
    for community in communities:
        results.append(same_circle_community(community))
    obtained = [res[0] for res in results]
    truth = [res[1] for res in results]   

    mean = [sum(obtained)/len(results), sum(truth)/ max(len(results), len(obtained))] #Our vs Our, Our vs Truth
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
    full_test = False

    if full_test:
        follows = [20, 30, 40, 50, 60, 70, 80]
        hashtags = [1,2,3,4,5,10]
        mentions = [1,2,3,4,5,10]
        for follow in follows:
            for hashtag in hashtags:
                for mention in mentions:
                    print("user couples in same circles")
                    couples = detect(follow, hashtag, mention)
                    print("\ncommunities")
                    name = "results_tresh_"+str(follow) +"_"+ str(hashtag) + "_"+str(mention)+".txt"
                    communities = detect_complex_commu(follow, hashtag, mention)
                    with open(os.path.join(BASE_DIR, name) , 'w') as f:
                        f.write(couples)
                        f.write(communities)
    else:
        followsThreshold = 80
        hashtagThreshold = 10
        mentionThreshold = 15
        print("user couples in same circles")
        couples = detect(followsThreshold, hashtagThreshold, mentionThreshold)
        print("\ncommunities")
        name = "results_tresh_"+str(followsThreshold) +"_"+ str(hashtagThreshold) + "_"+str(mentionThreshold)+".txt"
        communities = detect_complex_commu(followsThreshold, hashtagThreshold, mentionThreshold)
        with open(os.path.join(BASE_DIR, name) , 'w') as f:
            f.write(couples)
            f.write(communities)

        
