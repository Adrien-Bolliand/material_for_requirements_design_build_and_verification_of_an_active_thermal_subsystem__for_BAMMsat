import pigpio
from datetime import datetime
from time import perf_counter
from time import sleep
import atexit
import csv
from Heater_AB import Heater
from ADS1248_AB import ADS1248
from Bang_bang_AB import Bang_bang


def exit_handler():
    #data_log.close()
    ADS1248.pigpio.write(22, 0)
    ADS1248.pigpio.write(27, 0)
    ADS1248.pigpio.write(17, 0)
    bb_disc.pigpio.set_PWM_dutycycle(19, 0)
    bb_fluid.pigpio.set_PWM_dutycycle(13, 0)
    pi.stop()

    additional_note = input ('Additional notes for the README file:_')
      # initialise README log file
    
    with open (name+'_README.csv','w',newline='') as readme_log:
        readme_writter = csv.writer(readme_log, 'excel') # generate object the README file writer
        readme_writter.writerow([timestamp, '  ' + note]) # write the 1st row with test information
        readme_writter.writerow(['IMPORTANT. Values of the data file are valide from their "time log" of the same line until the "time log" of the next line'])
        readme_writter.writerow(['Voltage power supply: ' + str(power_voltage_in) + ' V']) # write the 2nd row with power supply information
        readme_writter.writerow(['Note from end of experiment: ' + additional_note]) # write the 1st row with test information
        readme_writter.writerow(['Values on the bottom where logged at the end of the experiment . ' + additional_note]) # write the 1st row with test information
        readme_writter.writerow(['bang bang name ','resistor (ohm) ' ,'extrem low threshold final (°C) ', 'low threshold final (°C)', 'high threshold final (°C)', 'extrem high threshold final (°C)', 'PWM extrem low final', 'PWM low final', 'PWM high final', 'PWM extrem hight final'])
        readme_writter.writerow([bb_disc.name, bb_disc.heater.resistor,  bb_disc.thres_ex_low,  bb_disc.thres_low,  bb_disc.thres_high,  bb_disc.thres_ex_high,  bb_disc.PWM_ex_low,  bb_disc.PWM_low,  bb_disc.PWM_high,  bb_disc.PWM_ex_high])
        readme_writter.writerow([bb_fluid.name, bb_fluid.heater.resistor, bb_fluid.thres_ex_low, bb_fluid.thres_low, bb_fluid.thres_high, bb_fluid.thres_ex_high, bb_fluid.PWM_ex_low, bb_fluid.PWM_low, bb_fluid.PWM_high, bb_fluid.PWM_ex_high])


def read_pressure_high(Volt, Vin_sensor):
    try:
        high_pressure = (Volt + Vin_sensor * 0.00842)/(Vin_sensor*0.002421) # values from sensor datasheet: https://docs.rs-online.com/54de/0900766b814a74e2.pdf
        return high_pressure
    except:
        print ('No value')
        return None

def read_pressure_low(Volt, Vin_sensor):
    try:
        low_pressure = (Volt/(0.8*Vin_sensor)) - 0.125
        return low_pressure
    except:
        print('No value')
        return None

## varible definition
position_high_pressure_sensor = 4
position_volt_heater = 3
Voltage_sensor_in = 4.97 # The input voltage into the high_pressure sensor
power_voltage_in = 25   # The input voltage into the heaters

## Initialize SPI
pi = pigpio.pi()
frq = 2*10**6
spi = pi.spi_open(0, frq, 1)
## ADS1248 declarations
ADS1248.setup(pi, spi, 26, frq) # (spi, drdy_pin)
adc1 = ADS1248(22, 820)  # (cs_pin, Rref = 820 ohm) Define ADC1 objects
adc2 = ADS1248(27, 820)  # (cs_pin, Rref = 820 ohm) Define ADC2 objects
adc3 = ADS1248(17, 820)  # (cs_pin, Rref = 820 ohm) Define ADC3 objects

## Define the heaters
heater_disc = Heater('disc heater', 70, power_voltage_in)
heater_fluid = Heater('fluid heater', 103, power_voltage_in)

## Define Bang Bang
bb_disc = Bang_bang(pi,'bb_disc', heater_disc, 19, 0, 10, 80, 100, 18.5, 19, 19.5, 20, 320) # Declaration of the bang bang regulator regulating the custom heater below the disc with the default parameters
bb_fluid = Bang_bang(pi,'bb_fluid', heater_fluid, 13, 0, 15, 70, 100, 10, 12, 13, 14, 320) # Declaration of the bang bang regulator regulating the film heater on the fluidic bag support
         # Bang_bang(name (str), PWM_GPIO, heater,PWM_value_extrem_low = 0, PWM_value_low = 20, PWM__value_high = 90, PWM_value_extrem_high = 100, Thres_extrem_low = 18.5, Thres_value_low = 19, Thres_value_high = 21, Thres_extrem_high = 21.5) Try regulation in ambient at between 18 and 22 *C 


## Initialisation
atexit.register(exit_handler)
t = 0
timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
name_ext = input ('name extension WITHOUT SPACES:_')
name= "test_bang_bang_adjust_" + timestamp + '_' + name_ext
note = input('Note for the file: ')
note_file = 'Note at the begging: ' + note

  # initialise data log file
with open (name+'_data.csv', 'w', newline='') as data_log:
    data_writter = csv.writer(data_log, 'excel') # generate object file writter
    data_writter.writerow(['Time_log_sec',
                        'RTD_1_1_Celsius','RTD_1_2_Celsius','RTD_1_3_Celsius', 'RTD_1_4_Celsius',
                        'RTD_2_1_Celsius','RTD_2_2_Celsius','RTD_2_3_Celsius', 'RTD_2_4_Celsius',
                        'RTD_3_1_Celsius','RTD_3_3_Celsius','internal temp ADC1', 'internal temp ADC2', 'internal temp ADC3',
                        'Pressure_kPa',
                        'heater_voltage (V)','PWM_disc', 'PWM_fluid', 'Energy_disc_Watt','Energy_fluid_Watt', 'Heaters_Energy_Watt',
                        'disc_thersh_ex_low (*C)', 'disc_thresh_low (*C)', 'disc_thresh high(*C)', 'disc_thresh_ex_high (*C)',
                        'disc_pwm_value_ex_low', 'disc_pwm_value_low', 'disc_pwm_value_high', 'disc_pwm_value_ex_hight', 
                        'fluid_thersh_ex_low (*C)', 'fluid_thresh_low (*C)', 'fluid_thresh high(*C)', 'fluid_thresh_ex_high (*C)',
                        'fluid_pwm_value_ex_low', 'fluid_pwm_value_low', 'fluid_pwm_value_high', 'fluid_pwm_value_ex_hight', 'volt_heater']) # 3rd line is the data header

  # Initilise ADS1248
adc1.wakeup()
adc2.wakeup()
adc3.wakeup()
#adc1.spi.write(bytes([0xFF])) #send a NOP command (seemed to have debugged the ADS once... not sure why, but it worked)
#adc2.spi.write(bytes([0xFF])) #send a NOP command (seemed to have debugged the ADS once... not sure why, but it worked)
#adc3.spi.write(bytes([0xFF])) #send a NOP command (seemed to have debugged the ADS once... not sure why, but it worked)


### lOOP
while True:
    
    t_process = perf_counter() # To take into account how long the loop was
    
    RTD_1_1 = adc1.Read_RTD(1) # 2 reading are taken and averaged
    RTD_1_2 = adc1.Read_RTD(2) # 2 reading are taken and averaged
    RTD_1_3 = adc1.Read_RTD(3) # 2 reading are taken and averaged
    bb_fluid.update(RTD_1_3[1])  # update the status of the bang bang regulating the fluid heater
    RTD_1_4 = adc1.Read_RTD(4) # 2 reading are taken and averaged

    RTD_2_1 = adc2.Read_RTD(1) # 2 reading are taken and averaged
    bb_disc.update(RTD_2_1[1])  # update the status of the bang bang regulating the custom heater below the disc
    RTD_2_2 = adc2.Read_RTD(2) # 2 reading are taken and averaged
    RTD_2_3 = adc2.Read_RTD(3) # 2 reading are taken and averaged
    RTD_2_4 = adc2.Read_RTD(4) # 2 reading are taken and averaged

    RTD_3_1 = adc3.Read_RTD(1) # 2 reading are taken and averaged
    RTD_3_3 = adc3.Read_RTD(3) # 2 reading are taken and averaged
    ADC_1_temp = adc1.Read_internal_temperature()
    ADC_2_temp = adc2.Read_internal_temperature()
    ADC_3_temp = adc3.Read_internal_temperature()

    high_pressure_volt = adc3.Read_5V_sensor(position_high_pressure_sensor)
    high_pressure = read_pressure_high(high_pressure_volt, Voltage_sensor_in)
    volt_heater = adc3.Read_5V_sensor(position_volt_heater)

    
    # Store data
    with open (name+'_data.csv', 'a', newline='') as data_log:
        data_writter = csv.writer(data_log, 'excel') # generate object file writter
        data_writter.writerow([t,
                            RTD_1_1[1],RTD_1_2[1],RTD_1_3[1],RTD_1_4[1],
                            RTD_2_1[1],RTD_2_2[1],RTD_2_3[1],RTD_2_4[1],
                            RTD_3_1[1], RTD_3_3[1], ADC_1_temp, ADC_2_temp, ADC_3_temp,
                            high_pressure,
                            power_voltage_in,bb_disc.PWM_value,bb_fluid.PWM_value, bb_disc.energy, bb_fluid.energy, bb_disc.energy + bb_fluid.energy,
                            bb_disc.thres_ex_low, bb_disc.thres_low, bb_disc.thres_high, bb_disc.thres_ex_high,
                            bb_disc.PWM_ex_low, bb_disc.PWM_low, bb_disc.PWM_high, bb_disc.PWM_ex_high,
                            bb_fluid.thres_ex_low, bb_fluid.thres_low, bb_fluid.thres_high, bb_fluid.thres_ex_high,
                            bb_fluid.PWM_ex_low, bb_fluid.PWM_low, bb_fluid.PWM_high, bb_fluid.PWM_ex_high, volt_heater])
    # Print
    print ('__________________')
    print(timestamp)
    print (t)
    print (' ')
    print (str(high_pressure_volt)+ ' V, the voltage reading of the high_pressure sensor ')
    print (str(high_pressure) + ' kPa')
    print (' ')
    print (str(volt_heater)+ ' V, the voltage reading of LED PCB at the heater ')
    print (' ')



    if RTD_2_1[0] or RTD_2_1[1] != None:
        print ('RTD2_1 '+'%.7f' % RTD_2_1[0] + ' ohm  ' + '%.2f' % RTD_2_1[1] + ' *C'+ ' surface disc ext') # print resistance with 7 decimal and temperature with 2 decimals
    else:
        print ('No value')
    if RTD_2_2[0] or RTD_2_2[1] != None:
        print ('RTD2_2 '+'%.7f' % RTD_2_2[0] + ' ohm  ' + '%.2f' % RTD_2_2[1] + ' *C'+ ' surface disc int') # print resistance with 7 decimal and temperature with 2 decimals
    else:
        print ('No value')
    print('')
    if RTD_2_3[0] or RTD_2_3[1] != None:
        print ('RTD2_3 '+'%.7f' % RTD_2_3[0] + ' ohm  ' + '%.2f' % RTD_2_3[1] + ' *C'+ 'IN disc') # print resistance with 7 decimal and temperature with 2 decimals
    else:
        print ('No value')
    if RTD_2_4[0] or RTD_2_4[1] != None:
        print ('RTD2_4 '+'%.7f' % RTD_2_4[0] + ' ohm  ' + '%.2f' % RTD_2_4[1] + ' *C'+ ' IN disc') # print resistance with 7 decimal and temperature with 2 decimals
    else:
        print ('No value')
    if RTD_1_1[0] or RTD_1_1[1] != None:
        print ('RTD1_1 '+'%.7f' % RTD_1_1[0] + ' ohm  ' + '%.2f' % RTD_1_1[1] + ' *C'+ ' IN disc') # print resistance with 7 decimal and temperature with 2 decimals
    else:
        print ('No value')
    if RTD_1_2[0] or RTD_1_2[1] != None:
        print ('RTD1_2 '+'%.7f' % RTD_1_2[0] + ' ohm  ' + '%.2f' % RTD_1_2[1] + ' *C'+ ' IN disc') # print resistance with 7 decimal and temperature with 2 decimals
    else:
        print ('No value')
    print ('')

    print('Threshold disc: ' + str (bb_disc.thres_ex_low) + ' '+ str (bb_disc.thres_low) + ' '+ str (bb_disc.thres_high) + ' ' + str (bb_disc.thres_ex_high))
    print('PWM values:     ' + str (bb_disc.PWM_ex_low) + ' ' + str (bb_disc.PWM_low) + ' ' + str (bb_disc.PWM_high) + ' ' + str (bb_disc.PWM_ex_high)+'\n')

    if RTD_1_3[0] or RTD_1_3[1] != None:
        print ('RTD1_3 '+'%.7f' % RTD_1_3[0] + ' ohm  ' + '%.2f' % RTD_1_3[1] + ' *C'+' on the fluidic bag ') # print resistance with 7 decimal and temperature with 2 decimals
    else:
        print ('No value')
    if RTD_1_4[0] or RTD_1_4[1] != None:
        print ('RTD1_4 '+'%.7f' % RTD_1_4[0] + ' ohm  ' + '%.2f' % RTD_1_4[1] + ' *C'+ ' on the rod next to fludic pipes ') # print resistance with 7 decimal and temperature with 2 decimals
    else:
        print ('No value')
    print (' ')

    
    print('Threshold fluid: ' + str (bb_fluid.thres_ex_low) + ' '+ str (bb_fluid.thres_low) + ' '+ str (bb_fluid.thres_high) + ' ' + str (bb_fluid.thres_ex_high))
    print('PWM values:     ' + str (bb_fluid.PWM_ex_low) + ' ' + str (bb_fluid.PWM_low) + ' ' + str (bb_fluid.PWM_high) + ' ' + str (bb_fluid.PWM_ex_high)+'\n')
    
    print(' ')
    if RTD_3_1[0] or RTD_3_1[1] != None:
        print ('RTD3_1 '+'%.7f' % RTD_3_1[0] + ' ohm  ' + '%.2f' % RTD_3_1[1] + ' *C'+ ' on the camera plate') # print resistance with 7 decimal and temperature with 2 decimals
    else:
        print ('No value')
    if RTD_3_3[0] or RTD_3_3[1] != None:
        print ('RTD3_3 '+'%.7f' % RTD_3_3[0] + ' ohm  ' + '%.2f' % RTD_3_3[1] + ' *C'+ '  on the LED PCBs') # print resistance with 7 decimal and temperature with 2 decimals
    else:
        print ('No value')
    if ADC_1_temp != None:
        print ('ADCt_1 '+'%.2f' % ADC_1_temp  +' *C'+ ' internal temp')
    else:
        print ('No value')
    if ADC_2_temp != None:
        print ('ADCt_2 '+'%.2f' % ADC_2_temp  +' *C'+ ' internal temp')
    else:
        print ('No value')
    if ADC_3_temp != None:
        print ('ADCt_3 '+'%.2f' % ADC_3_temp  +' *C'+ ' internal temp')
    else:
        print ('No value')

    
    
    print ('disc PWM value: '+str(bb_disc.PWM_value))
    print ('fluid PWM value: '+str(bb_fluid.PWM_value))
    print (' ')

    # Update values
    sleep(1)
    t = t + perf_counter() - t_process
    # WARNING. DO NOT USE FOR FLIGHT CODE
    # END LOOP 