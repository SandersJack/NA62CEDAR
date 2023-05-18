import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib import gridspec
import numpy as np 
import pandas as pd

nIndex = False

if(nIndex):

    df = pd.read_csv('RefractiveIndexINFO_MgF2.csv')

    df['nm'] = df['Wavelength, µm'] * 1e3

    data = df.loc[(df['nm'] > 180) & (df['nm'] < 700)][['nm','n']]


    z = np.polyfit(data['nm'],data['n'],5)

    print(z)
    wave = np.linspace(180,700,100)

    plt.plot(data['nm'],data['n'])
    plt.plot(wave,np.polyval(z, wave))
    plt.show()
    
else:
    
    df = pd.read_csv('transmittance_MgF2.csv')
    
    df['nm'] = df['Wavelength, µm'] * 1e3

    data = df.loc[(df['nm'] > 180) & (df['nm'] < 700)][['nm','T']]
    
    z = np.polyfit(data['nm'],data['T'],5)

    print(z)
    wave = np.linspace(180,700,100)
    
    plt.plot(data['nm'],data['T'])
    plt.plot(wave,np.polyval(z, wave))
    plt.show()