from tkinter import *
import serial
from Camera_Adapter.AdapterBoard import MultiAdapter
from Camera_Adapter.cameraapp import CameraApp
from imutils.video import VideoStream
import time



USB_PORT = "/dev/ttyACM0"
global usb

USB_PORT2 = "/dev/ttyACM1"
global usb2



def connect():
    global usb
    global usb2
    try:
        usb = serial.Serial(USB_PORT,9600,timeout=2) # Steppers and LED strips
    except:
        print("ERROR could not open USB port 1, check port name and permissions.")
        print("Exiting....")
        exit(-1)

    try:
        usb2 = serial.Serial(USB_PORT2,9600,timeout=2) # Pumps, Linear Actuators, and Temp/Humidity sensor
    except:
        print("ERROR could not open USB port 2, check port name and permissions.")
        print("Exiting....")
        exit(-1)

#connect()

window = Tk()
window.geometry("1200x500")
stepperFrame = Frame(window)
stepperFrame.grid(row=0,column=0,padx=10)

ledFrame= Frame(window)
ledFrame.grid(row=0,column=1)

tempFrame = Frame(window)
tempFrame.grid(row=2,column=0)

humidFrame = Frame(window)
humidFrame.grid(row=2,column=1)

linearFrame = Frame(window)
linearFrame.grid(row=1,column=1)

pumpFrame = Frame(window)
pumpFrame.grid(row=1,column=0)

cameraFrame = Frame(window)
cameraFrame.grid(row=0,column=2)




def on_close():
    th.output.close()
    window.destroy()
window.protocol("WM_DELETE_WINDOW",on_close)






def writeToArduino(command):
    global usb
    try:
        usb.write(command)
    except NameError:
        print("usb not connected")
    print(command.decode())

def writeToArduino2(command):
    global usb2
    try:
        usb2.write(command)
    except NameError:
        print("usb not connected")
    print(command.decode())



def sendStepper1():
    writeToArduino(b'stepper1On\n')


def killStepper1():
    writeToArduino(b'stepper1Off\n')


def sendStepper2():
    writeToArduino(b'stepper2On\n')


def killStepper2():
    writeToArduino(b'stepper2Off\n')


def killAllSteppers():
    writeToArduino(b'allStepperOff\n')

def toggleWhite():
    writeToArduino(b'toggleWhite\n')

def toggleUVC():
    writeToArduino(b'toggleUVC\n')

def makeLEDButtons():
    whiteToggle = Button(ledFrame,text="Toggle White LED's",command=toggleWhite,width=20,height=5,bg="white")
    whiteToggle.grid(row=0,column=0,padx=1,pady=10)
    uvcToggle = Button(ledFrame,text="Toggle UVC LED's",command=toggleUVC,width=20,height=5,bg="grey")
    uvcToggle.grid(row=1,column=0,padx=1,pady=10)


def makeStepperButtons():
    on1 = Button(stepperFrame, text="Run Stepper 1",command=sendStepper1,width=10,height=5,bg="green")
    off1 = Button(stepperFrame, text="Kill Stepper 1",command=killStepper1,width=10,height=5,bg="red")
    on1.grid(row=0,column=0,padx=1,pady=10)
    off1.grid(row=0,column=1,padx=1,pady=10)


    on2 = Button(stepperFrame, text="Run Stepper 2",command=sendStepper2,width=10,height=5,bg="green")
    off2 = Button(stepperFrame, text="Kill Stepper 2",command=killStepper2,width=10,height=5,bg="red")
    on2.grid(row=1,column=0,padx=1,pady=10)
    off2.grid(row=1,column=1,padx=1,pady=10)


    allOff = Button(stepperFrame,text="Kill All Steppers",command=killAllSteppers,height=5,bg="darkred")
    allOff.grid(row=3,column=0,columnspan=2,padx=0,pady=5,sticky="nesw")



def makePumpButtons():
    pumps = []

    pumps.append(Checkbutton(pumpFrame,text="Pump 1",command = lambda: togglePump(1),width = 10))
    pumps.append(Checkbutton(pumpFrame,text="Pump 2",command = lambda: togglePump(2),width = 10))
    pumps.append(Checkbutton(pumpFrame,text="Pump 3",command = lambda: togglePump(3),width = 10))
    pumps.append(Checkbutton(pumpFrame,text="Pump 4",command = lambda: togglePump(4),width = 10))
    pumps.append(Checkbutton(pumpFrame,text="Pump 5",command = lambda: togglePump(5),width = 10))
    pumps.append(Checkbutton(pumpFrame,text="Pump 6",command = lambda: togglePump(6),width = 10))
    pumps.append(Checkbutton(pumpFrame,text="Pump 7",command = lambda: togglePump(7),width = 10))
    pumps.append(Checkbutton(pumpFrame,text="Pump 8",command = lambda: togglePump(8),width = 10))
    pumps.append(Checkbutton(pumpFrame,text="Pump 9",command = lambda: togglePump(9),width = 10))
    pumps.append(Checkbutton(pumpFrame,text="Pump 10",command = lambda: togglePump(10),width = 10))
    pumps.append(Checkbutton(pumpFrame,text="Pump 11",command = lambda: togglePump(11),width = 10))
    pumps.append(Checkbutton(pumpFrame,text="Pump 12",command = lambda: togglePump(12),width = 10))

    for ind,pump in enumerate(pumps[:6]):
        pump.grid(row=0,column=ind,padx=1,pady=5)
    for ind,pump in enumerate(pumps[6:]):
        pump.grid(row=1,column=ind,padx=1,pady=5)

def togglePump(ind):
    writeToArduino2(bytes('$pump{:02d}'.format(ind),'utf-8'))

def toggleAct1():
    writeToArduino2(b'act1')
def toggleAct2():
    writeToArduino2(b'act2')

def makeActuatorButtons():
    act1Toggle = Button(linearFrame,text="Toggle Linear Actuator 1",command=toggleAct1,width =20,height = 5)
    act2Toggle = Button(linearFrame,text="Toggle Linear Actuator 2",command=toggleAct2,width=20,height=5)
    act1Toggle.grid(row=0,column=0,padx=1,pady=5)
    act2Toggle.grid(row=0,column=1,padx=1,pady=5)

class liveReadout:
    def __init__(self,parent,text):

        self.label = Label(parent,text=text)
        self.label.pack()
        self.val = 100
        self.text= text
        if text == "Humidity":
            self.code = b'getHumid\n'
        elif text == "Temperature":
            self.code=b'getTemp\n'



        self.refreshValue()
        self.label.after(2000,self.refreshValue)


    def refreshValue(self):

        #writeToArduino2(self.code)
        #self.val = usb2.readLine()
        self.val = self.val+1



        self.label.configure(text="{}: {}".format(self.text,self.val))

        self.label.after(2000,self.refreshValue)

class tempHumid:
    def __init__(self,t,h):
        self.humid = 0
        self.h = h

        self.temp = 0
        self.t = t
        self.code = b'getTH\n'
        self.frame = Frame(window)

        self.output = open("output.txt","a")


        self.frame.after(5000,self.refreshValues)


    def refreshValues(self):

        writeToArduino2(self.code)

        data = usb2.read_until('\n')
        data=data.decode()
        print(data)
        self.humid,self.temp = data.split('!')
        self.humid = self.humid.strip()
        self.temp = self.temp.strip()

        self.h.configure(text="Humidity: {}%".format(self.humid))
        self.t.configure(text="Temperature: {} C".format(self.temp))
        self.output.write("{}% | {}C\n".format(self.humid,self.temp))

        self.frame.after(10000,self.refreshValues)



def makeTempHumid():

#tempOut = liveReadout(tempFrame,"Temperature")
    tempOut = Label(tempFrame,text="Temperature")
    tempOut.pack()
#humidOut = liveReadout(humidFrame,"Humidity" )
    humidOut = Label(humidFrame,text="Humidity")
    humidOut.pack()
    global th
    th = tempHumid(tempOut,humidOut)


def startCameras():
    camAdapter = MultiAdapter()
    Arducam_adapter_board.init(320,240)
    cameras = CameraApp("/",cameraFrame,camAdapter)








if __name__ == '__main__':
    #connect()
    makeStepperButtons()
    makeLEDButtons()
    makeTempHumid()
    makePumpButtons()
    makeActuatorButtons()
    startCameras()

    while True:
        window.update()
