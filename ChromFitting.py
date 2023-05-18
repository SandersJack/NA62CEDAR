import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib import gridspec
import numpy as np 

#fwavelength = [200,225,250,275,300,325,350,375,400]
#fpoints = [0.0575,0.04574,0.04,0.034,0.028,0.025,0.0225,0.0205,0.02] ##F1

fwavelength = [200,225,250,275,300,325,350,375,400]
fpoints = [0.045,0.0415,0.035,0.029,0.025,0.022,0.02,0.019,0.019] ##F2


z = np.polyfit(fwavelength,fpoints,4)

xz = np.linspace(200,400,100)

def eq(z_,x):
    return z_[0]*x**3 + z_[1]*x**2 + z_[2]*x + z_[3]

def eq4(z_,x):
    return z_[0]*x**4 + z_[1]*x**3 + z_[2]*x**2 + z_[3]*x + z_[4]

test = eq4(z,xz)

print(z)

plt.plot(fwavelength,fpoints ,'.' )
plt.plot(xz,np.polyval(z, xz))
plt.plot(xz,test)
plt.legend(fontsize="small")
plt.show()

