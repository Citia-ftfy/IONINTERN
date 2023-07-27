#THIS FILE IS TO RUN TM_DRIVER CPP COMMANDS - Isaac Merwin June 2023
import subprocess
import time
import argparse
import random as rd
import magnetControl as mC
import moveSplitter as mS
#import robonet



#Position Data
zeroArray = [0,0,0,0,0,0] #sets to what ill call the zero point
gondolaArray = [0,-0.3,-0.610865,0.910865,-1.58,0] #TODO fix this, this is the stopping gondola point
homeArray = [1,1.5,1.5,1.5,0,0] #TODO fix this, away position so users can see the screen
wavePos1 = [1.58,-1.58,1.58,1.58,0,1.58]
wavePos2 = [1.58,1.58,-1.58,-1.58,0,-1.58]
blackMarker = [0,0.74,1.24,-0.4,1.58,0] #TODO
greenMarker = [] #TODO
redMarker = [] #TODO 
blueMarker = [] #TODO
selectedMarker = []
selectedDirection = False
roboVelocity = 1.0
roboAccelTime = 0.4
previousPoint = zeroArray

#Parse args
parser = argparse.ArgumentParser()
parser.add_argument('-r','--random',action='store_true',default=False)
parser.add_argument('-c','--continuous',action='store_true',default=False)
parser.add_argument('-hp','--home',action='store_true',default=False)
parser.add_argument('-gp','--gondola',action='store_true',default=False)
parser.add_argument('-wave','--wave',action='store_true',default=False)
parser.add_argument('-sp','--setpos', type=float, nargs=6, default=zeroArray)
parser.add_argument('-moveSplit','--moveSplit',action='store_true',default=False)
parser.add_argument('-mm','--moveMarker',action='store_true',default=False)
parser.add_argument('-markerSet','--markerSet',type=str,nargs=2,default=["black","True"])
args = parser.parse_args()

if(args.markerSet[0].lower()=="black"):
    selectedMarker=blackMarker
elif(args.markerSet[0].lower()=="red"):
    selectedMarker=redMarker
elif(args.markerSet[0].lower()=="green"):
    selectedMarker=greenMarker
elif(args.markerSet[0].lower()=="blue"):
    selectedMarker=blueMarker
else:
    raise Exception("Color not of expected type (black, red, green, blue) case insensitive")
    


j1 = str(args.setpos[0])
j2 = str(args.setpos[1])
j3 = str(args.setpos[2])
j4 = str(args.setpos[3])
j5 = str(args.setpos[4])
j6 = str(args.setpos[5])
#start rand gen
rd.seed(a=None, version=2)

#Source tm files just incase
output = subprocess.getoutput("source ~/tm_ws/devel/setup.bash")
print(output)

def strtobool (val):
    """Convert a string representation of truth to true (1) or false (0).
    True values are 'y', 'yes', 't', 'true', 'on', and '1'; false values
    are 'n', 'no', 'f', 'false', 'off', and '0'.  Raises ValueError if
    'val' is anything else.
    """
    val = val.lower()
    if val in ('y', 'yes', 't', 'true', 'on', '1'):
        return True
    elif val in ('n', 'no', 'f', 'false', 'off', '0'):
        return False
    else:
        raise ValueError("invalid truth value %r" % (val,))

selectedDirection = strtobool(args.markerSet[1])

def setArray(a1,a2,a3,a4,a5,a6):
    temp_array = [a1,a2,a3,a4,a5,a6]
    if(len(temp_array)<6):
        raise Exception("set Array did not get enough data to set array breaking - setArray in runner.py")
    return(temp_array)

def robo_sp(positionsArray):
    if(len(positionsArray) == 6):
        pA = positionsArray
    else:
        print("To little points given to robo_sp in runner.py")
        print("going home")
        pA = zeroArray   
    if(args.moveSplit):
        #previousPoint = previousPoint
        splitPoints = mS.getSplits(zeroArray,pA)
        for point in splitPoints:
            j1 = point[0]
            j2 = point[1]
            j3 = point[2]
            j4 = point[3]
            j5 = point[4]
            j6 = point[5]
            j1 = str(j1)
            j2 = str(j2)
            j3 = str(j3)
            j4 = str(j4)
            j5 = str(j5)
            j6 = str(j6)
            rVelocity = str(roboVelocity)
            rAccelTime = str(roboAccelTime)
            print("rosrun demo demo_set_positions "+j1+" "+j2+" "+j3+" "+j4+" "+j5+" "+j6+" "+rVelocity+" "+rAccelTime)
            output = subprocess.getoutput("rosrun demo demo_set_positions "+j1+" "+j2+" "+j3+" "+j4+" "+j5+" "+j6+" "+rVelocity+" "+rAccelTime)
            print(output)
            previousPoint=point 
    else:
        j1 = pA[0]
        j2 = pA[1]
        j3 = pA[2]
        j4 = pA[3]
        j5 = pA[4]
        j6 = pA[5]
        j1 = str(j1)
        j2 = str(j2)
        j3 = str(j3)
        j4 = str(j4)
        j5 = str(j5)
        j6 = str(j6)
        rVelocity = str(roboVelocity)
        rAccelTime = str(roboAccelTime)
        print("rosrun demo demo_set_positions "+j1+" "+j2+" "+j3+" "+j4+" "+j5+" "+j6+" "+rVelocity+" "+rAccelTime)
        output = subprocess.getoutput("rosrun demo demo_set_positions "+j1+" "+j2+" "+j3+" "+j4+" "+j5+" "+j6+" "+rVelocity+" "+rAccelTime)
        print(output)
        previousPoint=pA
    #roboVelocity = 0.4
    #roboAccelTime = 0.2

def robo_sp_moveSeperate(positionsArray):
    if(len(positionsArray) == 6):
        pA = positionsArray
    else:
        print("To little points given to robo_sp in runner.py")
        print("going home")
        pA = zeroArray   
    j1 = pA[0]
    j2 = pA[1]
    j3 = pA[2]
    j4 = pA[3]
    j5 = pA[4]
    j6 = pA[5]
    j1 = str(j1)
    j2 = str(j2)
    j3 = str(j3)
    j4 = str(j4)
    j5 = str(j5)
    j6 = str(j6)
    rVelocity = str(roboVelocity)
    rAccelTime = str(roboAccelTime)
    zero = str(0)
    print("rosrun demo demo_set_positions "+j1+" "+j2+" "+j3+" "+j4+" "+j5+" "+j6+" "+rVelocity+" "+rAccelTime)
    output = subprocess.getoutput("rosrun demo demo_set_positions "+j1+" "+zero+" "+zero+" "+zero+" "+zero+" "+zero+" "+rVelocity+" "+rAccelTime)
    print(output)
    output = subprocess.getoutput("rosrun demo demo_set_positions "+j1+" "+j2+" "+zero+" "+zero+" "+zero+" "+zero+" "+rVelocity+" "+rAccelTime)
    print(output)
    output = subprocess.getoutput("rosrun demo demo_set_positions "+j1+" "+j2+" "+j3+" "+zero+" "+zero+" "+zero+" "+rVelocity+" "+rAccelTime)
    print(output)
    output = subprocess.getoutput("rosrun demo demo_set_positions "+j1+" "+j2+" "+j3+" "+j4+" "+zero+" "+zero+" "+rVelocity+" "+rAccelTime)
    print(output)
    output = subprocess.getoutput("rosrun demo demo_set_positions "+j1+" "+j2+" "+j3+" "+j4+" "+j5+" "+zero+" "+rVelocity+" "+rAccelTime)
    print(output)
    output = subprocess.getoutput("rosrun demo demo_set_positions "+j1+" "+j2+" "+j3+" "+j4+" "+j5+" "+j6+" "+rVelocity+" "+rAccelTime)
    print(output)
    previousPoint=pA
    #roboVelocity = 0.4
    #roboAccelTime = 0.2

def robo_random():
    time.sleep(4)
    randr = rd.choice([1])*rd.random()
    randr2 = rd.choice([1])*rd.random()
    j1 = randr
    j2 = randr2/2
    j3 = randr2/2
    j4 = randr2*(-1)
    j5 = randr+1.58
    j6 = 0
    robo_sp(setArray(j1,j2,j3,j4,j5,j6))
    
    
def robo_wave():
    robo_sp(wavePos1)
    time.sleep(18)
    robo_sp(wavePos2)
    time.sleep(18)


def robo_magnet(magIsOn):
    if(magIsOn):
        mC.set_high()
    else:
        mC.set_low()
#TODO NOT TRUE

def moveMarker(toOrFrom,positionsArray):
    #toOrFrom = True: going to gondola, False: coming from gondola
    #positionsArray: Array of joint positions of the marker in question
    #TODO FIX TIMINGS
    pA = positionsArray
    if(toOrFrom):
        robo_sp(zeroArray)
        robo_sp(pA)
        time.sleep(12)
        robo_magnet(True) #Turn magnet on
        print("Magnet On")
        time.sleep(1)
        robo_sp(zeroArray)
        robo_sp(gondolaArray)
        time.sleep(15)
        robo_magnet(False) #Turn magnet off
        print("Magnet Off")
        time.sleep(1)
        robo_sp(zeroArray)
        #robo_sp(homeArray)
        time.sleep(15)
    else:
        robo_sp(zeroArray)
        robo_sp(gondolaArray)
        time.sleep(17)
        robo_magnet(True) #Turn magnet on
        print("Magnet On")
        time.sleep(1)
        robo_sp(zeroArray)
        robo_sp(pA)
        time.sleep(17)
        robo_magnet(False) #Turn magnet off
        print("Magnet Off")
        time.sleep(1)
        robo_sp(zeroArray)
        #robo_sp(homeArray)
        time.sleep(15)
        
        


test_bool = True

#Make this some kind of listener 

while(test_bool):
    robo_magnet(False)
    if(args.moveMarker):
        moveMarker(selectedDirection,selectedMarker)
    if(args.home):
        robo_sp(homeArray)
    if(args.gondola):
        robo_sp(gondolaArray)
    if(args.wave):
        robo_wave()
    if(not args.gondola and not args.home and not args.random and not args.wave and not args.moveMarker):
        robo_sp_moveSeperate(setArray(j1,j2,j3,j4,j5,j6))
    if(args.random):
        robo_random()
    if not (args.continuous):
        break
    time.sleep(2)
    

