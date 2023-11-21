import uproot
import numpy as np
import matplotlib.pyplot as plt
import mplhep as hep
plt.style.use(hep.style.ROOT)
import pandas as pd
from csv import writer
from scipy.stats import norm
import argparse
import os


x = [0,1,2,3]
y = [15,11,12,13]


figure1 = plt.figure()
axs = figure1.add_subplot()

axs.plot(x,y)
temp_canvas = figure1.canvas

#fig2 = plt.figure()
#fig2.axes.append(axs)

#plt.show()


print(temp_canvas)