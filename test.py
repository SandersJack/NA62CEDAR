import matplotlib.pyplot as plt
import numpy as np 


def n6n8Photons(ratio):
    return np.log(1+((14)/(np.sqrt(4-7*(1-ratio))-2)))

x = np.linspace(1.01,2,100)
y = n6n8Photons(x)

plt.plot(x,y)

plt.plot([1.23,1.23],[2,n6n8Photons(1.23)],"--",color="orange",label="CEDAR-H with PMT CE")
plt.plot([1,1.23],[n6n8Photons(1.23),n6n8Photons(1.23)],"--",color="orange")

plt.plot([1.0489,1.0489],[2,n6n8Photons(1.0489)],"--",color="brown",label="CEDAR-H without PMT CE")
plt.plot([1,1.0489],[n6n8Photons(1.0489),n6n8Photons(1.0489)],"--",color="brown")

plt.plot([1.27,1.27],[2,n6n8Photons(1.27)],"--",color="limegreen",label="CEDAR-W with PMT CE")
plt.plot([1,1.27],[n6n8Photons(1.27),n6n8Photons(1.27)],"--",color="limegreen")

plt.plot([1.08129,1.08129],[2,n6n8Photons(1.08129)],"--",color="darkgreen",label="CEDAR-W without PMT CE")
plt.plot([1,1.08129],[n6n8Photons(1.08129),n6n8Photons(1.08129)],"--",color="darkgreen")


print(n6n8Photons(2.019))

plt.ylabel("NPhoto Electrons")
plt.xlabel("${n_6}/{n_8}$")
plt.xlim(1,2)
plt.ylim(2,6.5)
plt.title("Nphoto Electrons per PMT vs Ratio of 6FOLD and 8FOLD Coincidences")
plt.legend()
#plt.show()
