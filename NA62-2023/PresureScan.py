import uproot
import numpy as np
import matplotlib.pyplot as plt
import mplhep as hep
plt.style.use(hep.style.ROOT)
import pandas as pd
from csv import writer
from scipy.stats import norm
import argparse
import os
 
time = []
hitpevnt = []

_sec_8 = []
_sec_7 = []
_sec_6 = []
_sec_5 = []

_sec_8_comp = []
_sec_7_comp = []
_sec_6_comp = []
_sec_5_comp = []

_sec_5_comp_PiK = []

r76 = []
r87 = []
r86 = []
r85 = []

p_sec_8 = []
p_sec_7 = []
p_sec_6 = []
p_sec_5 = []

h_sec_0 = []
h_sec_1 = []
h_sec_2 = []
h_sec_3 = []
h_sec_4 = []
h_sec_5 = []
h_sec_6 = []
h_sec_7 = []

_mu = []
_presure = []
_presure_comp = []

_temp_Dia = []
_temp_Front = []
_temp_Back = []
_temp_Dia = []

#190, 600
ref_time = ["H_PRES","SmallerDia"] 
ref_P = [2.2,1.61]

file_name = "Testing"

'''
coefficients = [0,0] #np.polyfit(ref_time, ref_P, 1)

print('a =', coefficients[0])
print('b =', coefficients[1])

def func_presure(x):
    a = coefficients[0]
    b = coefficients[1]
    
    if x < ref_time[0]:
        return ref_P[0]
    
    if x > ref_time[1]:
        return ref_P[1]
    
    return a*x + b

print(func_presure(1682729338))

#exit(0)
'''
 
#directory = '/eos/user/j/jsanders/cedar_roots/PRESS_3may_2/'

#directory = '/afs/cern.ch/work/c/cparkins/public/PRESS_5/'

#directory = '/eos/user/j/jsanders/condorout/4913989/reco/'

directory = '/eos/user/j/jsanders/cedar_roots/2Pressure_H/'

#directory = '/eos/user/c/cparkins/public/PSCAN_012975/'

#directory = '/afs/cern.ch/work/j/jsanders/Software/CedarAlignment/rootfiles/newDia/2ndpres/'

c = 0

for filename in os.scandir(directory):
    if filename.is_file():
        
        if "tar" in filename.path:
            continue
        
        if ".root" not in filename.path:
            continue
        file_name = filename.path
        
        
        
        #file_name = "/eos/user/j/jsanders/condorout/4913989/reco/Saturn.4913989.530.root"
        #time.append(file_name[-35:-25])
        
        #print(file_name)
        
        #inFile = uproot.open(file_name)
        #inFile = uproot.open(file_name)
        
        try: 
            inFile = uproot.open(file_name)
        except ValueError:
            continue
        except OSError:
            continue
        
        h_NRecoHits = inFile["CedarMonitor/NRecoHits"]
        
        #ChannelId = inFile['SlimReco']['Cedar/fHits/fHits.fChannelID']
        NEvnts = inFile['SpecialTrigger;1']['EventHeader/fEventNumber']
        #NEvnts = inFile['SpecialTrigger;1']['EventHeader/fEventLength']
        
        h_NSectorsInCandidate = inFile["CedarMonitor/NSectorsInCandidate"]
        
        h_NRecoHitsInSector = inFile["CedarMonitor/NRecoHitsInSector"].values()
        
        presure = inFile['SpecialTrigger;1']['Cedar/fDIMInfo/fDIMInfo.fPressure'].array()
        
        #print(presure)
        
        h_NSectorsInSelectedCandidate = inFile["CedarMonitor/NSectorsInSelectedCandidate"]
        
        h_NRecoHitsInSelectedCandidate = inFile["CedarMonitor/NRecoHitsInSelectedCandidate"]
        
        #NSectors = inFile["CedarMonitor/NSectors"]
        
        #print(h_NSectorsInCandidate.axis().edges())
        nsecCand = h_NSectorsInCandidate.values()
        
        
        Arg = inFile['SpecialTrigger;1']['Beam/fARGONION']
        
        #burst = file_name[-14:-10]
        
        burst = inFile['SpecialTrigger;1']['EventHeader/fBurstID'].array()[0]
        
        #
        #if int(burst) > 788:
        #    continue
        
        time_stamp = file_name[-35:-25]
        
        pres = 0
        
        pres = file_name[-9:-5]
        
        #burst = [0,0]
        print(presure)
        
        #if presure is list:
        #    pres = presure[0]
        #else:
        #    pres = presure
        
        try:
            #if presure is list:
            #    pres = presure[0]
            #else: 
            #    pres = presure[0]
            pres = max(presure)
        except ValueError:
            continue
        print(burst)
        #pres = func_presure(int(time_stamp))
        
        print("-----------------------")
        print(pres)
        print(time_stamp)
        print(burst)
        
        #if round(pres*100)/100 == 1.88:
        #    break
       
        #print(Arg["fARGONION.fCounts"].array()[1])
        Arg_count = 1
        try:
            #if presure is list:
            #    pres = presure[0]
            #else: 
                #pres = presure[0]
            #Arg_count = Arg["fARGONION.fCounts"].array()[1]
            Arg_count = max(Arg["fARGONION.fCounts"].array())
        except ValueError:
            continue
        
        print(Arg_count)
        #if (len(Arg["fARGONION.fCounts"].array()) > 1):
        #    Arg_count = Arg["fARGONION.fCounts"].array()[1]
        #print(Arg_count)
        
        #try:
        #    evnts = NEvnts.array()[1]
        #except ValueError:
        #    continue
        
        THits = h_NRecoHits.member('fTsumwx')
        #print(evnts)
        #print(THits)
        #print(THits/evnts)
        #print(len(Hits.array()))
        #print(THits/len(ChannelId.array()))
        #if THits/len(Hits.array()) < 20:
        #    continue
        
        #if (nsecCand[-3]+nsecCand[-2]+nsecCand[-1]) < 1000:
        #    continue
        
        #if 2.02 < round(pres*1000)/1000 < 2.04:
        #    pass
        #else:
        #    continue
        
        temp_D = max(inFile['SpecialTrigger;1']['Cedar/fDIMInfo/fDIMInfo.fTempDiaph'].array())
        temp_B = max(inFile['SpecialTrigger;1']['Cedar/fDIMInfo/fDIMInfo.fTempRear'].array())
        temp_F = max(inFile['SpecialTrigger;1']['Cedar/fDIMInfo/fDIMInfo.fTempFront'].array())
        
        print(temp_D)
        
        _temp_Back.append(temp_B)
        _temp_Dia.append(temp_D)
        _temp_Front.append(temp_F)
        
        _presure.append(float(pres))
        time.append(burst)
        hitpevnt.append(0)#(THits/len(ChannelId.array()))/(Arg_count/1338310000))
        
        _sec_8.append((nsecCand[-1])/Arg_count)
        _sec_7.append((nsecCand[-2]+nsecCand[-1])/Arg_count)
        _sec_6.append((nsecCand[-3]+nsecCand[-2]+nsecCand[-1])/Arg_count)
        _sec_5.append((nsecCand[-4]+nsecCand[-3]+nsecCand[-2]+nsecCand[-1])/Arg_count)
        
        r76.append((nsecCand[-2]+nsecCand[-1])/(nsecCand[-3]+nsecCand[-2]+nsecCand[-1]))
        r87.append((nsecCand[-1])/(nsecCand[-2]+nsecCand[-1]))
        r86.append((nsecCand[-1])/(nsecCand[-3]+nsecCand[-2]+nsecCand[-1]))
        r85.append((nsecCand[-1])/(nsecCand[-4]+nsecCand[-3]+nsecCand[-2]+nsecCand[-1]))
        
        if 3.850 < round(pres*1000)/1000 < 3.890:
            print("R85 = {}".format(r85[-1]))
            print("R87 = {}".format(r87[-1]))
            print("R76 = {}".format(r76[-1]))

        
        p_sec_8.append(((nsecCand[-1])/sum(nsecCand)))
        p_sec_7.append((nsecCand[-2]+nsecCand[-1])/sum(nsecCand))
        p_sec_6.append((nsecCand[-3]+nsecCand[-2]+nsecCand[-1])/sum(nsecCand))
        p_sec_5.append((nsecCand[-4]+nsecCand[-3]+nsecCand[-2]+nsecCand[-1])/sum(nsecCand))
        
        print(h_NRecoHits.member('fEntries'))
        
        '''
        if float(pres) > 4.10:
            #if float(pres) < 4.32:
            pres -= 4.32
            pres *= -1
            pres += 4.32

                
            pres -= (4.32-3.73)
            pres -= (3.83-3.79)
            pres += 0.01
            
            _sec_8_comp.append(((nsecCand[-1])/Arg_count)*(70/23))
            _sec_7_comp.append(((nsecCand[-2]+nsecCand[-1])/Arg_count)*(70/23))
            _sec_6_comp.append(((nsecCand[-3]+nsecCand[-2]+nsecCand[-1])/Arg_count)*(70/23))
            _sec_5_comp.append(((nsecCand[-4]+nsecCand[-3]+nsecCand[-2]+nsecCand[-1])/Arg_count)*(70/23))
            
        elif float(pres) < 3.8:
            _sec_8_comp.append(0)
            _sec_7_comp.append(0)
            _sec_6_comp.append(0)
            _sec_5_comp.append(0)
        else:
            _sec_8_comp.append((nsecCand[-1])/Arg_count)
            _sec_7_comp.append((nsecCand[-2]+nsecCand[-1])/Arg_count)
            _sec_6_comp.append((nsecCand[-3]+nsecCand[-2]+nsecCand[-1])/Arg_count)
            _sec_5_comp.append((nsecCand[-4]+nsecCand[-3]+nsecCand[-2]+nsecCand[-1])/Arg_count)
        '''    
        if float(pres) < 3.8:  
            pres -= 3.72
            pres *= -1
            pres += 3.72
            
            pres += 0.01
            

        _sec_8_comp.append((nsecCand[-1])/Arg_count)
        _sec_7_comp.append((nsecCand[-2]+nsecCand[-1])/Arg_count)
        _sec_6_comp.append((nsecCand[-3]+nsecCand[-2]+nsecCand[-1])/Arg_count)
        _sec_5_comp.append((nsecCand[-4]+nsecCand[-3]+nsecCand[-2]+nsecCand[-1])/Arg_count)
            
        #_sec_5_comp_piK.append(_sec_5_comp[-1])
            
        _presure_comp.append(pres)
        
        '''
        h_sec_0.append(h_NRecoHitsInSector[0])
        h_sec_1.append(h_NRecoHitsInSector[1])
        h_sec_2.append(h_NRecoHitsInSector[2])
        h_sec_3.append(h_NRecoHitsInSector[3])
        h_sec_4.append(h_NRecoHitsInSector[4])
        h_sec_5.append(h_NRecoHitsInSector[5])
        h_sec_6.append(h_NRecoHitsInSector[6])
        h_sec_7.append(h_NRecoHitsInSector[7])
        
        
        fig, axs = plt.subplots(1, 1,figsize=(10,10))
        ax1 = axs
        
        bins_sel = h_NRecoHitsInSelectedCandidate.axis().edges()
        weight_sel = h_NRecoHitsInSelectedCandidate.counts()
        
        counts, bins, bars = ax1.hist(bins_sel[1:],bins_sel, weights=weight_sel)#, label="NHits (Sel): mu = {}".format(mu))

        value = []
        for i in range(len(bins[1:])):
            for t in range(int(counts[i])):
                value.append(bins[i])

        mu, std = norm.fit(value)
        _mu.append(mu)
        print("NHits (Sel): mu = {}".format(mu))
        
        plt.clf()
        plt.close()
        
        
        
        '''
        h_sec_0.append(h_NRecoHitsInSector[0])
        h_sec_1.append(h_NRecoHitsInSector[1])
        h_sec_2.append(h_NRecoHitsInSector[2])
        h_sec_3.append(h_NRecoHitsInSector[3])
        h_sec_4.append(h_NRecoHitsInSector[4])
        h_sec_5.append(h_NRecoHitsInSector[5])
        h_sec_6.append(h_NRecoHitsInSector[6])
        h_sec_7.append(h_NRecoHitsInSector[7])
            
            
        try:
            mu1 = h_NRecoHitsInSelectedCandidate.member("fTsumwx")/h_NRecoHitsInSelectedCandidate.member("fEntries")
        except ZeroDivisionError:
            mu1 = 0
            
        if 3.850 < round(pres*1000)/1000 < 3.890:
            print(file_name)
            print(mu1)
            
        _mu.append(mu1)
        #if 2.025 < round(pres*1000)/1000 < 2.035 :
        #    print("6FolD",(nsecCand[-3]+nsecCand[-2]+nsecCand[-1])/Arg_count)
        #print(_sec_6[-1])
        #    break
        '''
        try:
            mu1 = h_NRecoHitsInSelectedCandidate.member("fTsumwx")/h_NRecoHitsInSelectedCandidate.member("fEntries")
        except ZeroDivisionError:
            mu1 = 0
        _mu.append(mu1)
        
        #exit(0)
        print("NHits (Sel): mu = {}".format(mu1))
        
        
        
        counts, bins, bars = axs0.hist(bins_sel[1:],bins_sel, weights=weight_sel, label="SelectedCandidate")

        value = []
        for i in range(len(bins[1:])):
            for t in range(int(counts[i])):
                value.append(bins[i])

        mu, std = norm.fit(value)
        x = np.linspace(10, 60, 100)
        p = norm.pdf(x, mu, std)
        
        _mu.append(mu)
        print("NHits (Sel): mu = {}".format(mu))
        
        plt.clf()
        plt.close()
        
        '''
        
        c += 1
        
        #if c>55:
        #    break
        
        '''
        
        event_channel = []
        sec_8 = 0
        sec_7 = 0
        sec_6 = 0
        
        for i in range(len(ChannelId.array())):
            ChannelId.array()[i]
            #print(ChannelId.array()[i])
            num_sec = len(list(set(np.floor(ChannelId.array()[i]/100))))
            
            if num_sec == 8:
                sec_8 += 1
            elif num_sec > 7:
                sec_7 += 1
            elif num_sec > 6:
                sec_6 += 1
            
            #print(sum(event_hits))
        
        _sec_8.append(sec_8)
        _sec_7.append(sec_7)
        _sec_6.append(sec_6)
         '''


fig, axs = plt.subplots(figsize=(10,10))

axs.scatter(time,hitpevnt,marker="x")
axs.set_ylabel("Averge NHits per event")
axs.set_xlabel("Burst")
axs.xaxis.set_major_locator(plt.MaxNLocator(20))
axs.tick_params(axis='x', labelrotation = 90)

save_file = "output/PressureScans/{}-{}.Hits_Arg.png".format(ref_time[0],ref_time[1])
plt.savefig(save_file)


ratio_8 = []
ratio_7 = []
ratio_6 = []
ratio_5 = []
ratio_pres = []


for i in range(len(_presure_comp)):
    for t in range(len(_presure_comp)):  
        if round(_presure_comp[i]*1000)/1000 == round(_presure_comp[t]*1000)/1000 and (i != t):
            print("-------PION CONTAMINATION--------")
            print(_presure_comp[i],_presure_comp[t])
            print("5FOLD {}".format(_sec_5_comp[i]))
            print("6FOLD {}".format(_sec_6_comp[i]))
            print("7FOLD {}".format(_sec_7_comp[i]))
            print("8FOLD {}".format(_sec_8_comp[i]))
            print("=================================")
            print("5FOLD {}".format(_sec_5_comp[t]))
            print("6FOLD {}".format(_sec_6_comp[t]))
            print("7FOLD {}".format(_sec_7_comp[t]))
            print("8FOLD {}".format(_sec_8_comp[t]))
            print("-------PION DONE--------")
            if _sec_6_comp[i] == 0 or _sec_6_comp[t] == 0:
                continue
            if _sec_8_comp[t] > 1e-5:
                continue
            if 3.8 < round(_presure_comp[i]*1000)/1000 < 3.9:
                pass
            else:
                continue
            if _sec_8_comp[i] > _sec_8_comp[t] :
                ratio_8.append(_sec_8_comp[t]/_sec_8_comp[i])
                ratio_7.append(_sec_7_comp[t]/_sec_7_comp[i])
                ratio_6.append(_sec_6_comp[t]/_sec_6_comp[i])
                ratio_5.append(_sec_5_comp[t]/_sec_5_comp[i])
            else: 
                ratio_8.append(_sec_8_comp[i]/_sec_8_comp[t])
                ratio_7.append(_sec_7_comp[i]/_sec_7_comp[t])
                ratio_6.append(_sec_6_comp[i]/_sec_6_comp[t])
                ratio_5.append(_sec_5_comp[i]/_sec_5_comp[t])
            
            if 3.84 < round(_presure_comp[i]*1000)/1000 < 3.92:
                print("-------PION CONTAMINATION--------")
                print(_presure_comp[i],_presure_comp[t])
                print("5FOLD {}".format(_sec_5_comp[i]))
                print("6FOLD {}".format(_sec_6_comp[i]))
                print("7FOLD {}".format(_sec_7_comp[i]))
                print("8FOLD {}".format(_sec_8_comp[i]))
                print("=================================")
                print("5FOLD {}".format(_sec_5_comp[t]))
                print("6FOLD {}".format(_sec_6_comp[t]))
                print("7FOLD {}".format(_sec_7_comp[t]))
                print("8FOLD {}".format(_sec_8_comp[t]))
                print("-------PION DONE--------")
            
            ratio_pres.append(round(_presure_comp[i]*1000)/1000)
        
        

fig0, axs0 = plt.subplots(figsize=(10,10))

axs0.scatter(ratio_pres,ratio_8,marker="x",label="At Least 8 Sectors")
axs0.scatter(ratio_pres,ratio_7,marker="x",label="At Least 7 Sectors")
axs0.scatter(ratio_pres,ratio_6,marker="x",label="At Least 6 Sectors")
axs0.scatter(ratio_pres,ratio_5,marker="x",label="At Least 5 Sectors")
#axs0.set_ylabel("NFold Coincidences per Event Normalised to Argonian")
axs0.set_xlabel("Pressure")
#axs0.set_xlim(1.5,2.2)
axs0.set_yscale('log')
axs0.set_ylim(1e-5,1)
axs0.xaxis.set_major_locator(plt.MaxNLocator(20))
axs0.tick_params(axis='x', labelrotation = 90)
axs0.legend()
save_file = "output/PressureScans/{}-{}.Coin_log_ratio.png".format(ref_time[0],ref_time[1])
plt.savefig(save_file)

fig01, axs01 = plt.subplots(figsize=(10,10))

axs01.scatter(_presure_comp,_sec_8_comp,marker="x",label="At Least 8 Sectors")
axs01.scatter(_presure_comp,_sec_7_comp,marker="x",label="At Least 7 Sectors")
axs01.scatter(_presure_comp,_sec_6_comp,marker="x",label="At Least 6 Sectors")
axs01.scatter(_presure_comp,_sec_5_comp,marker="x",label="At Least 5 Sectors")
axs01.set_ylabel("NFold Coincidences per Event Normalised to Argonian")
axs01.set_xlabel("Pressure")
#axs01.set_xlim(1.5,2.2)
axs01.set_xlim(3.65,4.4)
axs01.set_yscale('log')
axs01.set_ylim(1e-7,1)
axs01.xaxis.set_major_locator(plt.MaxNLocator(20))
axs01.tick_params(axis='x', labelrotation = 90)
axs01.legend()
save_file = "output/PressureScans/{}-{}.Coin_log_compare.png".format(ref_time[0],ref_time[1])
plt.savefig(save_file)

fig1, axs1 = plt.subplots(figsize=(10,10))

axs1.scatter(_presure,_sec_8,marker="x",label="At Least 8 Sectors")
axs1.scatter(_presure,_sec_7,marker="x",label="At Least 7 Sectors")
axs1.scatter(_presure,_sec_6,marker="x",label="At Least 6 Sectors")
axs1.scatter(_presure,_sec_5,marker="x",label="At Least 5 Sectors")
axs1.set_ylabel("NFold Coincidences per Event Normalised to Argonian")
axs1.set_xlabel("Pressure")
axs1.set_xlim(3.65,4.4)
axs1.set_yscale('log')
#axs1.set_ylim(1e-7,1)
axs1.set_ylim(1e-7,1)
axs1.xaxis.set_major_locator(plt.MaxNLocator(20))
axs1.tick_params(axis='x', labelrotation = 90)
axs1.legend()
save_file = "output/PressureScans/{}-{}.Coin_log.png".format(ref_time[0],ref_time[1])
plt.savefig(save_file)

fig01, axs01 = plt.subplots(figsize=(10,10))

axs01.scatter(_presure,_sec_8,marker="x",label="At Least 8 Sectors")
axs01.scatter(_presure,_sec_7,marker="x",label="At Least 7 Sectors")
axs01.scatter(_presure,_sec_6,marker="x",label="At Least 6 Sectors")
axs01.scatter(_presure,_sec_5,marker="x",label="At Least 5 Sectors")
axs01.set_ylabel("NFold Coincidences per Event Normalised to Argonian")
axs01.set_xlabel("Pressure")
axs1.set_xlim(3.65,4.4)
#axs01.yscale("log")
#axs1.set_ylim(0,0.0025)
axs01.xaxis.set_major_locator(plt.MaxNLocator(20))
axs01.tick_params(axis='x', labelrotation = 90)
axs01.legend()
save_file = "output/PressureScans/{}-{}.Coin.png".format(ref_time[0],ref_time[1])
plt.savefig(save_file)

fig2, axs2 = plt.subplots(figsize=(10,10))


axs2.scatter(_presure,p_sec_8,marker="x",label="At Least 8 Sectors")
axs2.scatter(_presure,p_sec_7,marker="x",label="At Least 7 Sectors")
axs2.scatter(_presure,p_sec_6,marker="x",label="At Least 6 Sectors")
axs2.set_ylabel("Probabilty of NFold Conicidences per Burst")
axs2.set_xlabel("Pressure")
#axs2.set_xlim(1.5,2.2)
#axs2.set_ylim(0,0.3)
axs2.legend()
axs2.xaxis.set_major_locator(plt.MaxNLocator(20))
axs2.tick_params(axis='x', labelrotation = 90)

save_file = "output/PressureScans/{}-{}.CoinpEvnt.png".format(ref_time[0],ref_time[1])
plt.savefig(save_file)

fig3, axs3 = plt.subplots(figsize=(10,10))


axs3.scatter(_presure,h_sec_0,marker="x",label="S_0")
axs3.scatter(_presure,h_sec_1,marker="x",label="S_1")
axs3.scatter(_presure,h_sec_2,marker="x",label="S_2")
axs3.scatter(_presure,h_sec_3,marker="x",label="S_3")
axs3.scatter(_presure,h_sec_4,marker="x",label="S_4")
axs3.scatter(_presure,h_sec_5,marker="x",label="S_5")
axs3.scatter(_presure,h_sec_6,marker="x",label="S_6")
axs3.scatter(_presure,h_sec_7,marker="x",label="S_7")


axs3.set_ylabel("Hits in Sector per Burst")
axs3.set_xlabel("Burst")
#axs3.set_xlim(1.5,2.25)
axs3.xaxis.set_major_locator(plt.MaxNLocator(20))
axs3.tick_params(axis='x', labelrotation = 90)
axs3.legend()
save_file = "output/PressureScans/{}-{}.SecHits.png".format(ref_time[0],ref_time[1])
plt.savefig(save_file)

fig4, axs4 = plt.subplots(figsize=(10,10))

axs4.scatter(_presure,_mu,marker="x")
axs4.set_ylabel("Number of Hits in Selected Candidate")
axs4.set_xlabel("Presure")
axs4.xaxis.set_major_locator(plt.MaxNLocator(20))
axs4.tick_params(axis='x', labelrotation = 90)

save_file = "output/PressureScans/{}-{}.NHits_Sel.png".format(ref_time[0],ref_time[1])
plt.savefig(save_file)


fig5, axs5 = plt.subplots(figsize=(10,10))

axs5.scatter(_presure,r76,marker="x",label="R76")
axs5.scatter(_presure,r87,marker="x",label="R87")
axs5.set_ylabel("Ratios")
axs5.set_xlabel("Pressure")
#axs5.set_xlim(1.5,2.2)
axs5.set_yscale('log')
#axs5.set_ylim(1e-4,1)
axs5.xaxis.set_major_locator(plt.MaxNLocator(20))
axs5.tick_params(axis='x', labelrotation = 90)
axs5.legend()
save_file = "output/PressureScans/{}-{}.Ratio_log.png".format(ref_time[0],ref_time[1])
plt.savefig(save_file)

fig6, axs6 = plt.subplots(figsize=(10,10))

axs6.scatter(_presure,r76,marker="x",label="R76")
axs6.scatter(_presure,r87,marker="x",label="R87")
axs6.scatter(_presure,r86,marker="x",label="R86")
axs6.scatter(_presure,r85,marker="x",label="R85")
axs6.set_ylabel("Ratios")
axs6.set_xlabel("Pressure")
#axs6.set_xlim(1.5,2.2)
axs6.set_ylim(0,1)
axs6.xaxis.set_major_locator(plt.MaxNLocator(20))
axs6.tick_params(axis='x', labelrotation = 90)
axs6.legend()
save_file = "output/PressureScans/{}-{}.Ratio_log.png".format(ref_time[0],ref_time[1])
plt.savefig(save_file)

fig7, axs7 = plt.subplots(figsize=(10,10))

axs7.scatter(_presure,_temp_Back,marker="x",label="Rear")
axs7.scatter(_presure,_temp_Front,marker="x",label="Front")
axs7.scatter(_presure,_temp_Dia,marker="x",label="Diaphragm")
axs7.set_ylabel("Temperature")
axs7.set_xlabel("Pressure")
#axs6.set_xlim(1.5,2.2)
#axs7.set_ylim(0,1)
axs7.xaxis.set_major_locator(plt.MaxNLocator(20))
axs7.tick_params(axis='x', labelrotation = 90)
axs7.legend()
save_file = "output/PressureScans/{}-{}.Temp.png".format(ref_time[0],ref_time[1])
plt.savefig(save_file)


plt.show()