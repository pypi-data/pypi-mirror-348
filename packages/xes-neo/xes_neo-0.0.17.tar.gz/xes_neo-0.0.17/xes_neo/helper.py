import time
from xes_neo.__init__  import __version__

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def timecall():
    return time.time()

def str_to_bool(s):
    if s == 'True':
         return True
    elif s == 'False':
         return False
    else:
         raise ValueError # evil ValueError that doesn't tell you what the wrong value was

def str_to_list(s):
    arr = [float(i) for i in list(s.split(","))]
    return arr

def norm(val):
    return np.linalg.norm(val)


def banner():
    """
    https://patorjk.com/software/taag/#p=display&h=2&v=0&f=Univers&t=XES%20NEO
    """
    banner_str = ('''
                                XES Neo ver %s
__________________________________________________________________________________
                                                                                   
 ▄       ▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄       ▄▄        ▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄ 
▐░▌     ▐░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌     ▐░░▌      ▐░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌
 ▐░▌   ▐░▌ ▐░█▀▀▀▀▀▀▀▀▀ ▐░█▀▀▀▀▀▀▀▀▀      ▐░▌░▌     ▐░▌▐░█▀▀▀▀▀▀▀▀▀ ▐░█▀▀▀▀▀▀▀█░▌
  ▐░▌ ▐░▌  ▐░▌          ▐░▌               ▐░▌▐░▌    ▐░▌▐░▌          ▐░▌       ▐░▌
   ▐░▐░▌   ▐░█▄▄▄▄▄▄▄▄▄ ▐░█▄▄▄▄▄▄▄▄▄      ▐░▌ ▐░▌   ▐░▌▐░█▄▄▄▄▄▄▄▄▄ ▐░▌       ▐░▌
    ▐░▌    ▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌     ▐░▌  ▐░▌  ▐░▌▐░░░░░░░░░░░▌▐░▌       ▐░▌
   ▐░▌░▌   ▐░█▀▀▀▀▀▀▀▀▀  ▀▀▀▀▀▀▀▀▀█░▌     ▐░▌   ▐░▌ ▐░▌▐░█▀▀▀▀▀▀▀▀▀ ▐░▌       ▐░▌
  ▐░▌ ▐░▌  ▐░▌                    ▐░▌     ▐░▌    ▐░▌▐░▌▐░▌          ▐░▌       ▐░▌
 ▐░▌   ▐░▌ ▐░█▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄█░▌     ▐░▌     ▐░▐░▌▐░█▄▄▄▄▄▄▄▄▄ ▐░█▄▄▄▄▄▄▄█░▌
▐░▌     ▐░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌     ▐░▌      ▐░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌
 ▀       ▀  ▀▀▀▀▀▀▀▀▀▀▀  ▀▀▀▀▀▀▀▀▀▀▀       ▀        ▀▀  ▀▀▀▀▀▀▀▀▀▀▀  ▀▀▀▀▀▀▀▀▀▀▀ 
                                                                                
__________________________________________________________________________________

    '''% __version__)

    return banner_str
