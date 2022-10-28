from tokenize import Double
import pandas as pd
import csv
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import math 
import mplhep as hep
plt.style.use(hep.style.ROOT)
from os import listdir
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

filename = 'formated_data/TIMBER_data.{}.csv'.format(date_time)

with open(chosenFile, 'r') as inp, open(filename, 'w') as out:
    writer = csv.writer(out)
    r = 0
    PMTRows = []
    pRows = [0]
    miss = 0
    pressure = False 
   
    for row in csv.reader(inp):
        if r >= 2:
            if r == 2:   
                head = [row[0],"PMT0","PMT1","PMT2","PMT3","PMT4","PMT5","PMT6","PMT7","6Fold","7Fold","8Fold","Trigger","TotalHits","Pressure"]
                PMTRows.append(head)  
            elif row == ['VARIABLE: XBH6.XCED.041.440:PRESSURE']:
                
                miss = 3
                pressure = True
            elif miss == 0:
                if pressure:
                    #print(row[1])
                    try: 
                        pres = math.floor(float(row[1])*1000)/1000
                        pRows.append([row[0],pres])
                    except ValueError:
                        print("on line", row)
                else:
                    #print(row)
                    totalHits = 0
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
    writer.writerows(PMTRows)

df = pd.read_csv(filename)
df['Timestamp (UTC_TIME)'] = pd.to_datetime(df['Timestamp (UTC_TIME)'])


data_mean = df.groupby('Pressure', as_index=False)['6Fold'].mean()
data_error = df.groupby('Pressure', as_index=False)['6Fold'].sem()
data_mean['6Fold_Error'] = data_error['6Fold'].fillna(0)

data_mean['7Fold'] = df.groupby('Pressure', as_index=False)['7Fold'].mean()['7Fold']
data_error = df.groupby('Pressure', as_index=False)['7Fold'].sem()
data_mean['7Fold_Error'] = data_error['7Fold'].fillna(0)

data_mean['8Fold'] = df.groupby('Pressure', as_index=False)['8Fold'].mean()['8Fold']
data_error = df.groupby('Pressure', as_index=False)['8Fold'].sem()
data_mean['8Fold_Error'] = data_error['8Fold'].fillna(0)


ax1 = df.plot.scatter(x='Timestamp (UTC_TIME)',y='Pressure', c='DarkBlue')

ax2 = df.plot.scatter(x='Pressure',y='6Fold', c='DarkBlue',label="6Fold")
ax2_1 = df.plot.scatter(x='Pressure',y='7Fold', c='red' , label="7Fold", ax=ax2)
ax2_2 = df.plot.scatter(x='Pressure',y='8Fold', c='green', label="8Fold", ax=ax2)
ax2.set_ylabel("Counts")
ax2.legend()
ax2.set_title("All pressure points")

ax3 = data_mean.plot.scatter(x='Pressure',y='6Fold', yerr = '6Fold_Error', c='DarkBlue',label="6Fold")
ax3_1 = data_mean.plot.scatter(x='Pressure',y='7Fold', yerr = '7Fold_Error',c='red' , label="7Fold", ax=ax3)
ax3_2 = data_mean.plot.scatter(x='Pressure',y='8Fold', yerr = '8Fold_Error', c='green', label="8Fold", ax=ax3)
ax3.set_ylabel("Counts")
ax3.legend()
ax3.set_title("Average pressure points")


plt.show()