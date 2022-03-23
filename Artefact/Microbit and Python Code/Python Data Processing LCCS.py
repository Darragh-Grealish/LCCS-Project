

# Importing Libraries to be used
from firebase import firebase # Will allow us to connect append data to Firebase
import serial                 # Allows us to recieve data from the USB Port
import time
from datetime import datetime # Current date time in local system print(datetime.now())

# Creating connection from Python to Firebase, done by using the Database URL 
myData = firebase.FirebaseApplication("Firebase Credentials go here", None)
                                    #https://lccs-practice-default-rtdb.europe-west1.firebasedatabase.app/
# Serial Port setup  # Surface (not school computer) Put cmd into search bar and type chgport
ser = serial.Serial()
ser.baudrate = 115200  # Data Transfer Rate of MicroBit and Serial Port
ser.port = "COM3"      # USB Port Name on my Computer used to run this program
ser.open()             # Opening USB Port               

while True:   # Using While Loop to keep the Data Cleaning Procces Running until Stopped
    now = datetime.now()                    # Getting current time
    current_time = now.strftime("%H.%M.%S") # Getting the hours, minutes and seconds of current time
    #current_time = int(current_time)    
        
    data = str(ser.readline())     # 'data' now contains the current data package recieved
    data = data.replace("-","")    # Cleaning the data
    data = data.replace("\\n","")  # By removing unwanted characters and symbols
    data = data.replace("\\r","")  # Removing a     -   \n   \r   '   b
    data = data.replace("'","")
    data = data.replace("b","")
    #print(data)
    
    flame = data[0]      # Flame Status is at index[0]
    flame = int(flame)   # Flame is converted to integer either 0 or 1
    magnet = data[1:3]   # Magnet strength is at index[1 and 2]
    magnet = int(magnet) # Converted to an integer
    temp = data[3:5]     # Temperature value is at index[3 and 4]
    temp = int(temp)     # Converted to an integer
    dust = data[5:8]     # Dust value is at index [5, 6 and 7]
    dust = int(dust)     # Converted to an integer

    # IF statement for door being opened or closed depending on magnet strenght detected
    if magnet < 65:      # If magnet strength is less than 65 the door is opened
        magnetB = 0
    else:                # Else the door is closed 
        magnetB = 1    
        
    postRecord = { # Creating a record to send to Firebase containing the values we have collected and sorted from MicroBit
        'currentTime'      :  current_time,
        'flameDetection'   :  flame,  
        'doorStatus'       :  magnetB, # Sending apropriate values to each node 
        'roomTemperature'  :  temp,
        'dustLevel'        :  dust
        }
    print(postRecord) # Printing the record to see we have correctly matched up the values 
    
    myData.post('/monitorDevice/', postRecord) # Sending the data to Firebase
    # This data will be stored under 'monitorDevice' in Firebase
    
    time.sleep(3) # Allowing 3 seconds between each data collection
    
ser.close() # Closing the Serial Port after the while loop finishes but before the code finishes running 
