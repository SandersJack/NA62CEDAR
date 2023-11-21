import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib import gridspec
import mplhep as hep
plt.style.use(hep.style.ROOT)
import numpy as np 
from sympy import S, symbols, printing
import pandas as pd
from scipy.optimize import curve_fit
from functools import reduce


fwavelength = [220,250,300,350,400,450,500,550,600,650,700]
fpoints = [0,0.88,0.91,0.92,0.93,0.93,0.929,0.927,0.925,0.9225,0.92]

z1 = np.polyfit(fwavelength[:2],fpoints[:2],3)

z2 = np.polyfit(fwavelength[1:],fpoints[1:],3)

xz = np.linspace(220,250,100)
xz2 = np.linspace(250,700,100)

print(z1)
print(z2)

plt.plot(fwavelength,fpoints ,'.' )
plt.plot(xz,np.polyval(z1, xz))
plt.plot(xz2,np.polyval(z2, xz2))
plt.legend(fontsize="small")
plt.show()

plt.show()