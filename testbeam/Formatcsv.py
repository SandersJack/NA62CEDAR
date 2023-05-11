import csv
from datetime import datetime

now = datetime.now() # current date and time
date_time = now.strftime("%m-%d_%H-%M-%S")

with open('timbers/TIMBER_data.csv', 'r') as inp, open('formated_data/TIMBER_data.{}.csv'.format(date_time), 'w') as out:
    writer = csv.writer(out)
    r = 0
    PMTRows = []
    pRows = []
    miss = 0
    pressure = False 
   
    for row in csv.reader(inp):
        if r >= 2:
            #print(row)
            if r == 2:   
                head = [row[0],"PMT0","PMT1","PMT2","PMT3","PMT4","PMT5","PMT6","PMT7","TotalHits","Pressure"]
                PMTRows.append(head)  
            elif row == ['VARIABLE: XBH6.XCED.041.440:PRESSURE']:
                
                miss = 2
                pressure = True
            elif miss == 0:
                if pressure:
                    pRows.append(row)
                else:
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
        
