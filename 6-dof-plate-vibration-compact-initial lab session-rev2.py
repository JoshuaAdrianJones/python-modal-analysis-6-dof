#Vibration of a cantilever plate
#this python script is written as a port of the matlab script used in the lab
#to determine the natural frequencies of the 6 degree of freedom system
import math #standard mathematical library
import numpy

#this version is the lab session code to determine the theoretical values

#functions
def format(x):
    return ('%.5f' % x).rstrip('0').rstrip('.')#function for formatting to 4 decimal places and stripping redundant trailing zeros

def h(displacement):#calculate compliance values m/N x10^-6 converts displacements to compliances for a given load
    load= 0.501 #load in units: kg
    compliance =1e6 *displacement/(1000*load*9.81)#constants here are unit conversions
    return compliance


#functions



#inputs
densAL=2770
holeRadius = 3 # mm
plateThickness = 1.6#mm
plateWidth= 306#mm
boltMass = 9.3*1e-3 # camelCase variable declarations



#this new section of code simplifies the compliance matrix augmentation with the experimentally obtained results:
#input the measured compliance values here: be careful to enter absolute (+ve) values in mm#
#always enter floats rather than integers if the value is 1 enter 1.0 for example 

#displacements in units: mm


d_16=0.2

d_25=0.19

d_33=0.93

d_34=0.63

d_43=0.63

d_44=0.94

d_52=0.22

d_61=0.13


#inputs

###this section is commented out because the compliance matrix is being augmented, not directly calculated - redundent code for illustration only
#loads =  numpy.matrix([
#[1.482, 1.482, 0.976, 0.976, 0.976 ,0.976 ],
#[1.482, 1.482, 0.976, 0.976, 0.976, 0.976],
#[0.976, 0.976, 0.976, 0.976, 0.976, 0.976],
#[0.976, 0.976, 0.976, 0.976, 0.976, 0.976],
#[0.976, 0.976, 0.976, 0.976, 0.498,0.498],
#[0.976, 0.976, 0.976 ,0.976, 0.498, 0.498]
#])
#displacements = 1e-3*numpy.matrix([
#[0.170, 0.050, 0.310, 0.185, 0.500, 0.345],
#[0.050, 0.170, 0.185, 0.310, 0.345, 0.500],
#[ 0.300, 0.180, 1.830, 1.240, 3.420, 2.670],
#[0.180, 0.300, 1.240 ,1.830, 2.670, 3.420],
#[0.420, 0.345, 3.315, 2.505, 3.800, 3.140],
#[ 0.34, 0.420, 2.505, 3.315, 3.140, 3.800],
#]
#)

#flexibility=displacements /(9.81*loads)

###this section is commented out because the compliance matrix is being augmented, not directly calculated - redundent code for illustration only


#calculations
boltHoleMass=math.pi*(holeRadius**2)*plateThickness*densAL*1e-9;#variables should be self descriptive | e-9 is converting the m^3 to mm^3 unit is kg

plateMass = densAL*plateWidth**2*plateThickness*1e-9#unit is kg 

lumpedMass = plateMass/6 + boltMass -boltHoleMass # mass at each concentration 

lumpedMassMatrix= numpy.eye(6)*lumpedMass #build a diagonal matrix with the lumped mass value along the diagonal line, all over values 0
#calculations

#calculate the average compliance values for the flexibility matrix

avg1=numpy.mean(numpy.array([h(d_16),h(d_61),h(d_52),h(d_25)]))#better way to take the average
avg2=numpy.mean(numpy.array([h(d_34),h(d_43)]))
avg3=numpy.mean(numpy.array([h(d_44),h(d_33)]))


flexibility=1e-6*numpy.matrix([
[11.5, 2.7, 28.7, 16.0, 46.0, avg1],
[2.7, 11.5,16.0,28.7, avg1,46.0],
[28.7, 16.0,avg3,avg2,317.0,240.0],
[16.0, 28.7,avg2,avg3,240.0,317.0],
[46.0, avg1, 317.0, 240.0,714.0,575.0],
[avg1, 46.0,240.0, 317.0, 575.0, 714.0],
]
) 


#inverse the lumped mass matrix 
invLumpedMass = numpy.linalg.inv(lumpedMassMatrix)
#inverse the compliance matrix stiffness matrix
stiffnessMatrix=numpy.linalg.inv(flexibility)

#compute the eigenvalue and eigen vector matrix for the two inverses multiplied
A=invLumpedMass*stiffnessMatrix

d,v = numpy.linalg.eig(A)
print lumpedMassMatrix
#print A
print d
print v
#calculate the natural frequency(takes the rad/s values and reports the converted hz values
hz = numpy.sqrt( (numpy.ones((1,6))*d))/(2*numpy.pi)#numpy ones just flattens the diagonal matrix to become a collumn 6x1 matrix 



print '----Python console output----'
print 'The mass of the bolt is '+str(format(boltMass))+' kg' #str is used because the print keyword only takes arguements of the same type so bolt mass is conveted from a float to a string 
print 'The density of aluminium is '+str(densAL)+' kg/m^3'
print 'The mass of the bolt hole (material removed) is: '+ str(format(boltHoleMass))+' kg' #matches the matlab output
print 'The mass of plate is: '+ str(format(plateMass))+' kg' #matches the matlab output
print 'the lumped system mass at each of the six points is: '+ str(format(lumpedMass))+' kg'

print 'compliance matrix average value 1 is: ' + str(avg1)
print 'compliance matrix average value 2 is: ' + str(avg2)
print 'compliance matrix average value 3 is: ' + str(avg3)  

for i in xrange(0,6):#saves time typing multiple print lines, accesses the hz(i) values stored in the array hz
    print 'mode '+str((i+1))+' is: '+str(format(hz.item(5-i))) +' hz'