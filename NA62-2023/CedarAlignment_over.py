import uproot
import numpy as np
import matplotlib.pyplot as plt
#import mplhep as hep
#plt.style.use(hep.style.ROOT)
import pandas as pd
from csv import writer
from scipy.stats import norm
import argparse
import os
import seaborn as sns

#directory = '/afs/cern.ch/work/j/jsanders/Software/bugfix/develop/na62fw/NA62Reconstruction/Alignment_H/'
directory = '/eos/user/j/jsanders/cedar_roots/Alignment_H2/'

#directory = '/eos/user/j/jsanders/condorout/4914447/reco/'

c = 0

Motor_x = []
Motor_y = []
Nhits = []

for filename in os.scandir(directory):
    if filename.is_file():
        
        if "tar" in filename.path:
            continue
        
        if ".root" not in filename.path:
            continue


        try: 
            inFile = uproot.open(filename)
        except ValueError:
            continue
        except OSError:
            continue

        #h = inFile["CEDARMC/Photonhits0")
        h_NRecoHitsInSelectedCandidate = inFile["CedarMonitor/NRecoHitsInSelectedCandidate"]
        
        h_NSectorsInSelectedCandidate = inFile["CedarMonitor/NSectorsInSelectedCandidate"]
        
        cur_M_X = min(inFile['SpecialTrigger;1']['Cedar/fDIMInfo/fDIMInfo.fMotorPosX'].array())
        cur_M_Y = min(inFile['SpecialTrigger;1']['Cedar/fDIMInfo/fDIMInfo.fMotorPosY'].array())

        burst = inFile['SpecialTrigger;1']['EventHeader/fBurstID'].array()[0]
        
        print(burst)
        
        #if(burst) < 90:
        #    continue 


        fig, axs = plt.subplots(1, 1,figsize=(10,10))
        ax1 = axs

        # Plot 1

        bins_sel = h_NRecoHitsInSelectedCandidate.axis().edges()
        weight_sel = h_NRecoHitsInSelectedCandidate.counts()

        #mu = h_NRecoHitsInSelectedCandidate.member("fTsumwx")/h_NRecoHitsInSelectedCandidate.member("fEntries")
        counts, bins, bars = ax1.hist(bins_sel[1:],bins_sel, weights=weight_sel)#, label="NHits (Sel): mu = {}".format(mu))

        value = []
        for i in range(len(bins[1:])):
            for t in range(int(counts[i])):
                value.append(bins[i])

        mu, std = norm.fit(value)
        
        if mu < 15:
            continue

        Nhits.append(mu)
        Motor_x.append((round(cur_M_X*1000)/1000))
        Motor_y.append((round(cur_M_Y*1000)/1000))
        
        x = np.linspace(10, 30, 100)

        p = norm.pdf(x, loc=mu,scale=std)

        counts_sum = sum(counts)

        p = p*counts_sum

        ax1.plot(x, p, 'k', linewidth=2, label="NHits (Sel): mu = {}".format(mu))
        print("Fit Data: mu = {}".format(mu))

        ax1.set_xlim(0,40)
        ax1.legend()
        ax1.set_title("Number of Reco Hits in Candidate")
        
        plt.clf()
        plt.close()
        
        

        #if c >50:
        #    break 
        #c +=10
        '''
        fig, ax2 = plt.subplots(1, 1,figsize=(10,10))

        bins_Sec_Sel = h_NSectorsInSelectedCandidate.axis().edges()
        weight_Sec_Sel = h_NSectorsInSelectedCandidate.counts()

        ax2.hist(bins_Sec_Sel[1:],bins_Sec_Sel ,weights=weight_Sec_Sel,label="SelectedCandiate")
        ax2.set_title("Number of Sectors")
        ax2.legend()
        '''
        # Plot3 Asymetries
        '''
        sectorTotals = [0] * 8
        Min = 9999999
        Max = 0

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

'''

fig, axs = plt.subplots(1, 1,figsize=(10,10))

axs.plot(Motor_x,Nhits)
axs.set_xlabel("X motor [mm]")
axs.set_ylabel("Nhits in Selected Candidate")

fig, axs2 = plt.subplots(1, 1,figsize=(10,10))

axs2.plot(Motor_y,Nhits)
axs2.set_xlabel("Y motor [mm]")
axs2.set_ylabel("Nhits in Selected Candidate")

fig, axs3 = plt.subplots(1, 1,figsize=(10,10))


#axs3.pcolormesh(Motor_x,Motor_y,Nhits)

Nhits = np.array(Nhits)
Motor_x = np.array(Motor_x)
Motor_y = np.array(Motor_y)


#df = pd.DataFrame(data=[Nhits], columns=Motor_x, index=Motor_y)
df = pd.DataFrame(list(zip(Motor_x, Motor_y,Nhits)),columns =['MotorX', 'MotorY','NHits'])

#print(df)
#print(df.groupby(['MotorX', 'MotorY'], as_index=False)['NHits'].mean())

df = df.groupby(['MotorX', 'MotorY'], as_index=False)['NHits'].mean()

pivot = df.pivot(index='MotorX', columns='MotorY', values='NHits')
sns.heatmap(pivot,cmap='coolwarm',annot=True, cbar_kws={'label': 'NHits in Selected Candidate'},fmt=".2f")
#sns.heatmap(df, cmap='coolwarm', square=True,annot=True)
#h1 = axs3.hexbin(df.MotorX, df.MotorY, C=df.NHits, gridsize=50,cmap='coolwarm')

axs3.set_xlabel("Y motor [mm]")
axs3.set_ylabel("X motor [mm]")

save_file = "output/Align_H_2.png"
plt.savefig(save_file)
plt.show()