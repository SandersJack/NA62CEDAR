import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib import gridspec
import numpy as np 

def QuartzRefIndex(wavelength):
    x = wavelength
    A = 0.6961663 * x * x / (x * x - 0.0684043 * 0.0684043)
    B = 0.4079426 * x * x / (x * x - 0.1162414 * 0.1162414)
    C = 0.8974794 * x * x / (x * x - 9.8961610 * 9.8961610)
    n = np.sqrt(1.0 + A + B + C)
    return n


w = [184.950,194.227,206.266,214.506,228.872,253.728,312.657,334.244,365.119,404.770,435.957,486.269,546.227,587.725,632.990,656.454,706.714]
n = [1.575017,1.558918,1.542665,1.533722,1.521154,1.505522,1.484493,1.479764,1.474539,1.469615,1.466691,1.463123,1.460076,1.458461,1.457016,1.456364,1.455144]

z = np.polyfit(w,n,5)

print(z)
wave = np.linspace(180,700,100)
data = QuartzRefIndex(wave)

#plt.plot(wave,data)
plt.plot(w,n)
plt.plot(wave,np.polyval(z, wave))
plt.legend(fontsize="small")
plt.show()