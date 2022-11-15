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
import seaborn as sns

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
    hRows = [0]
    vRows = [0]
    miss = 0
    pressure = False 
    positionH = False
    positionV = False
    for row in csv.reader(inp):
        if r >= 2:
            if r == 2:   
                head = [row[0],"PMT0","PMT1","PMT2","PMT3","PMT4","PMT5","PMT6","PMT7","6Fold","7Fold","8Fold","Trigger","TotalHits","POS_H","POS_V","Pressure"]
                PMTRows.append(head)  
            elif row == ['VARIABLE: XBH6.XCED.041.440:PRESSURE']:
                
                miss = 3
                pressure = True
                positionH = False
                positionV = False
            elif row == ['VARIABLE: XBH6.XCED.041.440:POS_H']:
                
                miss = 3
                positionH = True
                pressure = False
                positionV = False
            elif row == ['VARIABLE: XBH6.XCED.041.440:POS_V']:
                miss = 3
                positionV = True
                pressure = False
                positionH = False
            elif miss == 0:
                if pressure:
                    try: 
                        pres = math.floor(float(row[1])*1000)/1000
                        pRows.append([row[0],pres])
                    except ValueError:
                        print("on line", row)
                if positionH:
                    try: 
                        hor = math.floor(float(row[1])*10)/10
                        hRows.append([row[0],hor])
                    except ValueError:
                        print("on line", row)
                if positionV:
                    try: 
                        vert = math.floor(float(row[1])*10)/10
                        vRows.append([row[0],vert])
                    except ValueError:
                        print("on line", row)
                if pressure == False and positionV == False and positionH == False:
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
            PMTRows[t].append(hRows[t][1])
            PMTRows[t].append(vRows[t][1])
            PMTRows[t].append(pRows[t][1])
    
    t1t2 = PMTRows[1][0].replace(" ", ".").replace(":", "-").replace(".", "-")+"_"+PMTRows[-1][0].replace(" ", ".").replace(":", "-").replace(".", "-")
    outfile = str("formated_data/Alignment/Timber_data."+t1t2+".csv")
    if path.exists(outfile) == False:
        with open(outfile, 'w') as out:
            writer = csv.writer(out)
            writer.writerows(PMTRows)
            ### Write a log file entry ###
            logtext = str(t1t2) 
            print("Is this CEDAR using H or N?")
            while True:
                gas_type = input().capitalize()
                if gas_type == "H" or gas_type == "N":
                    logtext += " --- Gas Type: {} - ".format(gas_type)
                    break
                else:
                    print("Please input either H or N")
                
            print("Add a comment below")
            com = input()
            logtext += com

            file_object = open('pdf/logbook.txt', 'a')
            file_object.write('\n'+ logtext )
            file_object.close()


df = pd.read_csv(outfile)
df['Timestamp (UTC_TIME)'] = pd.to_datetime(df['Timestamp (UTC_TIME)'])

df['8FoldpTrigger'] = df['8Fold']/df['Trigger']

position_mean = df.groupby(['POS_H','POS_V'], as_index=False)['8FoldpTrigger'].mean()

plt.hexbin(x=position_mean['POS_H'],y=position_mean['POS_V'], C=position_mean['8FoldpTrigger'],gridsize = 50)
plt.xlabel("Horizontal Azis [mm]")
plt.ylabel("Vertical Azis [mm]")
plt.title("Phase Space plot of X-Y postion")
plt.colorbar(label="8Fold Coincidences per Trigger")
plt.show()