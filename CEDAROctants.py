from random import seed
from random import random
from random import randint
from scipy.stats import poisson
import seaborn as sns
import matplotlib.pyplot as plt


seed(987665)
mu = 18
nSectors = []
nHits = []
totalrings = 10000

for ring in range(totalrings):
    nphotons = poisson.rvs(mu)
    octantHits = [0,0,0,0,0,0,0,0]
    octantbool = [0,0,0,0,0,0,0,0]
    for photon in range(nphotons):
        octant = randint(0,7)
        octantHits[octant] += 1
        octantbool[octant] = 1
        
    nSectors.append(sum(octantbool))
    nHits.append(sum(octantHits))

n8Sectors = n7Sectors = n6Sectors = 0
for t in range(len(nSectors)):
    if nSectors[t] > 7:
        n8Sectors += 1
    if nSectors[t] > 6:
        n7Sectors += 1
    if nSectors[t] > 5:
        n6Sectors += 1
        
print("********************************")
print("Number of 6 coincidence = {} . fraction of total rings {} ".format(n6Sectors, n6Sectors/totalrings))
print("Number of 7 coincidence = {} . fraction of total rings {} ".format(n7Sectors, n7Sectors/totalrings))
print("Number of 8 coincidence = {} . fraction of total rings {} ".format(n8Sectors, n8Sectors/totalrings))


sns.histplot(data=nSectors)
plt.show()
