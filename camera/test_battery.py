import smbus

def fibonacci(n): 
    a = 0
    b = 1
    if n < 0: 
        print("Incorrect input") 
    elif n == 0: 
        return a 
    elif n == 1: 
        return b 
    else: 
        for i in range(2,n): 
            c = a + b 
            a = b 
            b = c 
        print(getPiVoltage)
        return b 

def getPiVoltage():
    bus = smbus.SMBus(1)
    WITTYPI_ADDRESS = 0x69
    I2C_VOLTAGE_OUT_I = 3
    I2C_VOLTAGE_OUT_D = 4

    i = bus.read_byte_data(WITTYPI_ADDRESS,I2C_VOLTAGE_OUT_I)
    d = bus.read_byte_data(WITTYPI_ADDRESS,I2C_VOLTAGE_OUT_D)
    piVoltage = i + (d/100)

    return piVoltage


print(fibonacci(10000)) 