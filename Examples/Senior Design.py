import StructPy.cross_sections as xs
import StructPy.structural_classes as sc
import StructPy.Truss as tr
import StructPy.materials as ma
import math

# UNITS: KIPS, INCHES

# Define material
A992 = ma.Custom(E=29000,fy=46)

# Define cross section
#xs1 = xs.IBeam(2, 2, 0.1, 0.1)
#xs1 = xs.AISC("HSS8X8X5/16")
xs1 = xs.AISC("HSS2-1/2X2-1/2X5/16")
# define blank structure
# we will add to this later
s1 = tr.Truss(cross=xs1, material=A992)

# Add nodes to the structure
# bottom chord
n1 = s1.addNode(0,  0, fixity='pin')
n2 = s1.addNode(10*12, 0)
n3 = s1.addNode(20*12, 0)
s1.addNode(30*12, 0, fixity='roller')

#top chord
s1.addNode(5*12, 12*(8+7/12))
s1.addNode(15*12, 12*(8+7/12))
s1.addNode(25*12, 12*(8+7/12))

# Add members to the structure
#bottom chord
m0 = s1.addMember(0, 1)
m1 = s1.addMember(1, 2)
m2 = s1.addMember(2, 3)

#top chord
m3 = s1.addMember(4, 5)
m4 = s1.addMember(5, 6)

#connecting members
m5 = s1.addMember(0, 4)
m6 = s1.addMember(4, 1)
m7 = s1.addMember(1, 5)
m8 = s1.addMember(5, 2)
m9 = s1.addMember(2, 6)
m10 = s1.addMember(6, 3)

s1.plot(labels=False)

import numpy as np

# LOAD FACTORS
Load_case = 1

if Load_case == 1:
	dc = 1.25
	pl = 1.75
	ws = 0
elif Load_case == 2:
	dc = 1.25
	pl = 0
	ws = 1.4
elif Load_case == 3:
	dc = 1.0
	pl = 1.0
	ws = 0.3

print(f"LOAD CASE {Load_case}")

# self weight
# dc is load factor
# /1000 to convert to kips
DC1 = dc * s1.selfWeightAtNodes/1000

# Pedestrian LL

# Tributaty width: 18ft
# tributaty span: 5ft
# ped live load: 90psf
# convert to kips
# pl is load factor
PL = - pl * (5*18*90)/1000

# Deck self weight
# 5 ft tributary span
# 18 ft tributary width
# convert to kips
# dc is dead load factor
DC2 = dc * 5 * 18 * (25+25)/1000

# transverse beams!
DC3 = dc * (18 * xs1.W)/1000

# Dead load from cross braces
length = math.sqrt(10**2 + 18**2)/2
DC4 = dc * (xs1.W * length)/1000

# Wind Loading
WS = ws * 0.7

loading = np.array([WS, PL   -DC1[0] -DC2   -DC3 -2*DC4,
										0, 2*PL -DC1[1] -2*DC2 -DC3 -4*DC4 -pl*10,
										0, 2*PL -DC1[2] -2*DC2 -DC3 -4*DC4,
										0, PL   -DC1[3] -DC2   -DC3 -2*DC4,
										WS, 0    -DC1[4],
										0, 0    -DC1[5],
										0, 0    -DC1[6]
])

s1.directStiffness(loading)

for member in s1.members:
	print(member.axial[0,0])

s1.plotDeformation(scale=100)

minimum_area = 48.72 / 46

sum = sum(member.length for member in s1.members)
print(sum)
