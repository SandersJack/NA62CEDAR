import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib import gridspec
import mplhep as hep
plt.style.use(hep.style.ROOT)
import numpy as np 
from sympy import S, symbols, printing
import pandas as pd
from scipy.optimize import curve_fit
from functools import reduce


df = pd.read_csv(r'NA62_H_CEDAR_reflectivity_Biconvex_lenses.csv')
print(df)

fig = plt.figure(figsize=(12, 10))
gs = gridspec.GridSpec(nrows=2, ncols=1, height_ratios=[3, 1])
ax = plt.subplot(gs[0])
ax1 = plt.subplot(gs[1])

col = ['tab:blue','tab:orange']

for i in range(2): ## 0 = 1-4 ## 1 = 5-9
    
    df['{}'.format(i)] = df['{}'.format(i)] / 100
    
    df250 = df.loc[(200 <= df['nm']) & (df['nm'] < 340)]
    df3   = df.loc[(330 <= df['nm']) & (df['nm'] < 450)]
    df350 = df.loc[(450 <= df['nm']) & (df['nm'] < 490)]
    df400 = df.loc[(490 <= df['nm']) & (df['nm'] < 540)]
    df500 = df.loc[(540 <= df['nm']) & (df['nm'] <= 800)]
    
    z = np.polyfit(df250['nm'] ,df250['{}'.format(i)],3)
    ax.plot(df250.loc[(200 <= df250['nm']) & (df250['nm'] < 330)]['nm'],np.polyval(z, df250.loc[(200 <= df250['nm']) & (df250['nm'] < 330)]['nm']),color=col[i-1],label='{}'.format(i))
    
    z0 = np.polyfit(df3['nm'] ,df3['{}'.format(i)],3)
    ax.plot(df3.loc[(330 <= df3['nm']) & (df3['nm'] < 450)]['nm'],np.polyval(z0, df3.loc[(330 <= df3['nm']) & (df3['nm'] < 450)]['nm']),color=col[i-1])
    
    z2 = np.polyfit(df350['nm'], df350['{}'.format(i)],3)
    ax.plot(df350.loc[(450 <= df350['nm']) & (df350['nm'] < 490)]['nm'],np.polyval(z2, df350.loc[(450 <= df350['nm']) & (df350['nm'] < 490)]['nm']),color=col[i-1])
    
    z3 = np.polyfit(df500['nm'], df500['{}'.format(i)],3)
    ax.plot(df500['nm'],np.polyval(z3, df500['nm']),color=col[i-1])
    
    z4 = np.polyfit(df400['nm'], df400['{}'.format(i)],3)
    ax.plot(df400.loc[(490 <= df400['nm']) & (df400['nm'] < 540)]['nm'],np.polyval(z4, df400.loc[(490 <= df400['nm']) & (df400['nm'] < 540)]['nm']),color=col[i-1])
 
 
    vals = []
    
    
    
    
    tmp = list(np.polyval(z3, df500['nm']))
    for v in range(len(tmp)):
        vals.append(tmp[v])
    tmp = list(np.polyval(z4, df400.loc[(490 <= df400['nm']) & (df400['nm'] < 540)]['nm']))
    for v in range(len(tmp)):
        vals.append(tmp[v])
    tmp = list(np.polyval(z2, df350.loc[(450 <= df350['nm']) & (df350['nm'] < 490)]['nm']))
    for v in range(len(tmp)):
        vals.append(tmp[v])
    tmp = list(np.polyval(z0, df3.loc[(330 <= df3['nm']) & (df3['nm'] < 450)]['nm']))
    for v in range(len(tmp)):
        vals.append(tmp[v])   
    tmp = list(np.polyval(z, df250.loc[(200 <= df250['nm']) & (df250['nm'] < 330)]['nm']))
    for v in range(len(tmp)):
        vals.append(tmp[v])
    
    ax1.scatter(df['nm'][::10],df['{}'.format(i)][::10]-vals[::10],color=col[i-1])
    ax.scatter(df['nm'][::10],df['{}'.format(i)][::10],s=4,color='black')
    print('Window#{}'.format(i))
    print('f = {}*pow(x,3) + {}*pow(x,2) + {}*x + {}'.format(z[0],z[1],z[2],z[3]))
    print('f = {}*pow(x,3) + {}*pow(x,2) + {}*x + {}'.format(z0[0],z0[1],z0[2],z0[3]))
    print('f = {}*pow(x,3) + {}*pow(x,2) + {}*x + {}'.format(z2[0],z2[1],z2[2],z2[3]))
    print('f = {}*pow(x,3) + {}*pow(x,2) + {}*x + {}'.format(z4[0],z4[1],z4[2],z4[3]))
    print('f = {}*pow(x,3) + {}*pow(x,2) + {}*x + {}'.format(z3[0],z3[1],z3[2],z3[3]))
    
#ax.scatter(df['nm'][:-19][::10],df['Window#1'][:-19][::10],s=4,color='black',label="Data")   
ax.set_ylabel("Transmittance")
ax.set_xlabel("Wavelength [nm]")
ax.set_xlim(160,700)
ax1.set_xlim(160,700)
ax1.set_ylabel("Data - Fitted Data")
ax.set_title("Fitted data for Reflectivity of CEDAR-H Spherical Mirror")
ax.legend()
plt.show()