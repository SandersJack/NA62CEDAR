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
from matplotlib.lines import Line2D

'''
# List all files in directory timbers
mypath = 'timbers/'
files = []
print('Choose which Timber Files to use')
p = 0
for f in listdir(mypath):
    print('{} {}'.format(p,f))
    files.append(join(mypath, f))
    p += 1

try:
    chosenIndex = int(input())
    if chosenIndex < len(files):
        chosenFile = files[chosenIndex]
    else:
        raise ValueError
except ValueError:
    print("Invalid Entry, Has to be an integer and a valid index")
    exit(0)

################################################
# Formating the csv File for use in data-frame #
################################################
now = datetime.now() # current date and time
date_time = now.strftime("%m-%d_%H-%M-%S")


with open(chosenFile, 'r') as inp:
    r = 0
    PMTRows = []
    pRows = [0]
    miss = 0
    pressure = False 
   
    for row in csv.reader(inp):
        if r >= 2:
            if r == 2:   
                head = [row[0],"PMT0","PMT1","PMT2","PMT3","PMT4","PMT5","PMT6","PMT7","6Fold","7Fold","8Fold","Trigger","TotalHits","Diaphragm"]
                PMTRows.append(head)  
            elif row == ['VARIABLE: XBH6.XCED.041.440:DIAPHRAGM']:
                
                miss = 3
                pressure = True
            elif miss == 0:
                if pressure:
                    try: 
                        pres = math.floor(float(row[1])*1000)/1000
                        pRows.append([row[0],pres])
                    except ValueError:
                        print("on line", row)
                else:
                    totalHits = 0
                    #print(row)
                    for i in range(1,9):
                        totalHits += int(row[i])
                    row.append(totalHits)
                    PMTRows.append(row)
            if miss > 0:    
                miss -= 1
        r += 1
        
    newRows = [] 
    for t in range(len(PMTRows)):
        if t > 0: 
            PMTRows[t].append(pRows[t][1])
    
    t1t2 = PMTRows[1][0].replace(" ", ".").replace(":", "-").replace(".", "-")+"_"+PMTRows[-1][0].replace(" ", ".").replace(":", "-").replace(".", "-")
    outfile = str("formated_data/Diaphragm/Timber_data."+t1t2+".csv")
    if path.exists(outfile) == False:
        with open(outfile, 'w') as out:
            writer = csv.writer(out)
            writer.writerows(PMTRows)
            ### Write a log file entry ###
            logtext = str(t1t2) 
            print("Is this CEDAR using H, N or HN?")
            while True:
                gas_type = input().upper()
                print(gas_type)
                if gas_type == "H" or gas_type == "N" or gas_type == "HN":
                    logtext += " --- Gas Type: {} - ".format(gas_type)
                    break
                else:
                    print("Please input either H, N or HN")
                
            print("Add a comment below")
            com = input()
            logtext += com

            file_object = open('pdf/logbook.txt', 'a')
            file_object.write('\n'+ logtext )
            file_object.close()

'''
df = pd.read_csv("formated_data\Diaphragm\Timber_data.2022-11-07-20-42-31-335_2022-11-07-20-59-04-935.csv")
df['Timestamp (UTC_TIME)'] = pd.to_datetime(df['Timestamp (UTC_TIME)'])

plt.rcParams['figure.constrained_layout.use'] = True

data_mean = df.groupby('Diaphragm', as_index=False)['6Fold'].mean()
data_error = df.groupby('Diaphragm', as_index=False)['6Fold'].sem()
data_mean['6Fold_Error'] = data_error['6Fold'].fillna(0)

data_mean['7Fold'] = df.groupby('Diaphragm', as_index=False)['7Fold'].mean()['7Fold']
data_error = df.groupby('Diaphragm', as_index=False)['7Fold'].sem()
data_mean['7Fold_Error'] = data_error['7Fold'].fillna(0)

data_mean['8Fold'] = df.groupby('Diaphragm', as_index=False)['8Fold'].mean()['8Fold']
data_error = df.groupby('Diaphragm', as_index=False)['8Fold'].sem()
data_mean['8Fold_Error'] = data_error['8Fold'].fillna(0)

pdfname = str(df['Timestamp (UTC_TIME)'].iloc[0].strftime('%m-%d_%H-%M')) + "--" + str(df['Timestamp (UTC_TIME)'].iloc[-1].strftime('%m-%d_%H-%M'))
try:
    makedirs('pdf/Diaphragm/{}'.format(pdfname))
except FileExistsError:
    pass

ax1 = df.plot.scatter(x='Timestamp (UTC_TIME)',y='Diaphragm', c='DarkBlue')
plt.savefig("pdf/Diaphragm/{}/Diaphragm.pdf".format(pdfname), format="pdf", bbox_inches="tight")

ax2 = df.plot.scatter(x='Diaphragm',y='6Fold', c='DarkBlue',label="6Fold")
ax2_1 = df.plot.scatter(x='Diaphragm',y='7Fold', c='red' , label="7Fold", ax=ax2)
ax2_2 = df.plot.scatter(x='Diaphragm',y='8Fold', c='green', label="8Fold", ax=ax2)
ax2.set_ylabel("Coincidences")
ax2.set_xlabel("Diaphragm aperture [mm]")
ax2.legend()
ax2.set_title("All Diaphragm points")
plt.savefig("pdf/Diaphragm/{}/CoincidencesAllPoints.pdf".format(pdfname), format="pdf", bbox_inches="tight")

ax3 = data_mean.plot.scatter(x='Diaphragm',y='6Fold', yerr = '6Fold_Error', c='DarkBlue',label="6Fold")
ax3_1 = data_mean.plot.scatter(x='Diaphragm',y='7Fold', yerr = '7Fold_Error',c='red' , label="7Fold", ax=ax3)
ax3_2 = data_mean.plot.scatter(x='Diaphragm',y='8Fold', yerr = '8Fold_Error', c='green', label="8Fold", ax=ax3)
ax3.set_ylabel("Coincidences")
ax3.set_xlabel("Diaphragm aperture [mm]")
ax3.legend()
ax3.set_title("Average Diaphragm points")
plt.savefig("pdf/Diaphragm/{}/CoincidencesAvgPoints.pdf".format(pdfname), format="pdf", bbox_inches="tight")



df['6FoldpTrigger'] = df['6Fold']/df['Trigger']
df['7FoldpTrigger'] = df['7Fold']/df['Trigger']
df['8FoldpTrigger'] = df['8Fold']/df['Trigger']


pres = df['Diaphragm'].values.tolist()
fold = df['6FoldpTrigger'].values.tolist()

dfpTrigger_mean = df.groupby('Diaphragm', as_index=False)['Diaphragm','6FoldpTrigger']
df = df.drop(31)
df = df.drop(24)
df = df.drop(4)
df = df.drop(9)
df = df.drop(8)
df = df.drop(3)
df = df.drop(13)
df = df.drop(5)
print(df[df['Diaphragm'].between(18.5, 20.5)])


dfpTrigger_mean = df.groupby('Diaphragm', as_index=False)['6FoldpTrigger'].mean()
dfpTrigger_error = df.groupby('Diaphragm', as_index=False)['6FoldpTrigger'].sem()
dfpTrigger_mean['6FoldpTrigger_Error'] = dfpTrigger_error['6FoldpTrigger'].fillna(0)

dfpTrigger_mean['7FoldpTrigger'] = df.groupby('Diaphragm', as_index=False)['7FoldpTrigger'].mean()['7FoldpTrigger']
dfpTrigger_error = df.groupby('Diaphragm', as_index=False)['7FoldpTrigger'].sem()
dfpTrigger_mean['7FoldpTrigger_Error'] = dfpTrigger_error['7FoldpTrigger'].fillna(0)

dfpTrigger_mean['8FoldpTrigger'] = df.groupby('Diaphragm', as_index=False)['8FoldpTrigger'].mean()['8FoldpTrigger']
dfpTrigger_error = df.groupby('Diaphragm', as_index=False)['8FoldpTrigger'].sem()
dfpTrigger_mean['8FoldpTrigger_Error'] = dfpTrigger_error['8FoldpTrigger'].fillna(0)

size_marker = 40

ax4 = dfpTrigger_mean.plot.scatter(x='Diaphragm',y='6FoldpTrigger', yerr = '6FoldpTrigger_Error', xerr=0.001, c='DarkBlue',label="6-fold",marker="s",s=size_marker)
ax4_1 = dfpTrigger_mean.plot.scatter(x='Diaphragm',y='7FoldpTrigger', yerr = '7FoldpTrigger_Error',xerr=0.001,c='red' , label="7-fold", ax=ax4, marker="^",s=size_marker)
ax4_2 = dfpTrigger_mean.plot.scatter(x='Diaphragm',y='8FoldpTrigger', yerr = '8FoldpTrigger_Error', xerr=0.001,c='green', label="8-fold", ax=ax4, marker="o",s=size_marker)

dfpTrigger_mean.plot.line(x='Diaphragm',y='6FoldpTrigger', c='DarkBlue',ax=ax4,marker="s",markersize =0, ls="--")
dfpTrigger_mean.plot.line(x='Diaphragm',y='7FoldpTrigger',c='red', ax=ax4, marker="^",markersize =0, ls="--")
dfpTrigger_mean.plot.line(x='Diaphragm',y='8FoldpTrigger',c='green', ax=ax4, marker="o",markersize =0, ls="--")

ax4.set_ylabel("Coincidences per trigger", fontsize=30)
ax4.set_xlabel("Diaphragm aperture [mm]", fontsize=30)
ax4.set_xlim(0,20.001)
ax4.set_ylim(0,1.04)
#ax4.tick_params(axis='both', which='major', pad=10)

#ax4.legend(prop={'size': 30})
def create_dummy_line(**kwds):
    return Line2D([], [], **kwds)


lines = [
    ('6-fold', {'color': 'DarkBlue','linestyle': '--', 'marker': 's'}),
    ("7-fold", {'color': 'red', 'linestyle': '--', 'marker': '^'}),
    ('8-fold', {'color': 'green', 'linestyle': '--', 'marker': 'o'}),
]
ax4.legend(
    # Line handles
    [create_dummy_line(**l[1]) for l in lines],
    # Line titles
    [l[0] for l in lines],
    loc='upper left',
    prop={'size': 30}
)

for axis in ['top', 'bottom', 'left', 'right']:
        ax4.spines[axis].set_linewidth(2.5)

ax4.tick_params(axis='both', which='major', pad=10, labelsize=30)

ax4.tick_params(axis="both", which="major", length=20, width=2) 
ax4.tick_params(axis="both", which="minor", length=10, width=2)

#ax4.set_title("At Least N Coincidences per Trigger vs Diaphragm")
plt.savefig("pdf/Diaphragm/{}/DiaScan_CoincidencesAvgPointspTrigger.pdf".format(pdfname), format="pdf", bbox_inches="tight")
plt.show()
exit(0)
ax42 = dfpTrigger_mean.plot.scatter(x='Diaphragm',y='6FoldpTrigger', yerr = '6FoldpTrigger_Error', xerr=0.001, c='DarkBlue',label="6Fold")
ax42_1 = dfpTrigger_mean.plot.scatter(x='Diaphragm',y='7FoldpTrigger', yerr = '7FoldpTrigger_Error',xerr=0.001,c='red' , label="7Fold", ax=ax42)
ax42_2 = dfpTrigger_mean.plot.scatter(x='Diaphragm',y='8FoldpTrigger', yerr = '8FoldpTrigger_Error', xerr=0.001,c='green', label="8Fold", ax=ax42)
ax42.set_ylabel("Coincidences per trigger")
ax42.set_xlabel("Diaphragm aperture [mm]")
ax42.set_xlim(0,4)
ax42.set_ylim(0,.8)
ax42.legend()
ax42.set_title("At Least N Coincidences per Trigger vs Diaphragm")
plt.savefig("pdf/Diaphragm/{}/CoincidencesAvgPointspTriggerclose.pdf".format(pdfname), format="pdf", bbox_inches="tight")

ax5 = dfpTrigger_mean.plot.scatter(x='Diaphragm',y='6FoldpTrigger', yerr = '6FoldpTrigger_Error', xerr=0.001, c='DarkBlue',label="6Fold")
ax5_1 = dfpTrigger_mean.plot.scatter(x='Diaphragm',y='7FoldpTrigger', yerr = '7FoldpTrigger_Error',xerr=0.001,c='red' , label="7Fold", ax=ax5)
ax5_2 = dfpTrigger_mean.plot.scatter(x='Diaphragm',y='8FoldpTrigger', yerr = '8FoldpTrigger_Error', xerr=0.001,c='green', label="8Fold", ax=ax5)
ax5.set_ylabel("Coincidences per trigger")
ax5.set_xlabel("Diaphragm aperture [mm]")
ax5.legend()
ax5.set_title("At Least N Coincidences per Trigger vs Diaphragm")
ax5.set_yscale('log')
plt.savefig("pdf/Diaphragm/{}/LogCoincidencesAvgPointspTrigger.pdf".format(pdfname), format="pdf", bbox_inches="tight")

df['R76'] = df['7Fold']/df['6Fold']
df['R87'] = df['8Fold']/df['7Fold']

dRatio_mean = df.groupby('Diaphragm', as_index=False)['R76'].mean()
dRatio_error = df.groupby('Diaphragm', as_index=False)['R76'].sem()
dRatio_mean['R76_Error'] = dRatio_error['R76'].fillna(0)

dRatio_mean['R87'] = df.groupby('Diaphragm', as_index=False)['R87'].mean()['R87']
dRatio_error = df.groupby('Diaphragm', as_index=False)['R87'].sem()
dRatio_mean['R87_Error'] = dRatio_error['R87'].fillna(0)

ax6 = dRatio_mean.plot.scatter(x='Diaphragm',y='R76', yerr = 'R76_Error', xerr=0.001, c='DarkBlue',label="R76")
ax6_1 = dRatio_mean.plot.scatter(x='Diaphragm',y='R87', yerr = 'R87_Error',xerr=0.001,c='red' , label="R87", ax=ax6)
ax6.set_ylabel("Ratio")
ax6.set_xlabel("Diaphragm aperture [mm]")
ax6.legend()
plt.savefig("pdf/Diaphragm/{}/RatioPlot.pdf".format(pdfname), format="pdf", bbox_inches="tight")

plt.show()