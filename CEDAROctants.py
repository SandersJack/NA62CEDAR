from cProfile import label
from random import seed
from random import random
from random import randint
from scipy.stats import poisson
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import mplhep as hep
plt.style.use(hep.style.ROOT)

seed(987665)
mu = np.linspace(15,30,31)
nSectors_ = []
nHits_ = []
totalrings = 100000
for l in range(len(mu)):
    nSectors = []
    nHits = []
    for ring in range(totalrings):
        nphotons = poisson.rvs(mu[l])
        octantHits = [0,0,0,0,0,0,0,0]
        octantbool = [0,0,0,0,0,0,0,0]
        for photon in range(nphotons):
            octant = randint(0,7)
            octantHits[octant] += 1
            octantbool[octant] = 1
        nSectors.append(sum(octantbool))
        nHits.append(sum(octantHits))
    nSectors_.append(nSectors)
    nHits_.append(nHits)

n8Sectors_ = []
n7Sectors_ = []
n6Sectors_ = []
for v in range((len(mu))):
    n8Sectors = n7Sectors = n6Sectors = 0
    for t in range(len(nSectors)):
        if nSectors_[v][t] > 7:
            n8Sectors += 1
        if nSectors_[v][t] > 6:
            n7Sectors += 1
        if nSectors_[v][t] > 5:
            n6Sectors += 1
    n6Sectors_.append(n6Sectors)
    n7Sectors_.append(n7Sectors)
    n8Sectors_.append(n8Sectors)     
    print("********************************")
    print("For mu of {}".format(mu[v]))
    print("Number of at least 6 coincidence = {} . fraction of total rings {} ".format(n6Sectors, n6Sectors/totalrings))
    print("Number of at least 7 coincidence = {} . fraction of total rings {} ".format(n7Sectors, n7Sectors/totalrings))
    print("Number of at least 8 coincidence = {} . fraction of total rings {} ".format(n8Sectors, n8Sectors/totalrings))

fig0 = plt.figure()
ax0 = fig0.add_subplot(111)
r87 = []
r76 = []
for v in range((len(mu))):
    sns.histplot(x=nSectors_[v],discrete=True,fill=False,ax=ax0,label="mu={}".format(mu[v]),weights=np.full(totalrings,1/totalrings))
    r87.append(float(n8Sectors_[v])/n7Sectors_[v])
    r76.append(float(n7Sectors_[v]/n6Sectors_[v]))
    
ax0.set(xlabel='N Coincidences', ylabel='Fraction of Total Triggers',title="Exactly N Fold Coincidences")
ax0.legend()
plt.savefig("pdf/OctantSim/Coincidences.pdf", format="pdf", bbox_inches="tight")

fig = plt.figure()
ax1 = fig.add_subplot(111)

ax1.plot(mu,r87, label="R87",linestyle='--', marker='o', color='r')
ax1.plot(mu,r76, label="R76", linestyle='--', marker='o', color='b')

ax1.legend()
ax1.set_xlabel(r"Mean number of photoelectrons ($\lambda$)")
ax1.set_title("Ratio of cumulative coincidence probabilities")
plt.savefig("pdf/OctantSim/RatioPlot.pdf", format="pdf", bbox_inches="tight")
plt.show()
