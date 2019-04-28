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
        - {} communities detected,
        - {} communities actually exist

        - {} mean of difference between detected communities
        - {} accuracy

"""