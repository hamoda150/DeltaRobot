import serial
import serial.tools.list_ports

def serial_ports():
    # produce a list of all serial ports. The list contains a tuple with the port number, 
    # description and hardware address
    #
    ports = list(serial.tools.list_ports.comports())  

    # return the port if 'USB' is in the description 
    for port_no, description, address in ports:
        if 'USB' in description:
            return port_no


port = serial_ports()  
print (port)          
ser = serial.Serial()
ser.port = str(port)
ser.baudrate = 9600
ser.open()
ser.write(b'800') # send number 1
ser.close()
