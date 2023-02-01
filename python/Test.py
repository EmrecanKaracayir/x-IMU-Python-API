import serial

PORT = "com4"
BAUD_RATE = 9600

ser = serial.Serial(PORT, BAUD_RATE)



while True:
    b = ser.read(1)
    print(b)