import matplotlib.pyplot as plt
import mplhep as hep
plt.style.use(hep.style.ROOT)

infile = 'AlignmentValues.txt'
values = [] 
with open(infile , 'r') as inp:
    for row in inp:
        if row[0] == '#':
            continue
        
        values.append(row.split(' '))
        
lastValue = values[-1]
iD = int(lastValue[0])
pmts = lastValue[1:9]
trigger = int(lastValue[9])
xval = float(lastValue[10])
yval = float(lastValue[11])


pmtptrigger = [int(x) / trigger for x in pmts]
avrgs = []
# Creats the avrgs for the pmt values:
# 01 12 23 34 45 56 67 70
# PMT positions
#       0       1
#   7               2
#
#   6               3
#       5       4       

for i in range(len(pmtptrigger)):
    if i+1 < 8:
        avrgs.append((pmtptrigger[i]+pmtptrigger[i+1])/2)
    else: 
        avrgs.append((pmtptrigger[i]+pmtptrigger[0])/2)
        
print(avrgs)
diffs = []
diffs.append([0,(avrgs[0]-avrgs[4])])
diffs.append([(avrgs[2]-avrgs[6]),0])
diffs.append([(avrgs[1]-avrgs[5]),(avrgs[1]-avrgs[5])])
diffs.append([(avrgs[3]-avrgs[7]),-(avrgs[3]-avrgs[7])])

fig = plt.figure()
ax1 = fig.add_subplot(111)

ax1.plot([0, 0], [0.5, -0.5],linestyle='--')
ax1.plot([0.5, -0.5], [0, 0],linestyle='--')
ax1.plot([0.5, -0.5], [.5, -0.5],linestyle='--')
ax1.plot([0.5, -0.5], [-.5, 0.5],linestyle='--')

for t in range(len(diffs)):
    ax1.scatter(diffs[t][0],diffs[t][1])
    
ax1.set_title("Cedar Alignment Check")
plt.show()
