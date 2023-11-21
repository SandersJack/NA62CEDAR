import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib import gridspec
import numpy as np 

#fwavelength = [200,225,250,275,300,325]
#fwavelength1 = [350,375,400,600] 
#fpoints = [0.8550,0.875,0.8875,0.8925,0.894,0.895]
#fpoints1 = [0.894,0.893,.8925,0.7]

fwavelength = [200,225,250,275,300,325,350]
fwavelength1 = [350,375,400,600] 

fpoints = [0.044,0.0425,0.037,0.03,0.026,0.0225,0.0205]
fpoints1 = [0.0205,0.019,.019,0.019]

z = np.polyfit(fwavelength,fpoints,3)
z2 = np.polyfit(fwavelength1,fpoints1,3)

xz = np.linspace(200,335,6)
xz2 = np.linspace(335,600,50)

def eq(z_,x):
    return z_[0]*x**3 + z_[1]*x**2 + z_[2]*x + z_[3]

def eq4(z_,x):
    return z_[0]*x**4 + z_[1]*x**3 + z_[2]*x**2 + z_[3]*x + z_[4]
test = eq(z,xz) 
test2 = eq(z2,xz2)

print(z)
print(z2)

plt.plot(fwavelength,fpoints ,'.' )
plt.plot(xz,np.polyval(z, xz))
plt.plot(xz,test)
plt.plot(fwavelength1,fpoints1 ,'.' )
plt.plot(xz2,np.polyval(z2, xz2))
plt.plot(xz2,test2)
plt.legend(fontsize="small")
plt.show()

