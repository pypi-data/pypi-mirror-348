# Import Library
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from xes_neo.input_arg import *
from xes_neo.helper import timecall

if timeing_mode:
# %matplotlib inline
    t1 = timecall()

from psutil import cpu_count
# Set the number of threads
import os
import sys
from operator import itemgetter
import numpy as np
import pathlib
import copy
import logging
import operator
import datetime
import random
import csv


import matplotlib as mpl
import matplotlib.pyplot as plt


if timeing_mode:
    initial_elapsed = timecall()- t1
    print('Inital import function took %.2f second' %initial_elapsed)
