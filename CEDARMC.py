from tokenize import Double
import pandas as pd
import csv
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import math 
import mplhep as hep
plt.style.use(hep.style.ROOT)
from os import listdir , makedirs, path
from os.path import isfile, join
import numpy as np



def n7n8Photons(n7,n8):
    return np.log(1+((8)/((n7/n8)-1)))

def n6n8Photons(n6,n8):
    return np.log(1+((14)/(np.sqrt(4-7*(1-n6/n8))-2)))

def Fold8eff(phi):
    return (1-np.exp(-phi))**8

def Fold7eff(phi,n8):
    return n8 + 8*(1-np.exp(-phi))**7*np.exp(-phi)

def Fold6eff(phi,n7):
    return n7 + 28*(1-np.exp(-phi))**6*np.exp(-2*phi)

filename = "2mm_effredo2.csv"
dfmc = pd.read_csv(filename)
pdfname = "2mmpresurescanredo2"

try:
    makedirs('pdf/mc/{}'.format(pdfname))
except FileExistsError:
    pass
    

ax_4 = dfmc.plot.scatter(x='Pressure',y='6Fold', marker="x", c='DarkBlue',label="6Fold MC")
ax_4_4 = dfmc.plot.scatter(x='Pressure',y='7Fold', marker="x", c='red',label="7Fold MC",ax=ax_4)
ax_4_5 = dfmc.plot.scatter(x='Pressure',y='8Fold', marker="x", c='green',label="8Fold MC",ax=ax_4)

ax_4.set_ylabel("Coincidences per trigger")
ax_4.legend()
ax_4.set_title("At Least N Coincidences per Trigger vs Pressure MC")
plt.savefig("pdf/mc/{}/CoincidencesAvgPointspTrigger.pdf".format(pdfname), format="pdf", bbox_inches="tight")


ax_5 = dfmc.plot.scatter(x='Pressure',y='6Fold', marker="x", c='DarkBlue',label="6Fold MC")
ax_5_4 = dfmc.plot.scatter(x='Pressure',y='7Fold', marker="x", c='red',label="7Fold MC",ax=ax_5)
ax_5_5 = dfmc.plot.scatter(x='Pressure',y='8Fold', marker="x", c='green',label="8Fold MC",ax=ax_5)

ax_5.set_ylabel("Coincidences per trigger")
ax_5.legend()
ax_5.set_title("At Least N Coincidences per Trigger vs Pressure MC")
ax_5.set_yscale('log')
plt.savefig("pdf/mc/{}/LogCoincidencesAvgPointspTrigger.pdf".format(pdfname), format="pdf", bbox_inches="tight")

dfmc['R76'] = dfmc['7Fold']/dfmc['6Fold']
dfmc['R87'] = dfmc['8Fold']/dfmc['7Fold']


ax6 = dfmc.plot.scatter(x='Pressure',y='R76',marker="x",c='DarkBlue' , label="R76 MC")
ax6_3 = dfmc.plot.scatter(x='Pressure',y='R87',marker="x",c='red' , label="R87 MC", ax=ax6)

ax6.set_ylabel("Ratio")
ax6.legend()
plt.savefig("pdf/mc/{}/RatioPlot.pdf".format(pdfname), format="pdf", bbox_inches="tight")


dfmc['Photons78'] = n7n8Photons(dfmc['7Fold'],dfmc['8Fold'])
dfmc['Photons68'] = n7n8Photons(dfmc['6Fold'],dfmc['8Fold'])
dfmc['AvgPhoton'] = (dfmc['Photons78'] + dfmc['Photons68'])/2

ax7 = dfmc.plot.scatter(x='Pressure',y='Photons78',marker="x",c='DarkBlue' , label="Photons78")
ax7_3 = dfmc.plot.scatter(x='Pressure',y='Photons68',marker="x",c='red' , label="Photons68", ax=ax7)
ax7_3 = dfmc.plot.scatter(x='Pressure',y='AvgPhoton',marker="x",c='green' , label="AvgPhoton", ax=ax7)

ax7.set_ylabel("Photons")
ax7.legend(loc='upper center',bbox_to_anchor=(0.54,1))
plt.savefig("pdf/mc/{}/Photons.pdf".format(pdfname), format="pdf", bbox_inches="tight")

dfmc['8FoldEff'] = Fold8eff(dfmc['AvgPhoton'])
dfmc['7FoldEff'] = Fold7eff(dfmc['AvgPhoton'],dfmc['8FoldEff']) 
dfmc['6FoldEff'] = Fold6eff(dfmc['AvgPhoton'],dfmc['7FoldEff'])




ax8 = dfmc.plot.scatter(x='Pressure',y='6FoldEff',marker="x",c='DarkBlue' , label="6Fold")
ax8_3 = dfmc.plot.scatter(x='Pressure',y='7FoldEff',marker="x",c='red' , label="7Fold", ax=ax8)
ax8_3 = dfmc.plot.scatter(x='Pressure',y='8FoldEff',marker="x",c='green' , label="8Fold", ax=ax8)

ax8.set_ylabel("Coincidence Efficiency")
ax8.legend()
plt.savefig("pdf/mc/{}/CoincidenceEfficency.pdf".format(pdfname), format="pdf", bbox_inches="tight")

plt.show()