import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data", "twitter")

EVAL_COMMU_DETECTOR_MESSAGE = """
    Function "detect":\n
        - {} couples considered in same circle,
        - {} couples actually in same circles
"""
EVAL_COMMU_DETECTOR2_MESSAGE = """
    Function "detect_complex":\n
        tresholds : followers {}, # : {}, @ : {}
        - {} communities detected,
        - {} communities actually exist

        - {} best accuracy (in our community)
        - {} best accuracy (in truth community)
        
        - {} worse accuracy (in our community)
        - {} worse accuracy (in truth community)

        - {} mean accuracy of being in that community (in our community)
        - {} mean accuracy of being in that community (of total community)

        computation time : detection {} s, comparison {} s 
"""