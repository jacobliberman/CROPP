from tkinter import * 
import serial


USB_PORT = "/dev/ttyACM0"
global usb

USB_PORT2 = "/dev/ttyACM1"
global usb2



def connect():
    try:
        usb = serial.Serial(USB_PORT,9600,timeout=2)
    except:
        print("ERROR could not open USB port, check port name and permissions.")
        print("Exiting....")
        exit(-1)
        
    try:
        usb2 = serial.Serial(USB_PORT2,9600,timeout=2)
    except:
        print("ERROR could not open USB port, check port name and permissions.")
        print("Exiting....")
        exit(-1)
        
#connect()

window = Tk()
window.geometry("500x500")
stepperFrame = Frame(window)
stepperFrame.grid(row=0,column=0,padx=20)

ledFrame= Frame(window)
ledFrame.grid(row=0,column=1)

tempFrame = Frame(window)
tempFrame.grid(row=1,column=0)

humidFrame = Frame(window)
humidFrame.grid(row=1,column=1)









def writeToArduino(command):
    #usb.write(command)
    print(command.decode())


def sendStepper1():
    writeToArduino(b'stepper1On')
    
    
def killStepper1():
    writeToArduino(b'stepper1Off')


def sendStepper2():
    writeToArduino(b'stepper2On')
 
    
def killStepper2():
    writeToArduino(b'stepper2Off')

    
def killAllSteppers():
    writeToArduino(b'allStepperOff')
    
def toggleWhite():
    writeToArduino(b'whiteLEDOn')
    
def toggleUVC():
    writeToArduino(b'uvcLEDOn')

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


def makeTempHumid():
    tempOut = Label(tempFrame,text="Temperature: ")
    humidOut= Label(humidFrame,text="Humidity: ")
    tempOut.pack()
    humidOut.pack()

makeStepperButtons()
makeLEDButtons()
makeTempHumid()

while True:
    

    window.update()

