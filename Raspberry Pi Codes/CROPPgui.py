from tkinter import * 
import serial


USB_PORT = "/dev/ttyACM0"
global usb

USB_PORT2 = "/dev/ttyACM1"
global usb2



def connect():
    try:
        usb = serial.Serial(USB_PORT,9600,timeout=2) # Steppers and LED strips
    except:
        print("ERROR could not open USB port, check port name and permissions.")
        print("Exiting....")
        exit(-1)
        
    try:
        usb2 = serial.Serial(USB_PORT2,9600,timeout=2) # Pumps, Linear Actuators, and Temp/Humidity sensor
    except:
        print("ERROR could not open USB port, check port name and permissions.")
        print("Exiting....")
        exit(-1)
        
#connect()

window = Tk()
window.geometry("800x500")
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








def writeToArduino(command):
    #usb.write(command)
    print(command.decode())

def writeToArduino2(command):
    #usb2.write(command)
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
    
    pumps.append(Button(pumpFrame,text="Pump 1",command = lambda: writeToArduino2(b"$pump01"),width = 10))
    pumps.append(Button(pumpFrame,text="Pump 2",command = lambda: writeToArduino2(b"$pump02"),width = 10))
    pumps.append(Button(pumpFrame,text="Pump 3",command = lambda: writeToArduino2(b"$pump03"),width = 10))
    pumps.append(Button(pumpFrame,text="Pump 4",command = lambda: writeToArduino2(b"$pump04"),width = 10))
    pumps.append(Button(pumpFrame,text="Pump 5",command = lambda: writeToArduino2(b"$pump05"),width = 10))
    pumps.append(Button(pumpFrame,text="Pump 6",command = lambda: writeToArduino2(b"$pump06"),width = 10))
    pumps.append(Button(pumpFrame,text="Pump 7",command = lambda: writeToArduino2(b"$pump07"),width = 10))
    pumps.append(Button(pumpFrame,text="Pump 8",command = lambda: writeToArduino2(b"$pump08"),width = 10))
    pumps.append(Button(pumpFrame,text="Pump 9",command = lambda: writeToArduino2(b"$pump09"),width = 10))
    pumps.append(Button(pumpFrame,text="Pump 10",command = lambda: writeToArduino2(b"$pump10"),width = 10))
    pumps.append(Button(pumpFrame,text="Pump 11",command = lambda: writeToArduino2(b"$pump11"),width = 10))
    pumps.append(Button(pumpFrame,text="Pump 12",command = lambda: writeToArduino2(b"$pump12"),width = 10))
    
    for ind,pump in enumerate(pumps[:6]):
        pump.grid(row=0,column=ind,padx=1,pady=5)
    for ind,pump in enumerate(pumps[6:]):
        pump.grid(row=1,column=ind,padx=1,pady=5)
    
    
    
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
        
        self.frame.after(5000,self.refreshValues)
        
        
    def refreshValues(self):
        writeToArduino2(self.code)
        #self.humid = usb2.read_until('!')
        #self.temp = usb2.read_until('!')
        self.humid = self.humid + 1
        self.temp = self.temp + 1
        
        self.h.configure(text="Humidity: {}".format(self.humid))
        self.t.configure(text="Temperature: {}".format(self.temp))
        
        
        self.frame.after(5000,self.refreshValues)
        
    

def makeTempHumid():

#tempOut = liveReadout(tempFrame,"Temperature")
    tempOut = Label(tempFrame,text="Temperature")
    tempOut.pack()
#humidOut = liveReadout(humidFrame,"Humidity" )
    humidOut = Label(humidFrame,text="Humidity")
    humidOut.pack()
    th = tempHumid(tempOut,humidOut)

makeStepperButtons()
makeLEDButtons()
makeTempHumid()
makePumpButtons()
makeActuatorButtons()

while True:
    
    

    
    window.update()

