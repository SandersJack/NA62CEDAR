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

outfile = "formated_data/Timber_data.2022-11-05-10-30-04-935_2022-11-05-16-00-31-335.csv"

df = pd.read_csv(outfile)
df['Timestamp (UTC_TIME)'] = pd.to_datetime(df['Timestamp (UTC_TIME)'])


data_mean = df.groupby('Pressure', as_index=False)['PMT0'].mean()
data_error = df.groupby('Pressure', as_index=False)['PMT0'].sem()
data_mean['PMT0_Error'] = data_error['PMT0'].fillna(0)

data_mean['PMT1'] = df.groupby('Pressure', as_index=False)['PMT1'].mean()['PMT1']
data_error = df.groupby('Pressure', as_index=False)['PMT1'].sem()
data_mean['PMT1_Error'] = data_error['PMT1'].fillna(0)

data_mean['PMT2'] = df.groupby('Pressure', as_index=False)['PMT2'].mean()['PMT2']
data_error = df.groupby('Pressure', as_index=False)['PMT2'].sem()
data_mean['PMT2_Error'] = data_error['PMT2'].fillna(0)

data_mean['PMT3'] = df.groupby('Pressure', as_index=False)['PMT3'].mean()['PMT3']
data_error = df.groupby('Pressure', as_index=False)['PMT3'].sem()
data_mean['PMT3_Error'] = data_error['PMT3'].fillna(0)

data_mean['PMT4'] = df.groupby('Pressure', as_index=False)['PMT4'].mean()['PMT4']
data_error = df.groupby('Pressure', as_index=False)['PMT4'].sem()
data_mean['PMT4_Error'] = data_error['PMT4'].fillna(0)

data_mean['PMT5'] = df.groupby('Pressure', as_index=False)['PMT5'].mean()['PMT5']
data_error = df.groupby('Pressure', as_index=False)['PMT5'].sem()
data_mean['PMT5_Error'] = data_error['PMT5'].fillna(0)

data_mean['PMT6'] = df.groupby('Pressure', as_index=False)['PMT6'].mean()['PMT6']
data_error = df.groupby('Pressure', as_index=False)['PMT6'].sem()
data_mean['PMT6_Error'] = data_error['PMT6'].fillna(0)

data_mean['PMT7'] = df.groupby('Pressure', as_index=False)['PMT7'].mean()['PMT7']
data_error = df.groupby('Pressure', as_index=False)['PMT7'].sem()
data_mean['PMT7_Error'] = data_error['PMT7'].fillna(0)

pdfname = str(df['Timestamp (UTC_TIME)'].iloc[0].strftime('%m-%d_%H-%M')) + "--" + str(df['Timestamp (UTC_TIME)'].iloc[-1].strftime('%m-%d_%H-%M'))
try:
    makedirs('pdf/PMT/{}'.format(pdfname))
except FileExistsError:
    pass
    
print(data_mean.head(10))
ax1 = df.plot.scatter(x='Timestamp (UTC_TIME)',y='Pressure', c='DarkBlue')
ax1.grid()
plt.savefig("pdf/{}/Pressure.pdf".format(pdfname), format="pdf", bbox_inches="tight")

ax2 = df.plot.scatter(x='Pressure',y='PMT0',c='b',label="PMT0")
ax2_1 = df.plot.scatter(x='Pressure',y='PMT1',c='g' ,label="PMT1", ax=ax2)
ax2_2 = df.plot.scatter(x='Pressure',y='PMT2', c='r',label="PMT2", ax=ax2)
ax2_3 = df.plot.scatter(x='Pressure',y='PMT3',c='c', label="PMT3", ax=ax2)
ax2_4 = df.plot.scatter(x='Pressure',y='PMT4', c='m',label="PMT4", ax=ax2)
ax2_5 = df.plot.scatter(x='Pressure',y='PMT5', c='y',label="PMT5", ax=ax2)
ax2_6 = df.plot.scatter(x='Pressure',y='PMT6', c='orange',label="PMT6", ax=ax2)
ax2_7 = df.plot.scatter(x='Pressure',y='PMT7', c='brown',label="PMT7", ax=ax2)



ax2.set_ylabel("Counts")
ax2.legend()
ax2.set_title("All pressure points")
ax2.grid()
plt.savefig("pdf/PMT/{}/CoincidencesAllPoints.pdf".format(pdfname), format="pdf", bbox_inches="tight")

ax3 = data_mean.plot.scatter(x='Pressure',y='PMT0', yerr = 'PMT0_Error',c='b',label="PMT0")
ax3_1 = data_mean.plot.scatter(x='Pressure',y='PMT1',  yerr = 'PMT1_Error',c='g', label="PMT1", ax=ax3)
ax3_2 = data_mean.plot.scatter(x='Pressure',y='PMT2',  yerr = 'PMT2_Error',c='r',label="PMT2", ax=ax3)
ax3_3 = data_mean.plot.scatter(x='Pressure',y='PMT3',  yerr = 'PMT3_Error',c='c',label="PMT3", ax=ax3)
ax3_4 = data_mean.plot.scatter(x='Pressure',y='PMT4',  yerr = 'PMT4_Error',c='m',label="PMT4", ax=ax3)
ax3_5 = data_mean.plot.scatter(x='Pressure',y='PMT5',  yerr = 'PMT5_Error',c='y',label="PMT5", ax=ax3)
ax3_6 = data_mean.plot.scatter(x='Pressure',y='PMT6',  yerr = 'PMT6_Error',c='orange',label="PMT6", ax=ax3)
ax3_7 = data_mean.plot.scatter(x='Pressure',y='PMT7',  yerr = 'PMT7_Error',c='brown',label="PMT7", ax=ax3)
ax3.set_ylabel("Counts")
ax3.legend()
ax3.set_title("Average pressure points")
ax3.grid()
plt.savefig("pdf/PMT/{}/CoincidencesAvgPoints.pdf".format(pdfname), format="pdf", bbox_inches="tight")



df['PMT0pTrigger'] = df['PMT0']/df['Trigger']
df['PMT1pTrigger'] = df['PMT1']/df['Trigger']
df['PMT2pTrigger'] = df['PMT2']/df['Trigger']
df['PMT3pTrigger'] = df['PMT3']/df['Trigger']
df['PMT4pTrigger'] = df['PMT4']/df['Trigger']
df['PMT5pTrigger'] = df['PMT5']/df['Trigger']
df['PMT6pTrigger'] = df['PMT6']/df['Trigger']
df['PMT7pTrigger'] = df['PMT7']/df['Trigger']

df = df[df["PMT0pTrigger"] <= 1]
df = df[df["PMT1pTrigger"] <= 1]
df = df[df["PMT2pTrigger"] <= 1]
df = df[df["PMT3pTrigger"] <= 1]
df = df[df["PMT4pTrigger"] <= 1]
df = df[df["PMT5pTrigger"] <= 1]
df = df[df["PMT6pTrigger"] <= 1]
df = df[df["PMT7pTrigger"] <= 1]



dfpTrigger_mean = df.groupby('Pressure', as_index=False)['PMT0pTrigger'].mean()
dfpTrigger_error = df.groupby('Pressure', as_index=False)['PMT0pTrigger'].sem()
dfpTrigger_mean['PMT0pTrigger_Error'] = dfpTrigger_error['PMT0pTrigger'].fillna(0)

dfpTrigger_mean['PMT1pTrigger'] = df.groupby('Pressure', as_index=False)['PMT1pTrigger'].mean()['PMT1pTrigger']
dfpTrigger_error = df.groupby('Pressure', as_index=False)['PMT1pTrigger'].sem()
dfpTrigger_mean['PMT1pTrigger_Error'] = dfpTrigger_error['PMT1pTrigger'].fillna(0)

dfpTrigger_mean['PMT2pTrigger'] = df.groupby('Pressure', as_index=False)['PMT2pTrigger'].mean()['PMT2pTrigger']
dfpTrigger_error = df.groupby('Pressure', as_index=False)['PMT2pTrigger'].sem()
dfpTrigger_mean['PMT2pTrigger_Error'] = dfpTrigger_error['PMT2pTrigger'].fillna(0)

dfpTrigger_mean['PMT3pTrigger'] = df.groupby('Pressure', as_index=False)['PMT3pTrigger'].mean()['PMT3pTrigger']
dfpTrigger_error = df.groupby('Pressure', as_index=False)['PMT3pTrigger'].sem()
dfpTrigger_mean['PMT3pTrigger_Error'] = dfpTrigger_error['PMT3pTrigger'].fillna(0)

dfpTrigger_mean['PMT4pTrigger'] = df.groupby('Pressure', as_index=False)['PMT4pTrigger'].mean()['PMT4pTrigger']
dfpTrigger_error = df.groupby('Pressure', as_index=False)['PMT4pTrigger'].sem()
dfpTrigger_mean['PMT4pTrigger_Error'] = dfpTrigger_error['PMT4pTrigger'].fillna(0)

dfpTrigger_mean['PMT5pTrigger'] = df.groupby('Pressure', as_index=False)['PMT5pTrigger'].mean()['PMT5pTrigger']
dfpTrigger_error = df.groupby('Pressure', as_index=False)['PMT5pTrigger'].sem()
dfpTrigger_mean['PMT5pTrigger_Error'] = dfpTrigger_error['PMT5pTrigger'].fillna(0)

dfpTrigger_mean['PMT6pTrigger'] = df.groupby('Pressure', as_index=False)['PMT6pTrigger'].mean()['PMT6pTrigger']
dfpTrigger_error = df.groupby('Pressure', as_index=False)['PMT6pTrigger'].sem()
dfpTrigger_mean['PMT6pTrigger_Error'] = dfpTrigger_error['PMT6pTrigger'].fillna(0)

dfpTrigger_mean['PMT7pTrigger'] = df.groupby('Pressure', as_index=False)['PMT7pTrigger'].mean()['PMT7pTrigger']
dfpTrigger_error = df.groupby('Pressure', as_index=False)['PMT7pTrigger'].sem()
dfpTrigger_mean['PMT7pTrigger_Error'] = dfpTrigger_error['PMT7pTrigger'].fillna(0)

ax4 = dfpTrigger_mean.plot.scatter(x='Pressure',y='PMT0pTrigger', yerr = 'PMT0pTrigger_Error', xerr=0.001, c='b',label="PMT0")
ax4_1 = dfpTrigger_mean.plot.scatter(x='Pressure',y='PMT1pTrigger', yerr = 'PMT1pTrigger_Error',xerr=0.001,c='g',label="PMT1", ax=ax4)
ax4_2 = dfpTrigger_mean.plot.scatter(x='Pressure',y='PMT2pTrigger', yerr = 'PMT2pTrigger_Error', xerr=0.001,c='r',label="PMT2", ax=ax4)
ax4_3 = dfpTrigger_mean.plot.scatter(x='Pressure',y='PMT3pTrigger', yerr = 'PMT3pTrigger_Error',xerr=0.001,c='c',label="PMT3", ax=ax4)
ax4_4 = dfpTrigger_mean.plot.scatter(x='Pressure',y='PMT4pTrigger', yerr = 'PMT4pTrigger_Error', xerr=0.001,c='m',label="PMT4", ax=ax4)
ax4_5 = dfpTrigger_mean.plot.scatter(x='Pressure',y='PMT5pTrigger', yerr = 'PMT5pTrigger_Error',xerr=0.001,c='y',label="PMT5", ax=ax4)
ax4_6 = dfpTrigger_mean.plot.scatter(x='Pressure',y='PMT6pTrigger', yerr = 'PMT6pTrigger_Error', xerr=0.001,c='orange',label="PMT6", ax=ax4)
ax4_7 = dfpTrigger_mean.plot.scatter(x='Pressure',y='PMT7pTrigger', yerr = 'PMT7pTrigger_Error',xerr=0.001,c='brown',label="PMT7", ax=ax4)
ax4.set_ylabel("Counts per trigger")
ax4.legend()
ax4.set_title("PMT counts per Trigger vs Pressure")
ax4.grid()
plt.savefig("pdf/PMT/{}/CoincidencesAvgPointspTrigger.pdf".format(pdfname), format="pdf", bbox_inches="tight")

ax5 = dfpTrigger_mean.plot.scatter(x='Pressure',y='PMT0pTrigger', yerr = 'PMT0pTrigger_Error', xerr=0.001, c='b',label="PMT0")
ax5_1 = dfpTrigger_mean.plot.scatter(x='Pressure',y='PMT1pTrigger', yerr = 'PMT1pTrigger_Error',xerr=0.001,c='g',label="PMT1", ax=ax5)
ax5_2 = dfpTrigger_mean.plot.scatter(x='Pressure',y='PMT2pTrigger', yerr = 'PMT2pTrigger_Error', xerr=0.001,c='r',label="PMT2", ax=ax5)
ax5_3 = dfpTrigger_mean.plot.scatter(x='Pressure',y='PMT3pTrigger', yerr = 'PMT3pTrigger_Error',xerr=0.001,c='c',label="PMT3", ax=ax5)
ax5_4 = dfpTrigger_mean.plot.scatter(x='Pressure',y='PMT4pTrigger', yerr = 'PMT4pTrigger_Error', xerr=0.001,c='m',label="PMT4", ax=ax5)
ax5_5 = dfpTrigger_mean.plot.scatter(x='Pressure',y='PMT5pTrigger', yerr = 'PMT5pTrigger_Error',xerr=0.001,c='y',label="PMT5", ax=ax5)
ax5_6 = dfpTrigger_mean.plot.scatter(x='Pressure',y='PMT6pTrigger', yerr = 'PMT6pTrigger_Error', xerr=0.001,c='orange',label="PMT6", ax=ax5)
ax5_7 = dfpTrigger_mean.plot.scatter(x='Pressure',y='PMT7pTrigger', yerr = 'PMT7pTrigger_Error',xerr=0.001,c='brown',label="PMT7", ax=ax5)
ax5.set_ylabel("Counts per trigger")
ax5.legend()
ax5.set_title("PMT Counts per Trigger vs Pressure")
ax5.set_yscale('log')
ax5.grid()
plt.savefig("pdf/PMT/{}/LogCoincidencesAvgPointspTrigger.pdf".format(pdfname), format="pdf", bbox_inches="tight")


df['PMT0pPMT0'] = df['PMT0pTrigger']/df['PMT0pTrigger']
df['PMT1pPMT0'] = df['PMT1pTrigger']/df['PMT0pTrigger']
df['PMT2pPMT0'] = df['PMT2pTrigger']/df['PMT0pTrigger']
df['PMT3pPMT0'] = df['PMT3pTrigger']/df['PMT0pTrigger']
df['PMT4pPMT0'] = df['PMT4pTrigger']/df['PMT0pTrigger']
df['PMT5pPMT0'] = df['PMT5pTrigger']/df['PMT0pTrigger']
df['PMT6pPMT0'] = df['PMT6pTrigger']/df['PMT0pTrigger']
df['PMT7pPMT0'] = df['PMT7pTrigger']/df['PMT0pTrigger']

dfpPM_mean = df.groupby('Pressure', as_index=False)['PMT0pPMT0'].mean()
dfpPM_error = df.groupby('Pressure', as_index=False)['PMT0pPMT0'].sem()
dfpPM_mean['PMT0pPMT0_Error'] = dfpPM_error['PMT0pPMT0'].fillna(0)

dfpPM_mean['PMT1pPMT0'] = df.groupby('Pressure', as_index=False)['PMT1pPMT0'].mean()['PMT1pPMT0']
dfpPM_error = df.groupby('Pressure', as_index=False)['PMT1pPMT0'].sem()
dfpPM_mean['PMT1pPMT0_Error'] = dfpPM_error['PMT1pPMT0'].fillna(0)

dfpPM_mean['PMT2pPMT0'] = df.groupby('Pressure', as_index=False)['PMT2pPMT0'].mean()['PMT2pPMT0']
dfpPM_error = df.groupby('Pressure', as_index=False)['PMT2pPMT0'].sem()
dfpPM_mean['PMT2pPMT0_Error'] = dfpPM_error['PMT2pPMT0'].fillna(0)

dfpPM_mean['PMT3pPMT0'] = df.groupby('Pressure', as_index=False)['PMT3pPMT0'].mean()['PMT3pPMT0']
dfpPM_error = df.groupby('Pressure', as_index=False)['PMT3pPMT0'].sem()
dfpPM_mean['PMT3pPMT0_Error'] = dfpPM_error['PMT3pPMT0'].fillna(0)

dfpPM_mean['PMT4pPMT0'] = df.groupby('Pressure', as_index=False)['PMT4pPMT0'].mean()['PMT4pPMT0']
dfpPM_error = df.groupby('Pressure', as_index=False)['PMT4pPMT0'].sem()
dfpPM_mean['PMT4pPMT0_Error'] = dfpPM_error['PMT4pPMT0'].fillna(0)

dfpPM_mean['PMT5pPMT0'] = df.groupby('Pressure', as_index=False)['PMT5pPMT0'].mean()['PMT5pPMT0']
dfpPM_error = df.groupby('Pressure', as_index=False)['PMT5pPMT0'].sem()
dfpPM_mean['PMT5pPMT0_Error'] = dfpPM_error['PMT5pPMT0'].fillna(0)

dfpPM_mean['PMT6pPMT0'] = df.groupby('Pressure', as_index=False)['PMT6pPMT0'].mean()['PMT6pPMT0']
dfpPM_error = df.groupby('Pressure', as_index=False)['PMT6pPMT0'].sem()
dfpPM_mean['PMT6pPMT0_Error'] = dfpPM_error['PMT6pPMT0'].fillna(0)

dfpPM_mean['PMT7pPMT0'] = df.groupby('Pressure', as_index=False)['PMT7pPMT0'].mean()['PMT7pPMT0']
dfpPM_error = df.groupby('Pressure', as_index=False)['PMT7pPMT0'].sem()
dfpPM_mean['PMT7pPMT0_Error'] = dfpPM_error['PMT7pPMT0'].fillna(0)

ax6 = dfpPM_mean.plot.scatter(x='Pressure',y='PMT0pPMT0', yerr = 'PMT0pPMT0_Error', xerr=0.001, c='b',label="PMT0")
ax6_1 = dfpPM_mean.plot.scatter(x='Pressure',y='PMT1pPMT0', yerr = 'PMT1pPMT0_Error',xerr=0.001,c='g',label="PMT1", ax=ax6)
ax6_2 = dfpPM_mean.plot.scatter(x='Pressure',y='PMT2pPMT0', yerr = 'PMT2pPMT0_Error', xerr=0.001,c='r',label="PMT2", ax=ax6)
ax6_3 = dfpPM_mean.plot.scatter(x='Pressure',y='PMT3pPMT0', yerr = 'PMT3pPMT0_Error',xerr=0.001,c='c',label="PMT3", ax=ax6)
ax6_4 = dfpPM_mean.plot.scatter(x='Pressure',y='PMT4pPMT0', yerr = 'PMT4pPMT0_Error', xerr=0.001,c='m',label="PMT4", ax=ax6)
ax6_5 = dfpPM_mean.plot.scatter(x='Pressure',y='PMT5pPMT0', yerr = 'PMT5pPMT0_Error',xerr=0.001,c='y',label="PMT5", ax=ax6)
ax6_6 = dfpPM_mean.plot.scatter(x='Pressure',y='PMT6pPMT0', yerr = 'PMT6pPMT0_Error', xerr=0.001,c='orange',label="PMT6", ax=ax6)
ax6_7 = dfpPM_mean.plot.scatter(x='Pressure',y='PMT7pPMT0', yerr = 'PMT7pPMT0_Error',xerr=0.001,c='brown',label="PMT7", ax=ax6)
ax6.legend()
ax6.set_title("(PMT counts per Trigger)/(PMT0 counts per Trigger) vs Pressure")
ax6.grid()
ax6.set_ylabel("PMTN/PMT0")
plt.savefig("pdf/PMT/{}/PMTPM0pTrigger.pdf".format(pdfname), format="pdf", bbox_inches="tight")


plt.show()