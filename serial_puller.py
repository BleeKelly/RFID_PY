USB_PORT_ONE = "/dev/tty" #Serial Port for Arduino 1-Need to run 'ls /dev/tty* to find connected arduinos
USB_PORT_TWO = "/dev/tty" #Serial Port for Arduino 2-Need to run 'ls /dev/tty* to find connected arduinos
BAUD_RATE = 9600

import pandas as pd #Imports to use dataframes
import serial as ser#Serial library
import csv

if __name__ == '__main__':
    rfid_data ={'UID':[],
                'Location':[]}#Creates dictionary to use to create dataframe
    rfid_df=pd.DataFrame(rfid_data)#Creates dataframe from aforemention dictionary
    ser_one = ser.Serial(USB_PORT_ONE ,BAUD_RATE, timeout=1)#Creates ser_one object for first arduino
    ser_one.reset_input_buffer()#Resets input buffer to prevent lingering signals
    ser_two = ser.Serial(USB_PORT_TWO,BAUD_RATE,timeout=1)#creates ser_two object for second arduino
    ser_two.reset_input_buffer()#Resets input buffer to prevent lingering signals
    while True:#Infinite loop
        if ser.in_waiting > 0:#If message from first arduino is present, execute this block
            line = ser_one.readline().decode('utf-8').rstrip()#Reads data from serial port, decodes it from UTF-8 and strips the whitespace on the right
            for row in csv.reader(line):#Reads csv formatted stri g
                arduino_data=row#Stores data
                df.loc[len(df)] = arduino_data#Appends to end of dataframe
                html=df.to_HTML()#Creates Html Code
                text_file = open("index.html", "w")#Opens html file to write to
                text_file.write(html)#Writes updated dataframe
                text_file.close()#Closes HTML.
                #The above section should probably not be in the for loop for best performance but I didn't want to worry about scope at 1 in the morning...Will fix if needed


        if ser_two.in_waiting > 0:
            line = ser_two.readline().decode('utf-8').rstrip()
            for row in line:
                arduino_data=row
                df.loc[len(df)] = arduino_data
                html=df.to_HTML()
                text_file = open("index.html", "w")
                text_file.write(html)
