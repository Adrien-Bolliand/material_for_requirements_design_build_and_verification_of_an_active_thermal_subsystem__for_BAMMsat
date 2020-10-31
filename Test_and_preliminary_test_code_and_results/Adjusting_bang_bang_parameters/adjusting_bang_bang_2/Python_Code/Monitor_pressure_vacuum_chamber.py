import pigpio
from datetime import datetime
from time import perf_counter
from time import sleep
import atexit
import csv
from Heater_AB import Heater
from ADS1248_AB import ADS1248
from Bang_bang_AB import Bang_bang
import os

## Initialize SPI
pi = pigpio.pi()
frq = 2*10**6
spi = pi.spi_open(0, frq, 1)
## ADS1248 declarations
ADS1248.setup(pi, spi, 26, frq) # (spi, drdy_pin)
adc1 = ADS1248(22, 820)  # (cs_pin, Rref = 820 ohm) Define ADC1 objects

## varible definition
position_low_pressure_sensor = 3
Voltage_sensor_in = 4.87 # The input voltage into the high_pressure sensor

def read_pressure_low(Volt, Vin_sensor):
    try:
        low_pressure = (Volt/(0.8*Vin_sensor)) - 0.125
        return low_pressure
    except:
        print('No value')
        return None

def exit_handler():
    data_log.close()
    ADS1248.pigpio.write(22, 0)
    pi.stop()

    additional_note = input ('Additional notes for the README file:_')
      # initialise README log file
    with open(name+'_README.csv','w',newline='') as readme_log:
        readme_writter = csv.writer(readme_log, 'excel') # generate object the README file writter
        readme_writter.writerow([timestamp]) # write the 1st row with test information
        readme_writter.writerow([note]) # write the 2nd row with test information

# get CPU temperature
def get_cpu_temp():
    res = os.popen("vcgencmd measure_temp").readline()
    t = float(res.replace("temp=","").replace("'C\n",""))
    return(t)

## Initialisation
atexit.register(exit_handler)
t = 0
timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
name_ext = input ('name extenssion WITHOUT SPACES:_')
name= "monitoring_vacuum_chamber_" + timestamp + '_' + name_ext
note = input('Note for the file: ')
note_file = 'Note at the beggining: ' + note

# initialise data log file
with open(name+'_data.csv', 'w', newline='') as data_log:
    #data_log = open(name+'_data.csv', 'w', newline='') # Create a new log file
    data_writter = csv.writer(data_log, 'excel') # generate object file writter
    data_writter.writerow(['Time_log_sec', 'voltage sensor (V)' ,'Pressure (bar)', 'RTD1_1 (*C)', 'ADS internal temp (*C)', 'CPU TEMP (*C)' ])

# Initilise ADS1248
adc1.wakeup()

### lOOP
while True:
    
    t_process = perf_counter() # To take into account how long the loop was

    RTD_1_1 = adc1.Read_RTD(1) # 2 reading are taken and averaged
    # RTD_1_2 = adc1.Read_RTD(2) # 2 reading are taken and averaged
    CPU_temp = get_cpu_temp()

    ADS_temp = adc1.Read_internal_temperature()

    low_pressure_volt = adc1.Read_5V_sensor(position_low_pressure_sensor)
    low_pressure = read_pressure_low(low_pressure_volt, Voltage_sensor_in)

    with open(name+'_data.csv', 'a', newline='') as data_log:
        data_writter = csv.writer(data_log, 'excel') # generate object file writter    
        data_writter.writerow([t, low_pressure_volt, low_pressure, RTD_1_1[1], ADS_temp, CPU_temp ])

    # Print
    print ('__________________')
    print(timestamp)
    print (t)
    print (' ')
    if RTD_1_1[0] or RTD_1_1[1] != None:
        print ('RTD1_1 '+'%.7f' % RTD_1_1[0] + ' ohm  ' + '%.2f' % RTD_1_1[1] + ' *C, on the alu panel') # print resistance with 7 decimal and temperature with 2 decimals
    else:
        print ('No value')
    #if RTD_1_2[0] or RTD_1_2[1] != None:
    #     print ('RTD1_2 '+'%.7f' % RTD_1_2[0] + ' ohm  ' + '%.2f' % RTD_1_2[1] + ' *C, on the pi SD') # print resistance with 7 decimal and temperature with 2 decimals
    # else:
    #     print ('No value')

    if ADS_temp != None:
        print (str (ADS_temp) + ' *C, internal temperature of the ADS') # print resistance with 7 decimal and temperature with 2 decimals
    else:
        print ('No value')
    
    if CPU_temp != None:
        print (str (CPU_temp) + ' *C, internal temperature of pi') # print resistance with 7 decimal and temperature with 2 decimals
    else:
        print ('No value')
    print (' ')
    print (str(low_pressure_volt)+ ' V, the voltage reading of the low_pressure sensor ')
    print (str(low_pressure) + ' bar')
    print (' ')

    # Update values
    sleep(1)
    t = t + perf_counter() - t_process
    # WARNING. DO NOT USE FOR FLIGHT CODE
    # END LOOP