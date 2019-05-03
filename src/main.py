import os
import sys
from constants import BASE_DIR

try :
    RELOAD_DATA = sys.argv[1] == "reload"
except:
    print("Not loading data, to do so, add 'reload' argument to scipt execution")
    RELOAD_DATA = False

if RELOAD_DATA:
    exec(open(os.path.join(BASE_DIR,"src","parser.py")).read())
    exec(open(os.path.join(BASE_DIR,"src","scoring_alpha.py")).read())
exec(open(os.path.join(BASE_DIR,"src","commu_detector.py")).read())