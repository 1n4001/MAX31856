# To run multiple Sensirion SDP810 flow sensors on one raspberry pi.
# IMPORTANT: Add the following 2 lines to /boot/config.txt to generate aditional i2c busses 3 and 4
# dtoverlay=i2c-gpio,bus=3,i2c_gpio_delay_us=1
# dtoverlay=i2c-gpio,bus=4,i2c_gpio_delay_us=1,i2c_gpio_sda=17,i2c_gpio_scl=27
# Dev by JJ Slabbert

import smbus
import time

bus3=smbus.SMBus(3) #Aditional 12c bus, configured in config.txt
bus4=smbus.SMBus(4) #Aditional 12c bus, configured in config.txt
address=0x13

bus3.write_i2c_block_data(address, 0x80, [0x08]) #Request prox reading
bus4.write_i2c_block_data(address, 0x80, [0x08]) #Request prox reading
time.sleep(0.1)

#Reading Sensor on i2c bus 3
reading3=bus3.read_i2c_block_data(address,0x80,1)
if (reading3 == 0x20):
    reading3h = bus3.read_i2c_block_data(address, 0x87, 1)
    reading3l = bus3.read_i2c_block_data(address, 0x88, 1)
    proximity_value3= (reading3h << 8) + reading3l

print("Proximity 3: {}".format(proximity_value3))


#Reading Sensor on i2c bus 4
reading4=bus4.read_i2c_block_data(address,0x80,1)
if (reading4 == 0x20):
    reading4h = bus4.read_i2c_block_data(address, 0x87, 1)
    reading4l = bus4.read_i2c_block_data(address, 0x88, 1)
    proximity_value4= (reading4h << 8) + reading4l

print("Proximity 3: {}".format(proximity_value3))
