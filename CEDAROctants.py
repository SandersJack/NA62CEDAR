from cProfile import label
from random import seed
from random import random
from random import randint
from scipy.stats import poisson
import seaborn as sns
import matplotlib.pyplot as plt

seed(987665)
mu = [15,20,25]
nSectors_ = []
nHits_ = []
totalrings = 10000
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

n8Sectors_ = n7Sectors_ = n6Sectors_ = []
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


fig, ax = plt.subplots()
for v in range((len(mu))):
    sns.histplot(data=nSectors_[v],binwidth=1.01,fill=False,ax=ax,label="mu={}".format(mu[v]))

ax.legend()

ax.set(xlabel='N Coincidences', ylabel='Coincidences',title="Exactly N Fold Coincidences")
plt.show()
