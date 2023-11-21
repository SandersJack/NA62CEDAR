import pandas as pd
import csv
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import mplhep as hep
plt.style.use(hep.style.ROOT)
import numpy as np


def ELConvert(value):
  return  1.986446e-25 / value

def LensTransmittance(value):
    return 1.0

def ManginMirrorReflectivity(wavelength):
  x1 = wavelength
  if x1 < 630:
    x = x1
  else:
      x = 630
  refl = -0.261299 + 0.00938637 * x - 2.47446e-05 * x * x + 2.31118e-08 * x * x * x - 5.79119e-12 * x * x * x * x
  if refl < 0:
    refl = 0
  if refl > 1:
    refl = 1
  return refl

def SphericalMirrorAndConeReflectivity(wavelength):
    x = wavelength
    if (x > 450):
        refl = 0.9
    else:
        refl = 0.90 - 0.05 / (450 - 200) * (450 - x)
    return refl


def QuartzWindowTransmittance(iWindow, Wavelength):
    x = Wavelength
    f = -999

    if iWindow == 1 or iWindow == 3 or iWindow == 7:
        if x > 370:
            f = 0.900 + 0.00011 * (x - 370)
        elif x > 270:
            f = 0.910 - 0.010 / 100. * (x - 270)
        elif x > 260:
            f = 0.890 + 0.020 / 10. * (x - 260)
        elif x > 250:
            f = 0.830 + 0.060 / 10. * (x - 250)
        elif x > 240:
            f = 0.790 + 0.040 / 10. * (x - 240)
        elif x > 230:
            f = 0.790
        elif x > 225:
            f = 0.740 + 0.050 / 5. * (x - 225)
        elif x > 220:
            f = 0.640 + 0.100 / 5. * (x - 220)
        elif x > 210:
            f = 0.350 + 0.290 / 10. * (x - 210)
        elif x > 205:
            f = 0.260 + 0.090 / 5. * (x - 205)
        else:
            f = 0.235 + 0.025 / 5. * (x - 200)

    elif(iWindow == 2 or iWindow == 4 or iWindow == 8):
        f = 0.9 + 0.00008 * (x - 200)

    elif(iWindow == 5):
        if x > 380:
            f = 0.92 + 0.0001 * (x - 380)
        elif x > 360:
            f = 0.92
        elif x > 250:
            f = 0.95 - 0.030 / 110. * (x - 250)
        elif x > 240:
            f = 0.95
        elif x > 210:
            f = 0.925 + 0.025 / 30. * (x - 210)
        else:
            f = 0.900 + 0.025 / 10. * (x - 200)


    elif iWindow == 6:
        if x > 500:
            f = 0.946
        elif x > 300:
            f = 0.950 - 0.00002 * (x - 300)
        elif x > 240:
            f = 0.958 - 0.008 / 60. * (x - 240)
        elif x > 210:
            f = 0.940 + 0.018 / 30. * (x - 210)
        else:
            f = 0.914 + 0.026 / 10. * (x - 200)


    if f < 0.001:
        f = 0.001
    if f > 0.999:
        f = 0.999
    return f


def CedarQE_EMI_9820_QB(wavelength):

    wlraw = wavelength
    if wlraw < 141.0:
        wl = 141.0
    elif wlraw > 649.0: 
        wl = 649.0
    else:
        wl = wlraw

    wls = [140, 160, 180, 200, 220, 240, 260, 280, 300, 320, 340, 360,
                            380, 400, 420, 440, 460, 480, 500, 520, 540, 560, 600, 650]
    qes = [0,    20, 21.6, 21.6, 21.4, 21.4, 22,   24, 25, 25.6, 26, 26,
                            26.4, 26, 24.8, 23.2, 20.8, 18,   15.2, 12, 8,  5.6,  2,  0]

    i = 0
    while(True):
        if(wl > wls[i] and wl < wls[i + 1]):
            break
        else:
            i+=1
    return 0.01 * (qes[i] + (wl - wls[i]) / (wls[i + 1] - wls[i]) * (qes[i + 1] - qes[i]))


def gaussian(x, mu, sig):
    return np.exp(-np.power(x - mu, 2.) / (2 * np.power(sig, 2.)))

def CedarQE_R9880U_110(wavelength):
    par = [1489.053765000671,     -20.61340505642701,     0.09607362916193821,
                      -0.000144918944048782, -1.087924475686453e-07, 3.619104979507752e-10,
                      2.742092765095943e-13, -1.067200613381487e-15, 6.333980140159196e-19,
                      4.675391577876988,     505.1903283978535,      15.37334879108591,
                      -23.08738129086531,    358.7521218115685,      53.63424346389683]

    x = wavelength
    if x < 650:
        x1 = x
    else:
        x1 = 650
    qe = 0
    for i in range(9):
        qe += par[i] * x1**i
    qe += par[9] * gaussian(x1, par[10], par[11])
    qe += par[12] * gaussian(x1, par[13], par[14])
    qe *= 0.01
    if(x > 650):
        qe *= (1 - (x - 650) / (675 - 650))
    if(qe < 0 or x < 200):
        qe = 0
    return qe

def CedarQE_EMI_9820_QB_Lau(wavelength):
    wl = wavelength
    qe = 0.25 - ((wl - 400) / 500.) ** 2
    if(qe < 0):
        qe = 0
    return qe


def JackTest(wavelength):
    wl = wavelength
    emi = CedarQE_EMI_9820_QB(wavelength)
    ktag = CedarQE_R9880U_110(wavelength)
    if(emi < ktag):
        return emi
    else:
        return ktag

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

def CedarQE_R7400U_03(wavelength):
    par = [-58.41145755814,     1.450540667766,      -0.01561331198442,
                            9.545010080831e-05,  -3.648461145542e-07, 9.047599515597e-10,
                            -1.457151808585e-12, 1.471328774241e-15,  -8.46121819724e-19,
                            2.11384701372e-22]

    x = wavelength
    if(x < 180):
        return 0
    if(x > 660):
        return 0
        
    qe = 0
    for i in range(10):
        qe += par[i] * x**i
    
    if(qe < 0):
        qe = 0
    return qe


#w = open('MCOptics/.csv', 'w')
#writer = csv.writer(w)
#writer.writerow(["Wavelength","Transmitance"])

fCherenkovLambdaMin = 180e-9
fCherenkovLambdaMax = 700e-9
fCherenkovPhotonEnergyMin = ELConvert(fCherenkovLambdaMax)
fCherenkovPhotonEnergyMax = ELConvert(fCherenkovLambdaMin)   

fMaterialPropertiesNEntries = 50

fPhotonEnergy = []
fWavelength = []
fLensTransmittance = []
fManginMirrorReflectivity = []
fQuartzWindowTransmittance = []
fCedarQE_EMI_9820_QB = []
fCedarQE_R9880U_110 = []
fCedarQE_EMI_9820_QB_Lau = []
fJack = []
fQuartzWindowAndFilterTransmittance = []
fCedarQE_R7400U_03 = []


for i in range(fMaterialPropertiesNEntries):
    fPhotonEnergy.append(fCherenkovPhotonEnergyMin
                       + (fCherenkovPhotonEnergyMax - fCherenkovPhotonEnergyMin)
                           / (fMaterialPropertiesNEntries - 1) * i)
    fWavelength.append(ELConvert(fPhotonEnergy[i])* 10**9)
    fLensTransmittance.append(LensTransmittance(fWavelength[i]))
    fManginMirrorReflectivity.append(ManginMirrorReflectivity(fWavelength[i]))
    fCedarQE_EMI_9820_QB.append(CedarQE_EMI_9820_QB(fWavelength[i]))
    fCedarQE_R9880U_110.append(CedarQE_R9880U_110(fWavelength[i]))
    fCedarQE_EMI_9820_QB_Lau.append(CedarQE_EMI_9820_QB_Lau(fWavelength[i]))
    fJack.append(JackTest(fWavelength[i]))
    fQuartzWindowAndFilterTransmittance.append(QuartzWindowAndFilterTransmittance(fWavelength[i]))
    fCedarQE_R7400U_03.append(CedarQE_R7400U_03(fWavelength[i]))
    

fig0, ax0 = plt.subplots(1, 1, figsize=(10, 10))
ax0.set_title("NA62 CEDAR-W MC QW Transmittance vs Wavelength")

for t in range(1,9):
    temp = []
    for q in range(fMaterialPropertiesNEntries):
        temp.append(QuartzWindowTransmittance(t, fWavelength[q]))   
    
    fQuartzWindowTransmittance.append(temp)
    ax0.scatter(fWavelength,fQuartzWindowTransmittance[t-1],label="QW {}".format(t),s=100/t)
    
ax0.set_xlabel("Wavelength [nm]")
ax0.set_ylabel("Transmittance")
ax0.legend()
ax0.grid(True)
    
fig, ax = plt.subplots(1, 1, figsize=(10, 10))
ax.plot(fWavelength,fLensTransmittance)
ax.set_title("MC Lens Transmittance vs Wavelength")
ax.set_xlabel("Wavelength")

fig1, ax1 = plt.subplots(1, 1, figsize=(10, 10))
ax1.plot(fWavelength,fManginMirrorReflectivity)
ax1.set_title("MC Mangin Mirror Reflectivity vs Wavelength")
ax1.set_xlabel("Wavelength")

fig2, ax2 = plt.subplots(1, 1, figsize=(10, 10))
ax2.plot(fWavelength,fCedarQE_EMI_9820_QB, label="CEDAR-W Test-Beam PMTs (CedarQE_EMI_9820)")
ax2.plot(fWavelength,fCedarQE_R9880U_110, label="KTAG PMTs (CedarQE_R9880U)")
#ax2.plot(fWavelength,fCedarQE_EMI_9820_QB_Lau, label="CedarQE_EMI_9820_QB_Lau")
ax2.plot(fWavelength,fCedarQE_R7400U_03, label="KTAG PMTs (CedarQE_R7400U_03)")
ax2.set_title("MC PMT QE vs Wavelength")
ax2.set_xlabel("Wavelength[nm]")
ax2.set_ylabel("QE")
ax2.legend()

fig4, ax3 = plt.subplots(1, 1, figsize=(10, 10))
ax3.plot(fWavelength,fQuartzWindowAndFilterTransmittance)
ax3.set_title("CEDAR-W MC Quartz Window + UV Filter Transmittance vs Wavelength")
ax3.set_xlabel("Wavelength [nm]")
ax3.set_ylabel("Transmittance")
ax3.legend()


plt.show()

    
