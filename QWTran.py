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
'''

fwavelength = [250,300,350,400,450,500,550,600,650,700]
fpoints = [0.93,0.955,0.965,0.965,0.962,0.96,0.958,0.955,0.952,0.95]

z = np.polyfit(fwavelength,fpoints,4)

xz = np.linspace(240,700,100)

def eq(x):
    return z[0]*x**4 + z[1]*x**3 + z[2]*x**2 + z[3]*x+z[4]

test = eq(xz)

print(z)

x = symbols("x")
poly = sum(S("{:6.2f}".format(v))*x**i for i, v in enumerate(z[::-1]))
eq_latex = printing.latex(poly)

plt.plot(fwavelength,fpoints ,'.' )
#plt.plot(xz,np.polyval(z, xz), label="${}$".format(eq_latex))
plt.plot(xz,test)
plt.legend(fontsize="small")
plt.show()

'''

def QuartzWindowAndFilterTransmittance(wavelength):
    x = wavelength
    f = 0
    if(x > 350):
        f = 0.905 + 0.00008 * (x - 350)
    elif(x > 300):
        f = 0.875 + 0.030 * (x - 300) / 50.0
    elif(x > 280):
        f = 0.845 + 0.030 * (x - 280) / 20.0
    elif(x > 270):
        f = 0.815 + 0.030 * (x - 270) / 10.0
    elif(x > 260):
        f = 0.760 + 0.055 * (x - 260) / 10.0
    elif(x > 250):
        f = 0.670 + 0.090 * (x - 250) / 10.0
    elif(x > 240):
        f = 0.490 + 0.180 * (x - 240) / 10.0
    else:
        f = 0.232 + 0.258 * (x - 230) / 10.0
    if(f < 0.001):
        f = 0.001
    if(f > 0.999):
        f = 0.999
    return f


oldx = np.linspace(220,800,100)
oldy = []
for i in range(len(oldx)):
    oldy.append(QuartzWindowAndFilterTransmittance(oldx[i]))

df = pd.read_excel(r'NA62CedarTRMofExitwindows.xlsx')
print(df)

fig = plt.figure(figsize=(12, 10))
gs = gridspec.GridSpec(nrows=2, ncols=1, height_ratios=[3, 1])
ax = plt.subplot(gs[0])
ax1 = plt.subplot(gs[1])

col = ['tab:blue','tab:orange','tab:green','tab:red','tab:purple','tab:brown','tab:pink','tab:grey','tab:olive','tab:cyan']

for i in range(1,9):
    
    df['Window#{}'.format(i)] = df['Window#{}'.format(i)] / 100
    
    df250 = df.loc[(218 <= df['nm']) & (df['nm'] < 248)]
    df350 = df.loc[(240 <= df['nm']) & (df['nm'] < 300)]
    df400 = df.loc[(290 <= df['nm']) & (df['nm'] < 400)]
    df500 = df.loc[(400 <= df['nm']) & (df['nm'] <= 800)]
    
    z = np.polyfit(df250['nm'] ,df250['Window#{}'.format(i)],3)
    ax.plot(df250.loc[(218 <= df250['nm']) & (df250['nm'] < 246)]['nm'],np.polyval(z, df250.loc[(218 <= df250['nm']) & (df250['nm'] < 246)]['nm']),color=col[i-1],label='Window#{}'.format(i))
    
    z2 = np.polyfit(df350['nm'], df350['Window#{}'.format(i)],3)
    ax.plot(df350.loc[(246 <= df350['nm']) & (df350['nm'] < 295)]['nm'],np.polyval(z2, df350.loc[(246 <= df350['nm']) & (df350['nm'] < 295)]['nm']),color=col[i-1])
    
    z3 = np.polyfit(df500['nm'], df500['Window#{}'.format(i)],3)
    ax.plot(df500['nm'],np.polyval(z3, df500['nm']),color=col[i-1])
    
    z4 = np.polyfit(df400['nm'], df400['Window#{}'.format(i)],3)
    ax.plot(df400.loc[(295 <= df400['nm']) & (df400['nm'] < 400)]['nm'],np.polyval(z4, df400.loc[(295 <= df400['nm']) & (df400['nm'] < 400)]['nm']),color=col[i-1])
 
 
    vals = []
    
    
    
    
    tmp = list(np.polyval(z3, df500['nm']))
    for v in range(len(tmp)):
        vals.append(tmp[v])
    tmp = list(np.polyval(z4, df400.loc[(295 <= df400['nm']) & (df400['nm'] < 400)]['nm']))
    for v in range(len(tmp)):
        vals.append(tmp[v])
    tmp = list(np.polyval(z2, df350.loc[(246 <= df350['nm']) & (df350['nm'] < 295)]['nm']))
    for v in range(len(tmp)):
        vals.append(tmp[v])
    tmp = list(np.polyval(z, df250.loc[(218 <= df250['nm']) & (df250['nm'] < 246)]['nm']))
    for v in range(len(tmp)):
        vals.append(tmp[v])
    
    
    ax1.scatter(df['nm'][:-18][::10],df['Window#{}'.format(i)][:-18][::10]-vals[::10],color=col[i-1])
    ax.scatter(df['nm'][:-19][::10],df['Window#{}'.format(i)][:-19][::10],s=4,color='black')
    print('Window#{}'.format(i))
    print('f = {}*pow(x,3) + {}*pow(x,2) + {}*x + {}'.format(z[0],z[1],z[2],z[3]))
    print('f = {}*pow(x,3) + {}*pow(x,2) + {}*x + {}'.format(z2[0],z2[1],z2[2],z2[3]))
    print('f = {}*pow(x,3) + {}*pow(x,2) + {}*x + {}'.format(z4[0],z4[1],z4[2],z4[3]))
    print('f = {}*pow(x,3) + {}*pow(x,2) + {}*x + {}'.format(z3[0],z3[1],z3[2],z3[3]))
    
ax.scatter(df['nm'][:-19][::10],df['Window#1'][:-19][::10],s=4,color='black',label="Data")   
ax.plot(oldx,oldy,"--",label="CEDAR-W QW+UV Filters")
ax.set_ylabel("Transmittance")
ax.set_xlabel("Wavelength [nm]")
ax.set_xlim(160,700)
ax1.set_xlim(160,700)
ax1.set_ylabel("Data - Fitted Data")
ax.set_title("Fitted data for Transmittance of CEDAR-H Quartz Windows + UV Filters")
ax.legend()
plt.show()