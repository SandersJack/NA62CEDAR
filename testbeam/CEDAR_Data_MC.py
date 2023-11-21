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

df = pd.read_csv("formated_data/Timber_data.2022-11-04-23-05-45-735_2022-11-05-03-05-31-335.csv")
df['Timestamp (UTC_TIME)'] = pd.to_datetime(df['Timestamp (UTC_TIME)'])

dfmc = pd.read_csv("2mm65GeV.csv")

data_mean = df.groupby('Pressure', as_index=False)['6Fold'].mean()
data_error = df.groupby('Pressure', as_index=False)['6Fold'].sem()
data_mean['6Fold_Error'] = data_error['6Fold'].fillna(0)

data_mean['7Fold'] = df.groupby('Pressure', as_index=False)['7Fold'].mean()['7Fold']
data_error = df.groupby('Pressure', as_index=False)['7Fold'].sem()
data_mean['7Fold_Error'] = data_error['7Fold'].fillna(0)

data_mean['8Fold'] = df.groupby('Pressure', as_index=False)['8Fold'].mean()['8Fold']
data_error = df.groupby('Pressure', as_index=False)['8Fold'].sem()
data_mean['8Fold_Error'] = data_error['8Fold'].fillna(0)

pdfname = str(df['Timestamp (UTC_TIME)'].iloc[0].strftime('%m-%d_%H-%M')) + "--" + str(df['Timestamp (UTC_TIME)'].iloc[-1].strftime('%m-%d_%H-%M')+ "_2")
try:
    makedirs('pdf/data_mc/{}'.format(pdfname))
except FileExistsError:
    pass
    


df['6FoldpTrigger'] = df['6Fold']/df['Trigger']
df['7FoldpTrigger'] = df['7Fold']/df['Trigger']
df['8FoldpTrigger'] = df['8Fold']/df['Trigger']

dfpTrigger_mean = df.groupby('Pressure', as_index=False)['6FoldpTrigger'].mean()
dfpTrigger_error = df.groupby('Pressure', as_index=False)['6FoldpTrigger'].sem()
dfpTrigger_mean['6FoldpTrigger_Error'] = dfpTrigger_error['6FoldpTrigger'].fillna(0)

dfpTrigger_mean['7FoldpTrigger'] = df.groupby('Pressure', as_index=False)['7FoldpTrigger'].mean()['7FoldpTrigger']
dfpTrigger_error = df.groupby('Pressure', as_index=False)['7FoldpTrigger'].sem()
dfpTrigger_mean['7FoldpTrigger_Error'] = dfpTrigger_error['7FoldpTrigger'].fillna(0)

dfpTrigger_mean['8FoldpTrigger'] = df.groupby('Pressure', as_index=False)['8FoldpTrigger'].mean()['8FoldpTrigger']
dfpTrigger_error = df.groupby('Pressure', as_index=False)['8FoldpTrigger'].sem()
dfpTrigger_mean['8FoldpTrigger_Error'] = dfpTrigger_error['8FoldpTrigger'].fillna(0)

ax4 = dfpTrigger_mean.plot.scatter(x='Pressure',y='6FoldpTrigger', yerr = '6FoldpTrigger_Error', xerr=0.001, c='DarkBlue',label="6Fold")
ax4_1 = dfpTrigger_mean.plot.scatter(x='Pressure',y='7FoldpTrigger', yerr = '7FoldpTrigger_Error',xerr=0.001,c='red' , label="7Fold", ax=ax4)
ax4_2 = dfpTrigger_mean.plot.scatter(x='Pressure',y='8FoldpTrigger', yerr = '8FoldpTrigger_Error', xerr=0.001,c='green', label="8Fold", ax=ax4)

ax_4_3 = dfmc.plot.scatter(x='Pressure',y='6Fold', marker="x", c='DarkBlue',label="6Fold MC",ax=ax4)
ax_4_4 = dfmc.plot.scatter(x='Pressure',y='7Fold', marker="x", c='red',label="7Fold MC",ax=ax4)
ax_4_5 = dfmc.plot.scatter(x='Pressure',y='8Fold', marker="x", c='green',label="8Fold MC",ax=ax4)

ax4.set_ylabel("Coincidences per trigger")
ax4.legend()
ax4.set_title("At Least N Coincidences per Trigger vs Pressure")
plt.savefig("pdf/data_mc/{}/CoincidencesAvgPointspTrigger.pdf".format(pdfname), format="pdf", bbox_inches="tight")

ax5 = dfpTrigger_mean.plot.scatter(x='Pressure',y='6FoldpTrigger', yerr = '6FoldpTrigger_Error', xerr=0.001, c='DarkBlue',label="6Fold")
ax5_1 = dfpTrigger_mean.plot.scatter(x='Pressure',y='7FoldpTrigger', yerr = '7FoldpTrigger_Error',xerr=0.001,c='red' , label="7Fold", ax=ax5)
ax5_2 = dfpTrigger_mean.plot.scatter(x='Pressure',y='8FoldpTrigger', yerr = '8FoldpTrigger_Error', xerr=0.001,c='green', label="8Fold", ax=ax5)

ax_5_3 = dfmc.plot.scatter(x='Pressure',y='6Fold', marker="x", c='DarkBlue',label="6Fold MC",ax=ax5)
ax_5_4 = dfmc.plot.scatter(x='Pressure',y='7Fold', marker="x", c='red',label="7Fold MC",ax=ax5)
ax_5_5 = dfmc.plot.scatter(x='Pressure',y='8Fold', marker="x", c='green',label="8Fold MC",ax=ax5)

ax5.set_ylabel("Coincidences per trigger")
ax5.legend()
ax5.set_title("At Least N Coincidences per Trigger vs Pressure")
ax5.set_yscale('log')
plt.savefig("pdf/data_mc/{}/LogCoincidencesAvgPointspTrigger.pdf".format(pdfname), format="pdf", bbox_inches="tight")

df['R76'] = df['7Fold']/df['6Fold']
df['R87'] = df['8Fold']/df['7Fold']

dfmc['R76'] = dfmc['7Fold']/dfmc['6Fold']
dfmc['R87'] = dfmc['8Fold']/dfmc['7Fold']

dRatio_mean = df.groupby('Pressure', as_index=False)['R76'].mean()
dRatio_error = df.groupby('Pressure', as_index=False)['R76'].sem()
dRatio_mean['R76_Error'] = dRatio_error['R76'].fillna(0)

dRatio_mean['R87'] = df.groupby('Pressure', as_index=False)['R87'].mean()['R87']
dRatio_error = df.groupby('Pressure', as_index=False)['R87'].sem()
dRatio_mean['R87_Error'] = dRatio_error['R87'].fillna(0)

ax6 = dRatio_mean.plot.scatter(x='Pressure',y='R76', yerr = 'R76_Error', xerr=0.001, c='DarkBlue',label="R76")
ax6_1 = dRatio_mean.plot.scatter(x='Pressure',y='R87', yerr = 'R87_Error',xerr=0.001,c='red' , label="R87", ax=ax6)

ax6_2 = dfmc.plot.scatter(x='Pressure',y='R76',marker="x",c='DarkBlue' , label="R76 MC", ax=ax6)
ax6_3 = dfmc.plot.scatter(x='Pressure',y='R87',marker="x",c='red' , label="R87 MC", ax=ax6)

ax6.set_ylabel("Ratio")
ax6.legend()
plt.savefig("pdf/data_mc/{}/RatioPlot.pdf".format(pdfname), format="pdf", bbox_inches="tight")

plt.show()