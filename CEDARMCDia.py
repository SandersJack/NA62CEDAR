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


filename = "scan_4.15.csv"
dfmc = pd.read_csv(filename)
pdfname = "4_15DiaScan"

try:
    makedirs('pdf/mc/{}'.format(pdfname))
except FileExistsError:
    pass
    

ax_4 = dfmc.plot.scatter(x='Diaphragm',y='6Fold', marker="x", c='DarkBlue',label="6Fold MC")
ax_4_4 = dfmc.plot.scatter(x='Diaphragm',y='7Fold', marker="x", c='red',label="7Fold MC",ax=ax_4)
ax_4_5 = dfmc.plot.scatter(x='Diaphragm',y='8Fold', marker="x", c='green',label="8Fold MC",ax=ax_4)

ax_4.set_ylabel("Coincidences per trigger")
ax_4.legend()
ax_4.set_title("At Least N Coincidences per Trigger vs Diaphragm MC")
plt.savefig("pdf/mc/{}/CoincidencesAvgPointspTrigger.pdf".format(pdfname), format="pdf", bbox_inches="tight")


ax_5 = dfmc.plot.scatter(x='Diaphragm',y='6Fold', marker="x", c='DarkBlue',label="6Fold MC")
ax_5_4 = dfmc.plot.scatter(x='Diaphragm',y='7Fold', marker="x", c='red',label="7Fold MC",ax=ax_5)
ax_5_5 = dfmc.plot.scatter(x='Diaphragm',y='8Fold', marker="x", c='green',label="8Fold MC",ax=ax_5)

ax_5.set_ylabel("Coincidences per trigger")
ax_5.legend()
ax_5.set_title("At Least N Coincidences per Trigger vs Diaphragm MC")
ax_5.set_yscale('log')
plt.savefig("pdf/mc/{}/LogCoincidencesAvgPointspTrigger.pdf".format(pdfname), format="pdf", bbox_inches="tight")

dfmc['R76'] = dfmc['7Fold']/dfmc['6Fold']
dfmc['R87'] = dfmc['8Fold']/dfmc['7Fold']


ax6 = dfmc.plot.scatter(x='Diaphragm',y='R76',marker="x",c='DarkBlue' , label="R76 MC")
ax6_3 = dfmc.plot.scatter(x='Diaphragm',y='R87',marker="x",c='red' , label="R87 MC", ax=ax6)

ax6.set_ylabel("Ratio")
ax6.legend()
plt.savefig("pdf/mc/{}/RatioPlot.pdf".format(pdfname), format="pdf", bbox_inches="tight")

plt.show()