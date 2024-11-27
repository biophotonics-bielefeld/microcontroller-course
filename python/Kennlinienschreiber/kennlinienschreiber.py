import sys
import time
import serial
import serial.tools.list_ports

"""
Looks for a serial port with an Ardunio Uno R4 connected
! Exists to system on errors

:return: The serial port that the Arduino is connected to

"""
def open_unoR4_port() -> serial.Serial:
    ports = serial.tools.list_ports.comports()  # gets a list of all serial ports in the system
    for port, desc, hwid in ports:              
        print ("#", port, desc, hwid)
        if 'UNO R4' in desc or 'VID:PID=2341:0069' in hwid:      # 'UNO R4' only works on Linux, search by HWID on Windows
            print('# Arduino found on port', port)
            ser = None
            try: 
                ser = serial.Serial(port, baudrate=115200)       # Try opening the port. Typical failure: Serial monitor still running                
            except serial.SerialException as e:
                print(f"Error opening serial port:\n{e}", file=sys.stderr)
                print("Check if Arduino serial monitor is still open!", file=sys.stderr)
                exit(-1)
            ser.reset_input_buffer()
            return ser
    sys.stderr.write("No Arduino found!")
    exit(-1)

"""
Send the 'set DAC' command
:param port:    The serial port of the Arduino
:param value:   The value to set the DAC to
"""
def set_dac(port: serial.Serial, value: int):
    port.write(b'S '+str(value).encode()+b'\n')
    ret = port.read_until()             # by default, this reads till '\n' is found, so one line
    if not ret.startswith(b'OK'):
        raise(ret)

"""
Send the 'read ADC' command
:param port:    The serial port of the Arduino
:param pin:     The pin to read
:return:        The value read by the ADC
"""
def read_adc(port: serial.Serial, pin: int) -> int:
    port.write(b'M '+str(pin).encode()+b'\n')    
    ret = port.read_until()             
    if not ret.startswith(b'OK'):
        raise(ret)
    else:
        val_str = ret[4:].decode()
        val_int = int(val_str)
        return val_int

"""
Small test: Set the DAC to values and read all pins
"""
def main():
    arduino_port = open_unoR4_port()
    
    for i in range(0,4096,256):
        set_dac(arduino_port, i)
        for pin in range(1,5):
            print( i, pin, read_adc(arduino_port, pin) )


    


if __name__ == "__main__":
    main()