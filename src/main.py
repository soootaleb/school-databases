import os
from constants import BASE_DIR

exec(open(os.path.join(BASE_DIR,"src","parser.py")).read())
exec(open(os.path.join(BASE_DIR,"src","scoring_alpha.py")).read())
exec(open(os.path.join(BASE_DIR,"src","commu_detector.py")).read())