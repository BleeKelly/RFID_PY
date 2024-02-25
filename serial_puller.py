USB_PORT_ONE = "/dev/ttyACM0" #Serial Port for Arduino 1-Need to run 'ls /dev/tty* to find connected arduinos
USB_PORT_TWO = "/dev/ttyACM1" #Serial Port for Arduino 2-Need to run 'ls /dev/tty* to find connected arduinos
BAUD_RATE = 115200

import pandas as pd #Imports to use dataframes
import serial as ser #Serial library
import csv

if __name__ == '__main__':
    rfid_data ={'UID':[],
                'Location':[]} #Creates dictionary to use to create dataframe
    rfid_df=pd.DataFrame(rfid_data) #Creates dataframe from aforemention dictionary
    ser_one = ser.Serial(USB_PORT_ONE ,BAUD_RATE, timeout=1) #Creates ser_one object for first arduino
    ser_one.reset_input_buffer() #Resets input buffer to prevent lingering signals
    ser_two = ser.Serial(USB_PORT_TWO,BAUD_RATE,timeout=1) #creates ser_two object for second arduino
    ser_two.reset_input_buffer() #Resets input buffer to prevent lingering signals
    counter = 0
    while True: #Infinite loop
        if ser_one.in_waiting > 0: #If message from first arduino is present, execute this block
            if counter<5:
                counter=counter+1
                print(counter)
                line = ser_one.readline().decode('UTF-8').rstrip() #Reads data from serial port, decodes it from UTF-8 and strips the whitespace on the right
                print(line)
                continue
            line = ser_one.readline().decode('UTF-8').rstrip() #Reads data from serial port, decodes it from UTF-8 and strips the whitespace on the right
            for row in csv.reader([line]): #Reads csv formatted string
                #print(row)
                arduino_data=row #Stores data
                rfid_df.iloc[len(rfid_df)] = arduino_data #Appends to end of dataframe
                rfid_df.drop_duplicates(subset=['Location'], inplace=True)# Removes duplicates fo data from the dataframe based on location....Currently removes latest one but needs to remove first
                html=rfid_df.to_html() #Creates Html Code
                print(rfid_df)#Prints updated dataframe to console
                text_file = open("/home/pi/py_rfid/index.html", "w") #Opens html file to write to
                text_file.write(html)#Writes generated HTML code to index.html on Pi...Will likely point Apache webserver at it before Friday.
                text_file.close() #Closes HTML.
                #The above section should probably not be in the for loop for best performance but I didn't want to worry about scope at 1 in the morning...Will fix if needed


        if ser_two.in_waiting > 0:
            line = ser_two.readline().rstrip()
            print(line)
 #           for row in line:
 #               arduino_data=row #Stores data
                rfid_df.iloc[len(rfid_df)] = arduino_data #Appends to end of dataframe
                rfid_df.drop_duplicates(subset=['Location'], inplace=True)
                html=rfid_df.to_html() #Creates Html Code
                print(rfid_df)
                text_file = open("/home/pi/py_rfid/index.html", "w") #Opens html file to write to
                text_file.write(html)
                text_file.close() #Closes HTML.
