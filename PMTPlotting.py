import ROOT
import numpy as np
import matplotlib.pyplot as plt
import mplhep as hep
plt.style.use(hep.style.ROOT)

fig = plt.figure(figsize=(11, 9))
ax = fig.add_subplot(1, 1, 1)

inFile = ROOT.TFile.Open("rootfiles/MCP_N_-18mm_mc.root","READ")
h = inFile.Get("CEDARMC/Photonhits0")

x = np.linspace(h.GetXaxis().GetXmin(), h.GetXaxis().GetXmax()-h.GetXaxis().GetBinWidth(1), num=h.GetNbinsX())
y = np.linspace(h.GetYaxis().GetXmin(), h.GetYaxis().GetXmax()-h.GetYaxis().GetBinWidth(1), num=h.GetNbinsY())

bin = np.empty((h.GetNbinsX() + 1, h.GetNbinsY() + 1), dtype=object)
xmap = []
ymap = []

for i in range(h.GetNbinsX() + 1):
    for t in range(h.GetNbinsY() + 1): 
        bin[i,t] = int(h.GetBinContent(i,t))
        for q in range(bin[i,t]):
            ymap.append(y[t])
            xmap.append(x[i])


print(h.GetNbinsX() + 1,h.GetNbinsY() + 1)
ax.hist2d(xmap,ymap, bins=200, cmin=1, range=[[h.GetXaxis().GetXmin(), h.GetXaxis().GetXmax()], [h.GetYaxis().GetXmin(), h.GetYaxis().GetXmax()]])
ax.set_xlabel("Perpendicular Coordinate (mm)")
ax.set_ylabel("Z (Relative to light Guide Center) (mm)")
ax.set_xlim(-80,80)
ax.set_ylim(-80,80)
ax.set_title("Photon activity on MCP-PMT Array with current NA62 PMT array overlaid")

# add cones
# Light guide geometry (taken from CedarGeometryParameters.cc)
lightguideInnerRadius = 285.0
NoLightguideRows      = 8
NoConesPerRow         = [5,8,9,8,9,8,9,8] # available cones
lightguideRowPhiShift = [0.0]*NoLightguideRows # why?
conePhiShift          = 3.654 # deg
coneThetaShift        = 3.224 # deg
coneLength            = 15.0 # mm
coneOpeningAngle      = 37.0 # deg
coneOuterRadius       = 4.0 # mm
coneInnerRadius       = coneOuterRadius + (coneLength*np.tan(0.5*coneOpeningAngle*np.pi/180))
dx                    = coneInnerRadius*(1-np.cos(np.arcsin(coneInnerRadius/lightguideInnerRadius)))
coneCentreRadius      = lightguideInnerRadius+0.5*coneLength-dx
coneCenter            = coneInnerRadius + 0.5 * coneLength - dx

pmtDiameter           = 8.0
pmtLength             = 1.5
pmtCenter             = 300.611
#print(pmtCenter)
# List used to fade out un-instrumented PMTs

instrumentedPMTsalpha = [0.5, 0.5, 1, 0.5, 0.5,               # row 0 (largest z)
                    0.5, 1, 1, 1, 1, 1, 1, 0.5,          # row 1
                    0.5, 1, 1, 1, 1, 1, 1, 1, 0.5,       # row 2
                    1, 1, 1, 1, 1, 1, 1, 1,              # row 3
                    1, 1, 1, 1, 1, 1, 1, 1, 1,           # row 4
                    1, 1, 1, 1, 1, 1, 1, 1,              # row 5
                    0.5, 1, 1, 1, 1, 1, 1, 1, 0.5,       # row 6
                    0.5, 1, 0.5, 0.5, 0.5, 0.5, 1, 0.5]  # row 7 (smallest z)


instrumentedPMTs = ['--', '--', '-', '--', '--',                   # row 0
                    '--', '-', '-', '-', '-', '-', '-', '--',      # row 1
                    '--', '-', '-', '-', '-', '-', '-', '-', '--', # row 2
                    '-', '-', '-', '-', '-', '-', '-', '-',        # row 3
                    '-', '-', '-', '-', '-', '-', '-', '-', '-',   # row 4
                    '-', '-', '-', '-', '-', '-', '-', '-',        # row 5
                    '--', '-', '-', '-', '-', '-', '-', '-', '--', # row 6
                    '--', '-', '--', '--', '--', '--', '-', '--']  # row 7

instrumentedPMTscolor = ['b', 'b', 'r', 'b', 'b',                   # row 0
                    'b', 'r', 'r', 'r', 'r', 'r', 'r', 'b',      # row 1
                    'b', 'r', 'r', 'r', 'r', 'r', 'r', 'r', 'b', # row 2
                    'r', 'r', 'r', 'r', 'r', 'r', 'r', 'r',        # row 3
                    'r', 'r', 'r', 'r', 'r', 'r', 'r', 'r', 'r',   # row 4
                    'r', 'r', 'r', 'r', 'r', 'r', 'r', 'r',        # row 5
                    'b', 'r', 'r', 'r', 'r', 'r', 'r', 'r', 'b', # row 6
                    'b', 'r', 'b', 'b', 'b', 'b', 'r', 'b']  # row 7
    
coneNo = 0 # cone counter
for iRow in range(0, NoLightguideRows):
    thetaCone = ((iRow - 0.5*(NoLightguideRows - 1))*coneThetaShift + 90) * np.pi/180
    phiRow = (0.5 * conePhiShift * lightguideRowPhiShift[iRow]) * np.pi/180
    for iCone in range(0, NoConesPerRow[iRow]):
        phiCone = (-(iCone - 0.5*(NoConesPerRow[iRow]-1))*conePhiShift - phiRow)* np.pi/180
        #print(conePhiShift,phiRow,NoConesPerRow[iRow])
        zCone = lightguideInnerRadius*np.cos(thetaCone*np.pi/180)
        aCone = lightguideInnerRadius*np.sin(thetaCone*np.pi/180)*np.sin(phiCone*np.pi/180)
        
        zpmt = pmtCenter * np.cos(thetaCone) #+ 0.5*(0.1-1.5) + 0.5 + 0.5
        xpmt = pmtCenter * np.sin(thetaCone) * np.sin(phiCone)

        cone = plt.Circle((xpmt, zpmt), pmtDiameter*0.5, edgecolor=instrumentedPMTscolor[coneNo],
                            facecolor='None', linestyle=instrumentedPMTs[coneNo]) # linestyle was alpha
        ax.add_artist(cone)
        coneNo+=1
        #print(instrumentedPMTs[coneNo])

#plt.grid(alpha=0.5, linestyle='-')
#plt.colorbar()
plt.show()
