import numpy as np
import os.path
import cv2


CMD_CHANGELENGTH = "C01,"
CMD_CHANGEPENWIDTH = "C02,"
CMD_CHANGEMOTORSPEED = "C03,"
CMD_CHANGEMOTORACCEL = "C04,"
CMD_DRAWPIXEL = "C05,"
CMD_DRAWSCRIBBLEPIXEL = "C06,"
CMD_DRAWRECT = "C07,"
CMD_CHANGEDRAWINGDIRECTION = "C08,"
CMD_SETPOSITION = "C09,"
CMD_TESTPATTERN = "C10,"
CMD_TESTPENWIDTHSQUARE = "C11,"
CMD_TESTPENWIDTHSCRIBBLE = "C12,"
CMD_PENDOWN = "C13,"
CMD_PENUP = "C14,"
CMD_DRAWSAWPIXEL = "C15,"
CMD_DRAWROUNDPIXEL = "C16,"
CMD_CHANGELENGTHDIRECT = "C17,"
CMD_TXIMAGEBLOCK = "C18,"
CMD_STARTROVE = "C19,"
CMD_STOPROVE = "C20,"
CMD_SET_ROVE_AREA = "C21,"
CMD_LOADMAGEFILE = "C23,"
CMD_CHANGEMACHINESIZE = "C24,"
CMD_CHANGEMACHINENAME = "C25,"
CMD_REQUESTMACHINESIZE = "C26,"
CMD_RESETMACHINE = "C27,"
CMD_DRAWDIRECTIONTEST = "C28,"
CMD_CHANGEMACHINEMMPERREV = "C29,"
CMD_CHANGEMACHINESTEPSPERREV = "C30,"
CMD_SETMOTORSPEED = "C31,"
CMD_SETMOTORACCEL = "C32,"
CMD_MACHINE_MODE_STORE_COMMANDS = "C33,"
CMD_MACHINE_MODE_EXEC_FROM_STORE = "C34,"
CMD_MACHINE_MODE_LIVE = "C35,"
CMD_RANDOM_DRAW = "C36,"
CMD_SETMACHINESTEPMULTIPLIER = "C37,"
CMD_START_TEXT = "C38,"
CMD_DRAW_SPRITE = "C39,"
CMD_CHANGELENGTH_RELATIVE = "C40,"
CMD_SWIRLING = "C41,"
CMD_DRAW_RANDOM_SPRITE = "C42,"
CMD_DRAW_NORWEGIAN = "C43,"
CMD_DRAW_NORWEGIAN_OUTLINE = "C44,"
CMD_SETPENLIFTRANGE = "C45,"
CMD_SELECT_ROVE_SOURCE_IMAGE = "C46"
CMD_RENDER_ROVE = "C47"

CMD_ACTIVATE_MACHINE_BUTTON = "C49"
CMD_DEACTIVATE_MACHINE_BUTTON = "C50"

PATH_SORT_NONE = 0
PATH_SORT_MOST_POINTS_FIRST = 1
PATH_SORT_GREATEST_AREA_FIRST = 2
PATH_SORT_CENTRE_FIRST = 3

PAGE_WIDTH_MM = 2274.0
MM_PER_PIXEL = 1.0
SAVE_PATH="/home/iplstaff/python_runner/IONINTERN/application.linux64"
#completeName = os.path.join(SAVE_PATH, name_of_file+".txt") 

STEPS_PER_REV = 200.0 #in steps
MM_PER_REV = 149.00 #in mm

STEPS_PER_MM = STEPS_PER_REV/MM_PER_REV
PAGE_WIDTH = PAGE_WIDTH_MM*STEPS_PER_MM
STEPS_PER_PIXEL = MM_PER_PIXEL*STEPS_PER_MM

MAX_SEGMENT_LENGTH = 2

commandQueue = []

def stepsToMM(num):
    a = num*STEPS_PER_MM
    return a

def getApos(xpos,ypos):
    a = np.sqrt(xpos**2+ypos**2)
    return a

def getBpos(xpos,ypos):
    a = np.sqrt((PAGE_WIDTH-xpos)**2+ypos**2)
    return a

def clearCommands(cQ):
    cQ = []
    return cQ

def addCommand(command):
    commandQueue.append(command)

def penUp():
    addCommand(CMD_PENUP+"180,END")

def penDown():
    addCommand(CMD_PENDOWN+"110,END")

def writeCommands(name_of_file):
    completeName = os.path.join(SAVE_PATH, name_of_file+".txt") 
    file1 = open(completeName, "w")
    for command in commandQueue:
        file1.write(command+'\n')
    file1.write(CMD_PENUP+"180,END"+'\n')
    file1.write(CMD_CHANGELENGTH+"3766,3766,END")
    file1.close()

def goXY(x,y):
    x=x+int(PAGE_WIDTH_MM/2)-229
    y=y-785
    a=CMD_CHANGELENGTHDIRECT+str(int(getApos(stepsToMM(x),stepsToMM(y))))+","+str(int(getBpos(stepsToMM(x),stepsToMM(y))))+","+str(MAX_SEGMENT_LENGTH)+",END"
    return a

def testDrawBox():
    x=1500
    y=-600
    addCommand(goXY(x,y))
    #addCommand(CMD_CHANGELENGTHDIRECT+str(int(getApos(stepsToMM(x),stepsToMM(y))))+","+str(int(getBpos(stepsToMM(x),stepsToMM(y))))+","+str(MAX_SEGMENT_LENGTH)+",END")
    x=1450
    y=-600
    addCommand(goXY(x,y))
    #addCommand(CMD_CHANGELENGTHDIRECT+str(int(getApos(stepsToMM(x),stepsToMM(y))))+","+str(int(getBpos(stepsToMM(x),stepsToMM(y))))+","+str(MAX_SEGMENT_LENGTH)+",END")
    x=1450
    y=-550
    addCommand(goXY(x,y))
    #addCommand(CMD_CHANGELENGTHDIRECT+str(int(getApos(stepsToMM(x),stepsToMM(y))))+","+str(int(getBpos(stepsToMM(x),stepsToMM(y))))+","+str(MAX_SEGMENT_LENGTH)+",END")
    x=1500
    y=-550
    addCommand(goXY(x,y))
    #addCommand(CMD_CHANGELENGTHDIRECT+str(int(getApos(stepsToMM(x),stepsToMM(y))))+","+str(int(getBpos(stepsToMM(x),stepsToMM(y))))+","+str(MAX_SEGMENT_LENGTH)+",END")



def drawPixels(filename):
    img = cv2.imread(filename)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #DONT HARDCODE THIS THIS IS FINE FOR FINE
    points = [[]] #Start and end points
    for z in range(1023):
        k = z-511
        lineOn=False
        o=0
        listy = []
        #print(np.diag(img,k)
        for pixel in np.diag(img,k):
            
            if(pixel==255):
                if not lineOn:
                    #print(o)    
                    #points = np.append(points,o)
                    listy.append([-1,o])
                    lineOn=True
            else:
                if lineOn:
                    #points = np.append(points,o)
                    listy.append([-2,o])
                    lineOn=False
            o+=1
        #print(listy)
        points.append(listy)
    #ok now lets parse these points better
    for line in points:
        print(line)
    
    penUp()
    addCommand(goXY(0,-600)) #GO to bottom left corner
    p=511
    for z in range(1023):
        if(z%5==1):
            pass
        elif(z%5==2):
            pass
        elif(z%5==3):
            pass
        elif(z%5==4):
            pass
        elif(z%5==0):
            k = z-511
            length = len(points[z])
            extendcmd = length%2==1
            if(k<=0):    
                penUp()
                addCommand(goXY(0,k-89))
                for c in range(length):
                    addCommand(goXY(0+points[z][c][1],k-89-points[z][c][1]))
                    if(points[z][c][0]==-1):
                        penDown()
                    else:
                        penUp()
                if extendcmd:
                    addCommand(goXY(0+z,k-89-z))
            elif(k>0):
                y = -89
                for c in range(length):
                    addCommand(goXY(k+points[z][c][1],-89-points[z][c][1]))
                    if(points[z][c][0]==-1):
                        penDown()
                    else:
                        penUp()
                if extendcmd:
                    addCommand(goXY(k+p,-89-p))
                p-=1
        
    



def testback():
    blank_image = np.zeros((512,512,3), np.uint8)
    register=0
    for i in range(512):
        for k in range(512):
            regr = register%9
            if(regr==0 or regr==1 or regr==2):
                blank_image[i,k] = [57,68,148]
            elif(regr==3 or regr==4 or regr==5):
                blank_image[i,k] = [28,185,129]
            elif(regr==6 or regr==7 or regr==8):
                blank_image[i,k] = [245,86,86]
            register+=1
    cv2.imwrite("abb.png",blank_image)


#testback()
#drawPixels("blob.png")
testDrawBox()
writeCommands("test")


 
