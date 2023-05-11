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


df = pd.read_csv(outfile)
df['Timestamp (UTC_TIME)'] = pd.to_datetime(df['Timestamp (UTC_TIME)'])


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
ax2.legend()
ax2.set_title("All Diaphragm points")
plt.savefig("pdf/Diaphragm/{}/CoincidencesAllPoints.pdf".format(pdfname), format="pdf", bbox_inches="tight")

ax3 = data_mean.plot.scatter(x='Diaphragm',y='6Fold', yerr = '6Fold_Error', c='DarkBlue',label="6Fold")
ax3_1 = data_mean.plot.scatter(x='Diaphragm',y='7Fold', yerr = '7Fold_Error',c='red' , label="7Fold", ax=ax3)
ax3_2 = data_mean.plot.scatter(x='Diaphragm',y='8Fold', yerr = '8Fold_Error', c='green', label="8Fold", ax=ax3)
ax3.set_ylabel("Coincidences")
ax3.legend()
ax3.set_title("Average Diaphragm points")
plt.savefig("pdf/Diaphragm/{}/CoincidencesAvgPoints.pdf".format(pdfname), format="pdf", bbox_inches="tight")



df['6FoldpTrigger'] = df['6Fold']/df['Trigger']
df['7FoldpTrigger'] = df['7Fold']/df['Trigger']
df['8FoldpTrigger'] = df['8Fold']/df['Trigger']

dfpTrigger_mean = df.groupby('Diaphragm', as_index=False)['6FoldpTrigger'].mean()
dfpTrigger_error = df.groupby('Diaphragm', as_index=False)['6FoldpTrigger'].sem()
dfpTrigger_mean['6FoldpTrigger_Error'] = dfpTrigger_error['6FoldpTrigger'].fillna(0)

dfpTrigger_mean['7FoldpTrigger'] = df.groupby('Diaphragm', as_index=False)['7FoldpTrigger'].mean()['7FoldpTrigger']
dfpTrigger_error = df.groupby('Diaphragm', as_index=False)['7FoldpTrigger'].sem()
dfpTrigger_mean['7FoldpTrigger_Error'] = dfpTrigger_error['7FoldpTrigger'].fillna(0)

dfpTrigger_mean['8FoldpTrigger'] = df.groupby('Diaphragm', as_index=False)['8FoldpTrigger'].mean()['8FoldpTrigger']
dfpTrigger_error = df.groupby('Diaphragm', as_index=False)['8FoldpTrigger'].sem()
dfpTrigger_mean['8FoldpTrigger_Error'] = dfpTrigger_error['8FoldpTrigger'].fillna(0)

ax4 = dfpTrigger_mean.plot.scatter(x='Diaphragm',y='6FoldpTrigger', yerr = '6FoldpTrigger_Error', xerr=0.001, c='DarkBlue',label="6Fold")
ax4_1 = dfpTrigger_mean.plot.scatter(x='Diaphragm',y='7FoldpTrigger', yerr = '7FoldpTrigger_Error',xerr=0.001,c='red' , label="7Fold", ax=ax4)
ax4_2 = dfpTrigger_mean.plot.scatter(x='Diaphragm',y='8FoldpTrigger', yerr = '8FoldpTrigger_Error', xerr=0.001,c='green', label="8Fold", ax=ax4)
ax4.set_ylabel("Coincidences per trigger")
ax4.legend()
ax4.set_title("At Least N Coincidences per Trigger vs Diaphragm")
plt.savefig("pdf/Diaphragm/{}/CoincidencesAvgPointspTrigger.pdf".format(pdfname), format="pdf", bbox_inches="tight")

ax42 = dfpTrigger_mean.plot.scatter(x='Diaphragm',y='6FoldpTrigger', yerr = '6FoldpTrigger_Error', xerr=0.001, c='DarkBlue',label="6Fold")
ax42_1 = dfpTrigger_mean.plot.scatter(x='Diaphragm',y='7FoldpTrigger', yerr = '7FoldpTrigger_Error',xerr=0.001,c='red' , label="7Fold", ax=ax42)
ax42_2 = dfpTrigger_mean.plot.scatter(x='Diaphragm',y='8FoldpTrigger', yerr = '8FoldpTrigger_Error', xerr=0.001,c='green', label="8Fold", ax=ax42)
ax42.set_ylabel("Coincidences per trigger")
ax42.set_xlim(0,4)
ax42.set_ylim(0,.8)
ax42.legend()
ax42.set_title("At Least N Coincidences per Trigger vs Diaphragm")
plt.savefig("pdf/Diaphragm/{}/CoincidencesAvgPointspTriggerclose.pdf".format(pdfname), format="pdf", bbox_inches="tight")

ax5 = dfpTrigger_mean.plot.scatter(x='Diaphragm',y='6FoldpTrigger', yerr = '6FoldpTrigger_Error', xerr=0.001, c='DarkBlue',label="6Fold")
ax5_1 = dfpTrigger_mean.plot.scatter(x='Diaphragm',y='7FoldpTrigger', yerr = '7FoldpTrigger_Error',xerr=0.001,c='red' , label="7Fold", ax=ax5)
ax5_2 = dfpTrigger_mean.plot.scatter(x='Diaphragm',y='8FoldpTrigger', yerr = '8FoldpTrigger_Error', xerr=0.001,c='green', label="8Fold", ax=ax5)
ax5.set_ylabel("Coincidences per trigger")
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
ax6.legend()
plt.savefig("pdf/Diaphragm/{}/RatioPlot.pdf".format(pdfname), format="pdf", bbox_inches="tight")

plt.show()