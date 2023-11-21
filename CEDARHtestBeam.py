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
import numpy as np
from scipy.optimize import curve_fit

def n7n8Photons(n7,n8):
    return np.log(1+((8)/((n7/n8)-1)))

def n6n8Photons(n6,n8):
    return np.log(1+((14)/(np.sqrt(4-7*(1-n6/n8))-2)))

def Fold8eff(phi):
    return (1-np.exp(-phi))**8

def Fold7eff(phi,n8):
    return n8 + 8*(1-np.exp(-phi))**7*np.exp(-phi)

def Fold6eff(phi,n7):
    return n7 + 28*(1-np.exp(-phi))**6*np.exp(-2*phi)
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
                head = [row[0],"PMT0","PMT1","PMT2","PMT3","PMT4","PMT5","PMT6","PMT7","6Fold","7Fold","8Fold","Trigger","TotalHits","Pressure"]
                PMTRows.append(head)  
            elif row == ['VARIABLE: XBH6.XCED.041.440:PRESSURE']:
                
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
    outfile = str("formated_data/Timber_data."+t1t2+".csv")
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
#outfile = "formated_data\Timber_data.2022-11-04-23-05-45-735_2022-11-05-03-05-31-335.csv" 
outfile = "formated_data\Timber_data.2022-11-05-10-30-04-935_2022-11-05-16-00-31-335.csv"
#outfile = "formated_data\Timber_data.2022-11-05-18-45-08-535_2022-11-06-00-00-30-135.csv" #"formated_data\Timber_data.2022-11-06-15-30-07-335_2022-11-07-06-29-37-335.csv"
#outfile = "formated_data\Timber_data.2022-11-06-15-30-07-335_2022-11-07-06-29-37-335.csv"
df = pd.read_csv(outfile)
df['Timestamp (UTC_TIME)'] = pd.to_datetime(df['Timestamp (UTC_TIME)'])

plt.rcParams['figure.constrained_layout.use'] = True

data_mean = df.groupby('Pressure', as_index=False)['6Fold'].mean()
data_error = df.groupby('Pressure', as_index=False)['6Fold'].sem()
data_mean['6Fold_Error'] = data_error['6Fold'].fillna(0)

data_mean['7Fold'] = df.groupby('Pressure', as_index=False)['7Fold'].mean()['7Fold']
data_error = df.groupby('Pressure', as_index=False)['7Fold'].sem()
data_mean['7Fold_Error'] = data_error['7Fold'].fillna(0)

data_mean['8Fold'] = df.groupby('Pressure', as_index=False)['8Fold'].mean()['8Fold']
data_error = df.groupby('Pressure', as_index=False)['8Fold'].sem()
data_mean['8Fold_Error'] = data_error['8Fold'].fillna(0)

pdfname = str(df['Timestamp (UTC_TIME)'].iloc[0].strftime('%m-%d_%H-%M')) + "--" + str(df['Timestamp (UTC_TIME)'].iloc[-1].strftime('%m-%d_%H-%M'))
try:
    makedirs('pdf/{}'.format(pdfname))
except FileExistsError:
    pass
    



ax1 = df.plot.scatter(x='Timestamp (UTC_TIME)',y='Pressure', c='DarkBlue')
plt.savefig("pdf/{}/Pressure.pdf".format(pdfname), format="pdf", bbox_inches="tight")

ax2 = df.plot.scatter(x='Pressure',y='6Fold', c='DarkBlue',label="6-fold")
ax2_1 = df.plot.scatter(x='Pressure',y='7Fold', c='red' , label="7-fold", ax=ax2)
ax2_2 = df.plot.scatter(x='Pressure',y='8Fold', c='green', label="8-fold", ax=ax2)
ax2.set_ylabel("Coincidences")
ax2.set_xlabel("Pressure [bar]")
ax2.legend()
ax2.set_xlim(3.6,4.4)
ax2.set_title("All pressure points")
plt.savefig("pdf/{}/CoincidencesAllPoints.pdf".format(pdfname), format="pdf", bbox_inches="tight")

ax3 = data_mean.plot.scatter(x='Pressure',y='6Fold', yerr = '6Fold_Error', c='DarkBlue',label="6-fold")
ax3_1 = data_mean.plot.scatter(x='Pressure',y='7Fold', yerr = '7Fold_Error',c='red' , label="7-fold", ax=ax3)
ax3_2 = data_mean.plot.scatter(x='Pressure',y='8Fold', yerr = '8Fold_Error', c='green', label="8-fold", ax=ax3)
ax3.set_ylabel("Coincidences")
ax3.set_xlabel("Pressure [bar]")
ax3.legend()
ax3.set_yscale('log')
ax3.set_xlim(3.6,4.4)
ax3.set_title("Average pressure points")
ax3.tick_params(axis='both', which='major', pad=10)
plt.savefig("pdf/{}/CoincidencesAvgPoints.pdf".format(pdfname), format="pdf", bbox_inches="tight")



df['6FoldpTrigger'] = df['6Fold']/df['Trigger']
df['7FoldpTrigger'] = df['7Fold']/df['Trigger']
df['8FoldpTrigger'] = df['8Fold']/df['Trigger']

dfpTrigger_mean = df.groupby('Pressure', as_index=False)['6FoldpTrigger'].mean()
dfpTrigger_error = df.groupby('Pressure', as_index=False)['6FoldpTrigger'].sem()
dfpTrigger_mean['6FoldpTrigger_Error'] = dfpTrigger_error['6FoldpTrigger'].fillna(0)

dfpTrigger_mean['7FoldpTrigger'] = df.groupby('Pressure', as_index=False)['7FoldpTrigger'].mean()['7FoldpTrigger']
dfpTrigger_error    = df.groupby('Pressure', as_index=False)['7FoldpTrigger'].sem()
dfpTrigger_mean['7FoldpTrigger_Error'] = dfpTrigger_error['7FoldpTrigger'].fillna(0)

dfpTrigger_mean['8FoldpTrigger'] = df.groupby('Pressure', as_index=False)['8FoldpTrigger'].mean()['8FoldpTrigger']
dfpTrigger_error = df.groupby('Pressure', as_index=False)['8FoldpTrigger'].sem()
dfpTrigger_mean['8FoldpTrigger_Error'] = dfpTrigger_error['8FoldpTrigger'].fillna(0)

dfpTrigger_mean = dfpTrigger_mean[dfpTrigger_mean["6FoldpTrigger_Error"] < 0.001]

size_marker = 40

ax4 = dfpTrigger_mean.plot.scatter(x='Pressure',y='6FoldpTrigger', yerr = '6FoldpTrigger_Error', xerr=0.001, c='DarkBlue',label="6-fold",marker="s",s=size_marker)
ax4_1 = dfpTrigger_mean.plot.scatter(x='Pressure',y='7FoldpTrigger', yerr = '7FoldpTrigger_Error',xerr=0.001,c='red' , label="7-fold", ax=ax4, marker="^",s=size_marker)
ax4_2 = dfpTrigger_mean.plot.scatter(x='Pressure',y='8FoldpTrigger', yerr = '8FoldpTrigger_Error', xerr=0.001,c='green', label="8-fold", ax=ax4, marker="o",s=size_marker)
ax4.set_ylabel("Coincidences per trigger", fontsize=30)
ax4.set_xlabel("Pressure [bar]", fontsize=30)
ax4.legend(prop={'size': 30})
#ax4.set_title("At Least N Coincidences per Trigger vs Pressure")
ax4.set_ylim(0,0.8)
ax4.set_xlim(3.6,4.4)
for axis in ['top', 'bottom', 'left', 'right']:
        ax4.spines[axis].set_linewidth(2.5)

ax4.tick_params(axis='both', which='major', pad=10, labelsize=30)

ax4.tick_params(axis="both", which="major", length=20, width=2) 
ax4.tick_params(axis="both", which="minor", length=10, width=2)
plt.savefig("pdf/{}/CoincidencesAvgPointspTrigger.pdf".format(pdfname), format="pdf", bbox_inches="tight")

ax5 = dfpTrigger_mean.plot.scatter(x='Pressure',y='6FoldpTrigger', yerr = '6FoldpTrigger_Error', xerr=0.001, c='DarkBlue',label="6-fold",marker="s",s=size_marker)
ax5_1 = dfpTrigger_mean.plot.scatter(x='Pressure',y='7FoldpTrigger', yerr = '7FoldpTrigger_Error',xerr=0.001,c='red' , label="7-fold", ax=ax5,marker="^",s=size_marker)
ax5_2 = dfpTrigger_mean.plot.scatter(x='Pressure',y='8FoldpTrigger', yerr = '8FoldpTrigger_Error', xerr=0.001,c='green', label="8-fold", ax=ax5,marker="o",s=size_marker)
ax5.set_ylabel("Coincidences per trigger", fontsize=30)
ax5.set_xlabel("Pressure [bar]", fontsize=30)
ax5.set_ylim(10e-7,10)
#ax5.set_title("At Least N Coincidences per Trigger vs Pressure")
ax5.set_yscale('log')
#plt.savefig("pdf/{}/LogCoincidencesAvgPointspTrigger.pdf".format(pdfname), format="pdf", bbox_inches="tight")

fold6 = dfpTrigger_mean['6FoldpTrigger'].values.tolist()
fold7 = dfpTrigger_mean['7FoldpTrigger'].values.tolist()
fold8 = dfpTrigger_mean['8FoldpTrigger'].values.tolist()
pres = dfpTrigger_mean['Pressure'].values.tolist()

#mean,std=norm.fit(data)
fold6_R1 = []
fold6_R2 = []
fold6_R3 = []
pres_R1 = []
pres_R1_p = []
pres_R2 = []
pres_R2_p = []
pres_R3 = []
pres_R3_p = []

for i in range(len(pres)):
    if 3.60 < pres[i] < 3.80:
        pres_R1_p.append(pres[i])
        
    if 3.64 < pres[i] < 3.78:
        pres_R1.append(pres[i])
        fold6_R1.append(fold6[i])
        
    if 3.75 < pres[i] < 3.95:
        pres_R2_p.append(pres[i])
        
    if 3.78 < pres[i] < 3.92:
        pres_R2.append(pres[i])
        fold6_R2.append(fold6[i])
        
    if 4.15 < pres[i] < 4.40:
        pres_R3_p.append(pres[i])
        
    if 4.17 < pres[i] < 4.36:
        pres_R3.append(pres[i])
        fold6_R3.append(fold6[i])

def sup_gauss(x, a, x0, sigma,p):
    return a * np.exp(-((x - x0) ** 2 / (2 * sigma ** 2))**p)

popt6_1,pcov6_1 = curve_fit(sup_gauss,pres_R1,fold6_R1)
ax5.plot(pres_R1_p,sup_gauss(pres_R1_p,*popt6_1),'b--')

popt6_2,pcov6_2 = curve_fit(sup_gauss,pres_R2,fold6_R2)
ax5.plot(pres_R2_p,sup_gauss(pres_R2_p,*popt6_2),'b--')

popt6_3,pcov6_3 = curve_fit(sup_gauss,pres_R3,fold6_R3)
ax5.plot(pres_R3_p,sup_gauss(pres_R3_p,*popt6_3),'b--')

ax5.legend(prop={'size': 30})
ax5.set_xlim(3.6,4.4)
for axis in ['top', 'bottom', 'left', 'right']:
        ax5.spines[axis].set_linewidth(2.5)

ax5.tick_params(axis='both', which='major', pad=10, labelsize=30)

ax5.tick_params(axis="both", which="major", length=20, width=2) 
ax5.tick_params(axis="both", which="minor", length=10, width=2)
print(sup_gauss(3.85,*popt6_1))
print(sup_gauss(3.85,*popt6_2))
print(sup_gauss(3.85,*popt6_1)/sup_gauss(3.85,*popt6_2))

plt.savefig("pdf/{}/LogCoincidencesAvgPointspTrigger.pdf".format(pdfname), format="pdf", bbox_inches="tight")

fold6 = dfpTrigger_mean['6FoldpTrigger'].values.tolist()
fold7 = dfpTrigger_mean['7FoldpTrigger'].values.tolist()
fold8 = dfpTrigger_mean['8FoldpTrigger'].values.tolist()
pres = dfpTrigger_mean['Pressure'].values.tolist()

counts1 = 0 
counts2 = 0
counts3 = 0

folds1 = 0 
folds2 = 0
folds3 = 0

for i in range(len(pres)):
    if 3.68 < pres[i] < 3.70:
        counts1 += 1
        print(pres[i],fold6[i])
        folds1 += fold6[i]
    elif 3.82 < pres[i] < 3.87:
        counts2 += 1
        folds2 += fold6[i]
        print(pres[i],fold6[i])
    elif 4.257 < pres[i] < 4.28:
        counts3 += 1
        folds3 += fold6[i]
        print(pres[i],fold6[i])

print("Pion frac= {}".format(folds1/counts1))
print("Kaon frac= {}".format(folds2/counts2))
print("Pronton frac= {}".format(folds3/counts3))

print("Total = {}".format(folds1/counts1 + folds2/counts2 + folds3/counts3))
for i in range(len(pres)):
    if float(pres[i]) < 3.7:  
            pres[i] -= 3.7
            pres[i] *= -1
            pres[i] += 3.7
            pres[i] -= 0.01
if False:
    for i in range(len(pres)):
        for t in range(len(pres)):  
            if round(pres[i]*1000)/1000 == round(pres[t]*1000)/1000 and (i != t):
                print("-------PION CONTAMINATION--------")
                print(pres[i],pres[t])
                print("6FOLD {}".format(fold6[i]))
                print("7FOLD {}".format(fold7[i]))
                print("8FOLD {}".format(fold8[i]))
                print("=================================")
                print("6FOLD {}".format(fold6[t]))
                print("7FOLD {}".format(fold7[t]))
                print("8FOLD {}".format(fold8[t]))
                print("-------PION DONE--------")
            

fig, axs = plt.subplots(figsize=(10,10))
axs.scatter(pres,fold6,c='DarkBlue',label="6Fold")
axs.scatter(pres,fold7,c='red',label="7Fold")
axs.scatter(pres,fold8,c='green',label="8Fold")
axs.set_yscale('log')
axs.legend()


df['R76'] = df['7Fold']/df['6Fold']
df['R87'] = df['8Fold']/df['7Fold']

dRatio_mean = df.groupby('Pressure', as_index=False)['R76'].mean()
dRatio_error = df.groupby('Pressure', as_index=False)['R76'].sem()
dRatio_mean['R76_Error'] = dRatio_error['R76'].fillna(0)

dRatio_mean['R87'] = df.groupby('Pressure', as_index=False)['R87'].mean()['R87']
dRatio_error = df.groupby('Pressure', as_index=False)['R87'].sem()
dRatio_mean['R87_Error'] = dRatio_error['R87'].fillna(0)

ax6 = dRatio_mean.plot.scatter(x='Pressure',y='R76', yerr = 'R76_Error', xerr=0.001, c='DarkBlue',label="R76")
ax6_1 = dRatio_mean.plot.scatter(x='Pressure',y='R87', yerr = 'R87_Error',xerr=0.001,c='red' , label="R87", ax=ax6)
ax6.set_ylabel("Ratio")
ax6.set_xlabel("Pressure [bar]")
ax6.legend()
plt.savefig("pdf/{}/RatioPlot.pdf".format(pdfname), format="pdf", bbox_inches="tight")

df.loc[df['Pressure'] <= 3.787 , '6Foldeff'] = (df['6Fold']/df['Trigger'])/0.71
df.loc[df['Pressure'] > 3.787, '6Foldeff'] = (df['6Fold']/df['Trigger'])/0.036
df.loc[df['Pressure'] > 4, '6Foldeff'] = (df['6Fold']/df['Trigger'])/0.254

df.loc[df['Pressure'] <= 3.787 , '7Foldeff'] = (df['7Fold']/df['Trigger'])/0.71
df.loc[df['Pressure'] > 3.787, '7Foldeff'] = (df['7Fold']/df['Trigger'])/0.036
df.loc[df['Pressure'] > 4, '7Foldeff'] = (df['7Fold']/df['Trigger'])/0.254

df.loc[df['Pressure'] <= 3.787 , '8Foldeff'] = (df['8Fold']/df['Trigger'])/0.71
df.loc[df['Pressure'] > 3.787, '8Foldeff'] = (df['8Fold']/df['Trigger'])/0.036
df.loc[df['Pressure'] > 4, '8Foldeff'] = (df['8Fold']/df['Trigger'])/0.254


print(df.loc[((df['Pressure'] < 3.86) & (df['Pressure'] > 3.84))][['Pressure','6Foldeff']])
print(df.loc[((df['Pressure'] < 3.86) & (df['Pressure'] > 3.84))][['Pressure','7Foldeff']])
print(df.loc[((df['Pressure'] < 3.86) & (df['Pressure'] > 3.84))][['Pressure','8Foldeff']])

eff_mean = df.groupby('Pressure', as_index=False)['6Foldeff'].mean()
eff_error = df.groupby('Pressure', as_index=False)['6Foldeff'].sem()
eff_mean['6Foldeff_Error'] = eff_error['6Foldeff'].fillna(0)

eff_mean['7Foldeff'] = df.groupby('Pressure', as_index=False)['7Foldeff'].mean()['7Foldeff']
eff_error = df.groupby('Pressure', as_index=False)['7Foldeff'].sem()
eff_mean['7Foldeff_Error'] = eff_error['7Foldeff'].fillna(0)

eff_mean['8Foldeff'] = df.groupby('Pressure', as_index=False)['8Foldeff'].mean()['8Foldeff']
eff_error = df.groupby('Pressure', as_index=False)['8Foldeff'].sem()
eff_mean['8Foldeff_Error'] = eff_error['8Foldeff'].fillna(0)

ax7 = eff_mean.plot.scatter(x='Pressure',y='6Foldeff', yerr = '6Foldeff_Error', xerr=0.001, c='DarkBlue',label="6Fold", marker="s")
ax7_1 = eff_mean.plot.scatter(x='Pressure',y='7Foldeff', yerr = '7Foldeff_Error',xerr=0.001,c='red' , label="7Fold", ax=ax7, marker="^")
ax7_2 = eff_mean.plot.scatter(x='Pressure',y='8Foldeff', yerr = '8Foldeff_Error', xerr=0.001,c='green', label="8Fold", ax=ax7, marker="o")
ax7.set_ylabel("Efficiency")
ax7.set_xlabel("Pressure [bar]")
ax7.legend()
ax7.grid()
ax7.set_title("Efficiency vs Pressure")
plt.savefig("pdf/{}/EfficiencyvsPressure.pdf".format(pdfname), format="pdf", bbox_inches="tight")


dfpTrigger_mean['Photons78'] = n7n8Photons(dfpTrigger_mean['7FoldpTrigger'],dfpTrigger_mean['8FoldpTrigger'])
dfpTrigger_mean['Photons68'] = n6n8Photons(dfpTrigger_mean['6FoldpTrigger'],dfpTrigger_mean['8FoldpTrigger'])
dfpTrigger_mean['AvgPhoton'] = (dfpTrigger_mean['Photons78'] + dfpTrigger_mean['Photons68'])/2

ax8 = dfpTrigger_mean.plot.scatter(x='Pressure',y='Photons78',marker="x",c='DarkBlue' , label="Photons78")
ax8_3 = dfpTrigger_mean.plot.scatter(x='Pressure',y='Photons68',marker="x",c='red' , label="Photons68", ax=ax8)
#ax8_3 = dfpTrigger_mean.plot.scatter(x='Pressure',y='AvgPhoton',marker="x",c='green' , label="AvgPhoton", ax=ax8)

ax8.set_ylabel("Photons per PMT")
ax8.set_xlabel("Pressure [bar]")
ax8.legend(loc='upper center',bbox_to_anchor=(0.7,1))
plt.savefig("pdf/{}/Photons.pdf".format(pdfname), format="pdf", bbox_inches="tight")

dfpTrigger_mean['8FoldEff'] = Fold8eff(dfpTrigger_mean['AvgPhoton'])
dfpTrigger_mean['7FoldEff'] = Fold7eff(dfpTrigger_mean['AvgPhoton'],dfpTrigger_mean['8FoldEff']) 
dfpTrigger_mean['6FoldEff'] = Fold6eff(dfpTrigger_mean['AvgPhoton'],dfpTrigger_mean['7FoldEff'])


ax9 = dfpTrigger_mean.plot.scatter(x='Pressure',y='6FoldEff',marker="x",c='DarkBlue' , label="6Fold")
ax9_3 = dfpTrigger_mean.plot.scatter(x='Pressure',y='7FoldEff',marker="x",c='red' , label="7Fold", ax=ax9)
ax9_3 = dfpTrigger_mean.plot.scatter(x='Pressure',y='8FoldEff',marker="x",c='green' , label="8Fold", ax=ax9)

ax9.set_ylabel("Coincidence Efficiency")
ax9.legend(loc='upper center',bbox_to_anchor=(0.7,1))
plt.savefig("pdf/{}/CoincidenceEfficency.pdf".format(pdfname), format="pdf", bbox_inches="tight")


#print(df['Pressure'],df['6Foldeff'])

plt.show()