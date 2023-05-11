import uproot
import numpy as np
import matplotlib.pyplot as plt
import mplhep as hep
plt.style.use(hep.style.ROOT)
import pandas as pd
from csv import writer
from scipy.stats import norm
import argparse

argParser = argparse.ArgumentParser()
argParser.add_argument("-i", "--file", help="input root file")
argParser.add_argument("-x", "--MX", help="Motor X Pos")
argParser.add_argument("-y", "--MY", help="Motor Y Pos")
argParser.add_argument("-d", "--Dia", help="Diaphragm Pos")
argParser.add_argument("-e", "--eob", action='store_true', help="Eob mode")

args = argParser.parse_args()

file_name = args.file

#file_name = "rootfiles/na62om_1680601280-07-012770-1314.ds35.histos.root"
adder = ""

if(args.eob):
    adder = "_eob"

inFile = uproot.open(file_name)

#h = inFile["CEDARMC/Photonhits0")
h_NRecoHits = inFile["CedarMonitor/NRecoHits"]
h_NSectors = inFile["CedarMonitor/NSectors"]
h_NCandidates = inFile["CedarMonitor/NCandidates"]
h_NSelectedCandidates = inFile["CedarMonitor/NSelectedCandidates"]
h_NRecoHitsInCandidate = inFile["CedarMonitor/NRecoHitsInCandidate"]
h_NRecoHitsInSelectedCandidate = inFile["CedarMonitor/NRecoHitsInSelectedCandidate"]
h_NSectorsInCandidate = inFile["CedarMonitor/NSectorsInCandidate"]
h_NSectorsInSelectedCandidate = inFile["CedarMonitor/NSectorsInSelectedCandidate"]

h_NRecoHitsInSector = inFile["CedarMonitor/NRecoHitsInSector"]
h_NRecoHitsInSectorVis = inFile["CedarMonitor/NRecoHitsInSectorVis"]
h_NRecoHitsChannelProfile = inFile["CedarMonitor/NRecoHitsChannelProfile"]

h_NRecoHitsInSector = inFile["CedarMonitor/NRecoHitsInSectorVis_EOB"]

h_NRecoHitsInSector_Sec = inFile["CedarMonitor/NRecoHitsInSector_EOB"]


presure = inFile['SpecialTrigger;1']['Cedar/fDIMInfo/fDIMInfo.fPressure'].array()

pres = 0

try:
    pres = presure[1]
except ValueError:
    pass

print(pres)

fig, axs = plt.subplots(2, 2,figsize=(20,20))
ax1 = axs[0,0]
ax2 = axs[0,1]
ax3 = axs[1,0]
ax4 = axs[1,1]

# Plot 1

NHitsMax = max(h_NRecoHits.values()[1:])
print(max(h_NRecoHits.values()[1:]))    
if( max(h_NRecoHitsInCandidate.values()[1:]) > NHitsMax): 
    NHitsMax = max(h_NRecoHitsInCandidate.values()[1:])

if( max(h_NRecoHitsInSelectedCandidate.values()[1:]) > NHitsMax): 
    NHitsMax = max(h_NRecoHitsInSelectedCandidate.values()[1:])

bins_sel = h_NRecoHitsInSelectedCandidate.axis().edges()
weight_sel = h_NRecoHitsInSelectedCandidate.counts()

bins_ = h_NRecoHitsInCandidate.axis().edges()
weight_ = h_NRecoHitsInCandidate.counts()
ax1.hist(bins_[1:], bins_, weights=weight_, label="Candidate")


#mu = h_NRecoHitsInSelectedCandidate.member("fTsumwx")/h_NRecoHitsInSelectedCandidate.member("fEntries")
counts, bins, bars = ax1.hist(bins_sel[1:],bins_sel, weights=weight_sel)#, label="NHits (Sel): mu = {}".format(mu))

value = []
for i in range(len(bins[1:])):
    for t in range(int(counts[i])):
        value.append(bins[i])

mu, std = norm.fit(value)

x = np.linspace(10, 30, 100)

p = norm.pdf(x, loc=mu,scale=std)

counts_sum = sum(counts)

p = p*counts_sum

ax1.plot(x, p, 'k', linewidth=2, label="NHits (Sel): mu = {}".format(mu))
print("Fit Data: mu = {}".format(mu))

ax1.set_xlim(0,70)
ax1.set_ylim(0,NHitsMax*1.05)
ax1.legend()
ax1.set_title("Number of Reco Hits in Candidate")

# Plot2 

NSectorsMax = max(h_NSectors.values()[1:])
if( max(h_NSectorsInCandidate.values()[1:]) > NSectorsMax ):
    NSectorsMax = max(h_NSectorsInCandidate.values()[1:])
if( max(h_NSectorsInSelectedCandidate.values()[1:]) > NSectorsMax ):
    NSectorsMax = max(h_NSectorsInSelectedCandidate.values()[1:])

bins_Sec = h_NSectorsInCandidate.axis().edges()
weight_Sec = h_NSectorsInCandidate.counts()

bins_Sec_Sel = h_NSectorsInSelectedCandidate.axis().edges()
weight_Sec_Sel = h_NSectorsInSelectedCandidate.counts()

ax2.hist(bins_Sec[1:],bins_Sec ,weights=weight_Sec, label="Candiate")
ax2.hist(bins_Sec_Sel[1:],bins_Sec_Sel ,weights=weight_Sec_Sel,label="SelectedCandiate")
ax2.set_ylim(0,NSectorsMax*1.05)
ax2.set_title("Number of Sectors")
ax2.legend()

# Plot3 Asymetries

sectorTotals = [0] * 8
Min = 9999999
Max = 0

print(h_NRecoHitsInSector_Sec.values()[1:])

for i in range(8):
    sectorTotals[i] = h_NRecoHitsInSector_Sec.values()[i]
    if( sectorTotals[i] < Min):
        Min = sectorTotals[i]
    if( sectorTotals[i] > Max):
        Max = sectorTotals[i]

U = sectorTotals[7] + sectorTotals[0]
D = sectorTotals[3] + sectorTotals[4]
J = sectorTotals[5] + sectorTotals[6]
S = sectorTotals[1] + sectorTotals[2]

AsymUpDown = (U-D)/(U+D)
AsymSalvJura = (S-J)/(S+J)

ax3.plot(0,AsymUpDown*10, "o", color='r')
ax3.plot(AsymSalvJura*10,0, "o", color='g')

ax3.axline((0,-0.5),(0,0.5), color='r')
ax3.axline((-0.5,0),(0.5,0), color='g')

NE = sectorTotals[0] + sectorTotals[1]
SE = sectorTotals[2] + sectorTotals[3]
SW = sectorTotals[4] + sectorTotals[5]
NW = sectorTotals[6] + sectorTotals[7]

AsymGL = (NE-SW)/(NE+SW)
AsymMS = (NW-SE)/(NW+SE)

xGL = AsymGL*np.cos(np.pi/4)
yGL = AsymGL*np.sin(np.pi/4)

xMS = -AsymMS*np.cos(np.pi/4)
yMS = AsymMS*np.sin(np.pi/4)

ax3.plot(xGL*10,yGL*10, "o", color='b')
ax3.plot(xMS*10,yMS*10, "o", color='purple')
ax3.set_title("Asymmetry Plot")

#NW-SE line
ax3.axline((-0.5*np.sin(np.pi/4),0.5*np.cos(np.pi/4)),(0.5*np.cos(np.pi/4),-0.5*np.sin(np.pi/4)),color='purple')
#Jura-Saleve line
ax3.axline((-0.5*np.sin(np.pi/4),-0.5*np.cos(np.pi/4)),(0.5*np.cos(np.pi/4),0.5*np.sin(np.pi/4)),color='b')

ax3.set_ylim(-10,10)
ax3.set_xlim(-10,10)

#Plot 4

bins_Sec_x = h_NSectorsInCandidate.axis("x").edges()
weight_Sec_x = h_NSectorsInCandidate.counts()

hist = h_NRecoHitsInSector.to_hist()
hep.hist2dplot(hist, ax=ax4, cmin=1)
run = file_name[-21:-15]
cur_Burst = inFile['SpecialTrigger;1']['EventHeader/fBurstID'].array()[0]

save_file = "output/{}.{}.plots.png".format(run,cur_Burst)
plt.savefig(save_file)

fig, axT = plt.subplots(1,1,figsize=(10,10))
#Table
NMeanHitsForKCand = np.mean(h_NRecoHitsInSelectedCandidate.values()[1:])

cur_M_X = inFile['SpecialTrigger;1']['Cedar/fDIMInfo/fDIMInfo.fMotorPosX'].array()[1]
cur_M_Y = inFile['SpecialTrigger;1']['Cedar/fDIMInfo/fDIMInfo.fMotorPosY'].array()[1]
cur_Do = 2.091 #inFile['SpecialTrigger;1']['Cedar/fDIMInfo/fDIMInfo.Diaph'].array()[1]
myCsvRow = [cur_Burst,cur_M_X,cur_M_Y,cur_Do,round(1000*NMeanHitsForKCand)/1000,round(1000*AsymUpDown)/1000,round(100*AsymSalvJura)/1000,round(100*AsymGL)/1000,round(1000*AsymMS)/1000]
with open('csv/prevdata.csv','a',newline='') as fd:
    writer_object = writer(fd)
    writer_object.writerow(myCsvRow)
    fd.close()
    
data = pd.read_csv("csv/prevdata.csv")
Burst = data['Burst'][-7:].tolist()
M_X = data['M_X'][-7:].tolist()
M_Y = data['M_Y'][-7:].tolist()
D_o = data['D_o'][-7:].tolist()
nHits = data['nHits'][-7:].tolist()
A_UD = data['A_UD'][-7:].tolist()
A_SJ = data['A_SJ'][-7:].tolist()
A_GL = data['A_GL'][-7:].tolist()
A_MS = data['A_MS'][-7:].tolist()

print(A_MS)
table_entries = []
for i in range(len(Burst)):
    table_entries.append([Burst[i],M_X[i],M_Y[i],D_o[i],nHits[i],A_UD[i],A_SJ[i],A_GL[i],A_MS[i]])
col_title = ["Burst","M_X","M_Y","D_o","nHits","A_UD","A_SJ","A_GL","A_MS"]

the_table = axT.table(cellText=table_entries,colLabels=col_title,loc='center')
the_table.scale(1, 5)
the_table.set_fontsize(20)
axT.axis("off")

save_file = "output/{}.{}.table.png".format(run,cur_Burst)
plt.savefig(save_file)
plt.show()