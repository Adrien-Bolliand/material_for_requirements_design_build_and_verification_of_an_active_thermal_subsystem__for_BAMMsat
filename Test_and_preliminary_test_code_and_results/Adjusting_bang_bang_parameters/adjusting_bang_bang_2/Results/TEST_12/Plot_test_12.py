import numpy as np
import matplotlib.pyplot as plt
import matplotlib.lines as lines
import os

file_path = os.path.dirname(os.path.abspath(__file__))

# Parameters
upper_requirement = 22 # For the upper line of the temperature plot
low_requirement = 18 #for the low line of the temperature plot
name_image_output = 'Test_plot_12'
## Paramet to remove data from the begging to sync data from PRi in 1 U and in 2U
### IMPORTANT remove data at begging and set the new 1st line a t = 0sec
            # Then cut the end of the data set AFTER the timming have been reset.
# Removing completely the data at the beginning and the end is important so that
# on the power computed and shown match the data displayed
# IN SECOND, cut the begging of the data set and set the new 1st line a t = 0sec.
diff_data_mon = 10.8 # the timing of the monitoring data is 10.8 sec ahead of the pi in the pressure vessel
t_offset_data = 0         # IN SECOND look for info in the readme file
t_offset_monitor_data = t_offset_data + diff_data_mon  # IN SECOND look for info in the readme file 
# IN SECOND to cut the end of the data set. time to consider after the data have been offset and time reset at zero.
t_cut_data = None            # IN SECOND look for info in the readme file
t_cut_mon = None             # IN SECOND look for info in the readme file
#visulalisation limit
visual_x_lim_low = 0
visual_x_lim_high = None

## Retrieve data
data_path = os.path.join(file_path, 'test_bang_bang_adjust_2020-09-18_03-27-49_TEST_12_data.csv')
#readme_path = os.path.join(file_path,'test_comparing_inside_outside_disc_chamber_2020-09-10_22-21-06_data_for_test_plor_README.csv')
monitoring_data = os.path.join(file_path, 'monitoring_vacuum_chamber_2020-09-16_12-18-37_TEST_12_data.csv')
t, R1_1, R1_2, R1_3, R1_4, R2_1, R2_2, R2_3, R2_4, R3_1, R3_3,ADC_1_temp, ADC_2_temp, ADC_3_temp, pressure, power_voltage, PWM_disc, PWM_fluid,pw_disc, pw_fluid, pw_total, ex_low_temp_disc, low_temp_disc, high_temp_disc, ex_high_temp_disc, ex_low_PWM_disc, low_PWM_disc, high_PWM_disc, ex_high_PWM_disc, ex_low_temp_fluid, low_temp_fluid, high_temp_fluid, ex_high_temp_fluid, ex_low_PWM_fluid, low_PWM_fluid, high_PWM_fluid, ex_high_PWM_fluid, volt_heater = np.genfromtxt(data_path,delimiter=',',skip_header=1,unpack=True)
tm, volt_sensor, pressure_chamber, R1_1_out, temp_ADS, CPU_temp = np.genfromtxt(monitoring_data,delimiter=',',skip_header=1,unpack=True)
# name, resistor, ex_low_temp, low_temp, high_temp, ex_high_temp, ex_low_PWM, low_PWM, high_PWM, ex_high_PWM = np.genfromtxt(readme_path,delimiter=',',skip_header=5,unpack=True)

### Data process
## REMOVE DATA BEFORE and AFTER THE TIME OFFSET
if t_offset_data > 0:
    i=0
    while t[i] < t_offset_data:
        i=i+1
    index_offset_data = list(range(0,i))
    #print('____________\n'+str(i))
    #remove data until offset index
    t = np.delete(t,index_offset_data)
    R1_1=np.delete(R1_1,index_offset_data);  R1_2=np.delete(R1_2,index_offset_data); R1_3=np.delete(R1_3,index_offset_data); R1_4=np.delete(R1_4,index_offset_data)
    R2_1=np.delete(R2_1,index_offset_data); R2_2=np.delete(R2_2,index_offset_data); R2_3=np.delete(R2_3,index_offset_data); R2_4=np.delete(R2_4,index_offset_data)
    R3_1=np.delete(R3_1,index_offset_data); R3_3=np.delete(R3_3,index_offset_data); ADC_1_temp=np.delete(ADC_1_temp,index_offset_data); ADC_2_temp=np.delete(ADC_2_temp,index_offset_data); ADC_3_temp=np.delete(ADC_3_temp,index_offset_data)
    pressure=np.delete(pressure,index_offset_data)
    power_voltage=np.delete(power_voltage,index_offset_data); PWM_disc=np.delete(PWM_disc,index_offset_data); PWM_fluid=np.delete(PWM_fluid,index_offset_data); pw_disc=np.delete(pw_disc,index_offset_data); pw_fluid=np.delete(pw_fluid,index_offset_data); pw_total=np.delete(pw_total,index_offset_data)
    ex_low_temp_disc=np.delete(ex_low_temp_disc,index_offset_data); low_temp_disc=np.delete(low_temp_disc,index_offset_data); high_temp_disc=np.delete(high_temp_disc,index_offset_data); ex_high_temp_disc=np.delete(ex_high_temp_disc,index_offset_data); ex_low_PWM_disc=np.delete(ex_low_PWM_disc,index_offset_data); low_PWM_disc=np.delete(low_PWM_disc,index_offset_data); high_PWM_disc=np.delete(high_PWM_disc,index_offset_data); ex_high_PWM_disc=np.delete(ex_high_PWM_disc,index_offset_data)
    ex_low_temp_fluid=np.delete(ex_low_temp_fluid,index_offset_data); low_temp_fluid=np.delete(low_temp_fluid,index_offset_data); high_temp_fluid=np.delete(high_temp_fluid,index_offset_data); ex_high_temp_fluid=np.delete(ex_high_temp_fluid,index_offset_data); ex_low_PWM_fluid=np.delete(ex_low_PWM_fluid,index_offset_data); low_PWM_fluid=np.delete(low_PWM_fluid,index_offset_data); high_PWM_fluid=np.delete(high_PWM_fluid,index_offset_data); ex_high_PWM_fluid=np.delete(ex_high_PWM_fluid,index_offset_data); volt_heater = np.delete(volt_heater,index_offset_data)
    
    t_off  = t[0]
    for i in range (0, len(t)):
        t[i] = t[i] - t_off 

if t_offset_monitor_data > 0:
    i=0
    while tm[i] < t_offset_monitor_data:
        i=i+1
    index_offset_monitor_data = list(range(0,i))
    #print('____________\n'+str(i))
    #remove data until offset index
    tm = np.delete(tm,index_offset_monitor_data)
    volt_sensor= np.delete(volt_sensor,index_offset_monitor_data); pressure_chamber= np.delete(pressure_chamber,index_offset_monitor_data)
    R1_1_out = np.delete(R1_1_out,index_offset_monitor_data); temp_ADS= np.delete(temp_ADS,index_offset_monitor_data); CPU_temp = np.delete(CPU_temp,index_offset_monitor_data)
    t_off  = tm[0]
    for i in range (0, len(tm)):
        tm[i] = tm[i] - t_off

if t_cut_data != None:
    i=0
    while t[i] < t_cut_data:
        i=i+1
    index_cut_data = list(range(i,len(t)))
    t = np.delete(t,index_cut_data)
    R1_1=np.delete(R1_1,index_cut_data); R1_2=np.delete(R1_2,index_cut_data); R1_3=np.delete(R1_3,index_cut_data); R1_4=np.delete(R1_4,index_cut_data)
    R2_1=np.delete(R2_1,index_cut_data); R2_2=np.delete(R2_2,index_cut_data); R2_3=np.delete(R2_3,index_cut_data); R2_4=np.delete(R2_4,index_cut_data)
    R3_1=np.delete(R3_1,index_cut_data); ADC_1_temp=np.delete(ADC_1_temp,index_cut_data); ADC_2_temp=np.delete(ADC_2_temp,index_cut_data); ADC_3_temp=np.delete(ADC_3_temp,index_cut_data)
    pressure=np.delete(pressure,index_cut_data)
    power_voltage=np.delete(power_voltage,index_cut_data); PWM_disc=np.delete(PWM_disc,index_cut_data); PWM_fluid=np.delete(PWM_fluid,index_cut_data); pw_disc=np.delete(pw_disc,index_cut_data); pw_fluid=np.delete(pw_fluid,index_cut_data); pw_total=np.delete(pw_total,index_cut_data)
    ex_low_temp_disc=np.delete(ex_low_temp_disc,index_cut_data); low_temp_disc=np.delete(low_temp_disc,index_cut_data); high_temp_disc=np.delete(high_temp_disc,index_cut_data); ex_high_temp_disc=np.delete(ex_high_temp_disc,index_cut_data); ex_low_PWM_disc=np.delete(ex_low_PWM_disc,index_cut_data); low_PWM_disc=np.delete(low_PWM_disc,index_cut_data); high_PWM_disc=np.delete(high_PWM_disc,index_cut_data); ex_high_PWM_disc=np.delete(ex_high_PWM_disc,index_cut_data)
    ex_low_temp_fluid=np.delete(ex_low_temp_fluid,index_cut_data); low_temp_fluid=np.delete(low_temp_fluid,index_cut_data); high_temp_fluid=np.delete(high_temp_fluid,index_cut_data); ex_high_temp_fluid=np.delete(ex_high_temp_fluid,index_cut_data); ex_low_PWM_fluid=np.delete(ex_low_PWM_fluid,index_cut_data); low_PWM_fluid=np.delete(low_PWM_fluid,index_cut_data); high_PWM_fluid=np.delete(high_PWM_fluid,index_cut_data); ex_high_PWM_fluid=np.delete(ex_high_PWM_fluid,index_cut_data)

if t_cut_mon != None:
    i=0
    while tm[i] < t_cut_mon:
        i = i+1
    index_cut_monitor_data = list(range(i,len(tm)))
    tm = np.delete(tm,index_cut_monitor_data); volt_sensor= np.delete(volt_sensor,index_cut_monitor_data); pressure_chamber= np.delete(pressure_chamber,index_cut_monitor_data); R1_1_out = np.delete(R1_1_out,index_cut_monitor_data); R1_2_out= np.delete(R1_2_out,index_cut_monitor_data); temp_ADS= np.delete(temp_ADS,index_cut_monitor_data)

## Remove aberrant values
def filter_aberations(temp_list, threshold, nb_point_to_average):
    initial_list_lenght = len(temp_list) # will be use to check that the modified list has the right lenght
    nb_of_delete = 0 # will count how many point have been deleted of the list
    data_test = [] # a small sample of the temperature list (temp_list) without aberrant values
    i = 0
    good_value_index = 0 # index of a non aberrant value

    ## This try argument makes sure that the data input is correct and can be processed
    try:
        length = len(temp_list)
        if length < nb_point_to_average:
            print ('not enougth data in the data set')
            return temp_list, nb_of_delete
    except:
        print (' There is a problem with the dataset, could not remove aberration points')
        return temp_list, nb_of_delete

    ## get a small list of the inital good values to start testing
    while len(data_test) != nb_point_to_average:
        difference = temp_list[i] - temp_list[i+1]
        if temp_list[i] != np.nan and  abs(difference) < threshold:
            data_test.append(temp_list[i])
        else:
            data_test = []
        i = i + 1
    good_value_index = i - nb_point_to_average # the index with the 1st 'good value'

    ## Delete potentially aberrant value at the begging of the data set
    if good_value_index != 0:
        for i in range (0, good_value_index):
            temp_list[i]=np.nan
            nb_of_delete = nb_of_delete + 1

    ## check for aberration in the all data set and MODIFY the extracted data
    for i in range (good_value_index, len(temp_list) - 1):
        if temp_list[i+1] != np.nan:
            difference = temp_list[good_value_index] - temp_list[i+1]
            if abs(difference) > threshold:
                nb_of_delete = nb_of_delete + 1
                temp_list[i+1] = np.nan
            else:
                good_value_index = i+1            
    
    ## Check if the list is OK
    if len(temp_list) == initial_list_lenght:
        print('success')
        return temp_list, nb_of_delete
    else:
        print ('There has been an unknown issue filtering aberration')
        return temp_list, nb_of_delete

## get genrate the variable that will limit what is shown on the graph
if visual_x_lim_low != None:
    visual_x_lim_low = visual_x_lim_low
    ##get index of of the time value visual_x_lim_low on the pressure vessel data set
    i = 0
    while t[i] < visual_x_lim_low:
        i = i+1
    index_x_lim_low = i
else:
    visual_x_lim_low = 0
    index_x_lim_low = 0

if visual_x_lim_high != None:
    visual_x_lim_high = visual_x_lim_high
    ##get index of of the time value visual_x_lim_low on the pressure vessel data set
    i = 0
    while t[i] < visual_x_lim_high:
        i = i+1
    index_x_lim_high = i
else:
    visual_x_lim_high = t[len(t)-1]
    index_x_lim_high = len(t)-1

## Compute power information
total_energy_disc = 0
total_energy_fluid = 0
total_energy = 0

for i in range (index_x_lim_low, index_x_lim_high):
    try:
        total_energy_disc = total_energy_disc + (pw_disc[i] * (t[i+1]-t[i]))
    except:
        if i>0:
            pw_disc [i] = pw_disc[i-1]
            total_energy_disc = total_energy_disc + (pw_disc[i] * (t[i+1]-t[i]))
        else:
            pw_disc[0] = 0
            total_energy_disc = 0
    try:
        total_energy_fluid = total_energy_fluid + (pw_fluid[i] * (t[i+1]-t[i]))
    except:
        if i>0:
            pw_fluid [i] = pw_fluid[i-1]
            total_energy_fluid = total_energy_fluid + (pw_fluid[i] * (t[i+1]-t[i]))
        else:
            pw_fluid[0] = 0
            total_energy_fluid = 0

total_energy = total_energy_disc + total_energy_fluid
averge_disc_power = total_energy_disc/(t[index_x_lim_high] - t[index_x_lim_low])
averge_fluid_power = total_energy_fluid/(t[index_x_lim_high] - t[index_x_lim_low])
total_average_power = averge_disc_power + averge_fluid_power

print (str (total_energy_disc) + ' total energy disc')
print (str (total_energy_fluid) + ' total energy fluid')
print (str(total_energy) + ' TOTAL ENERGY')
print (str(averge_disc_power) + ' average disc power')
print (str(averge_fluid_power) + ' average fluid power')

print (str(total_average_power) + ' AVERAGE power')

## REMOVE TEMPERATURE aberration values
threshold = 0.8
nb_point_check_start = 3

R1_1, R1_1_value_deleted = filter_aberations(R1_1,threshold, nb_point_check_start)
R1_2, R1_2_value_deleted = filter_aberations(R1_2,threshold, nb_point_check_start)
R1_3, R1_3_value_deleted  = filter_aberations(R1_3,threshold, nb_point_check_start)
R1_4, R1_4_value_deleted  = filter_aberations(R1_4,threshold, nb_point_check_start)

R2_1, R2_1_value_deleted  = filter_aberations(R2_1,threshold, nb_point_check_start)
R2_2, R2_2_value_deleted  = filter_aberations(R2_2,threshold, nb_point_check_start)
R2_3, R2_3_value_deleted  = filter_aberations(R2_3,threshold, nb_point_check_start)
R2_4, R2_4_value_deleted  = filter_aberations(R2_4,threshold, nb_point_check_start)

R3_1, R3_1_value_deleted = filter_aberations(R3_1,threshold, nb_point_check_start)
R3_3, R3_3_value_deleted = filter_aberations(R3_3,threshold, nb_point_check_start)

print ('RTD1_1 nb of value deleted: ' + str(R1_1_value_deleted) + '\nRTD1_2 nb of value deleted: '+ str(R1_2_value_deleted)+ '\nRTD1_3 nb of value deleted: '+str(R1_3_value_deleted)+'\nRTD1_4 nb of value deleted: '+str(R1_4_value_deleted)+
     '\nRTD2_1 nb of value deleted: ' + str(R2_1_value_deleted) + '\nRTD1_1 nb of value deleted: '+str(R2_2_value_deleted)+ '\nRTD2_3 nb of value deleted: '+str(R2_3_value_deleted)+'\nRTD2_4 nb of value deleted: '+str(R2_4_value_deleted)+
     '\nRTD3_1 nb of value deleted: ' + str(R3_1_value_deleted) + '\nRTD3_3 nb of value deleted: ' + str(R3_3_value_deleted) )

## Generate straight lines
x = [0, t[len(t)-1]]
line_req_up = [upper_requirement, upper_requirement]
line_req_low= [low_requirement, low_requirement]


## FIRST plot
plt.figure(figsize=(8.7,11), dpi=300) # Plot on a A4 format ==> easier implementation in text

# TEMPERATURE disc plot
plt.subplot(3,1,1)  # (nRows, nColumns, axes number to plot)
plt.plot(t, R2_1, color='chartreuse',  marker = "+", linewidth=1, label = 'RTD 2_1, surface of the disc,\nused to regulate the disc heater. No thermal paste')
plt.plot(t, R2_2, color='tab:pink', marker = "+", linewidth=1, label = "RTD 2_2, surface of disc internal position, with thermal paste")
plt.plot(t, R1_2, color='tab:blue', marker = "+", linewidth=1, label = 'RTD 1_2, inside a MCSD chamber below the motor mount')
plt.plot(t, R2_4, color='tab:olive', marker = "+", linewidth=1, label = "RTD 2_4, inside a MCSD chamber on the 1U side")
plt.plot(t, R1_1, color='salmon',  marker = "+", linewidth=1, label = "RTD 1_1, Inside a MCSD disc on the fluid side")
plt.plot(t, R2_3, color='tab:grey', marker = "+", linewidth=1, label = "RTD 2_3, Inside a MCSD disc side")
plt.plot(x, line_req_up, 'r-.', linewidth=0.5, label = str(upper_requirement)+ ' °C, the upper temperature limit for the C. elegans' )
plt.plot(x, line_req_low, 'b-.', linewidth=0.5, label = str(low_requirement)+ ' °C, the lower temperature limit for the C. elegans' )

plt.title('Temperature on different points of MCSD,\ninside chamber and on the surface to control the heater\nduring the pseudo thermal vacuum preliminary test 12')  
plt.xlabel('Time (sec)', loc = 'right'); plt.ylabel('Temperature (Celsius)')
plt.xlim(visual_x_lim_low, visual_x_lim_high)
#plt.ylim(20, 50)
plt.grid(axis='x', color='0.95')
plt.grid(axis='y', color='0.95')
plt.legend(loc='upper left', bbox_to_anchor=(-0.1, -0.2), fontsize = 'small', ncol = 2 )

# TEMPERATURE fluid plot
plt.subplot(3,1,3)  # (nRows, nColumns, axes number to plot)
plt.plot(t, R1_3, color='tab:orange', marker = "+", linewidth=1, label = 'RTD 1_3, on the fluidic bag,\nused regulate the fluidic heater')
plt.plot(t, R1_4, color='tab:green', marker = "+", linewidth=1, label = 'RTD 1_4, on the aluminium rod next to the fluidic bag')
plt.plot(t, R3_1, color='black', dashes=[6, 2], linewidth=1, label = "RTD 3_1, on the camera plate")
#plt.plot(t, R3_3, color='blue', dashes=[6, 2], linewidth=1, label = "RTD 3_1, on the LED PCB")
#plt.plot(t, ADC_1_temp, color='black', dashes=[6, 2], linewidth=1, label = "ADC_1 internal temperature reading")
#plt.plot(t, ADC_2_temp, color='grey', dashes=[6, 2], linewidth=1, label = "ADC_2 internal temperature reading")
#plt.plot(t, ADC_3_temp, color='chocolate', dashes=[6, 2], linewidth=1, label = "ADC_3 internal temperature reading")
plt.title('Temperature on different points inside the pressure vessel\nduring the pseudo thermal vacuum preliminary test 12') 
plt.xlabel('Time (sec)', loc = 'right'); plt.ylabel('Temperature (Celsius)')
plt.xlim(visual_x_lim_low, visual_x_lim_high)
#plt.ylim(0, 20)
plt.grid(axis='x', color='0.95')
plt.grid(axis='y', color='0.95')
plt.legend(loc='upper left', bbox_to_anchor=(-0.07, -0.2), fontsize = 'small', ncol = 2 )

#plt.subplots_adjust(left = 0.071,bottom=0.043, right = 0.912, top= 0.962, hspace = 0.45)
plt.savefig(os.path.join((os.path.join(file_path, 'plots')), name_image_output + '_temperatures.png'), format = 'png')


##SECOND plot
plt.figure(figsize=(8.7,11), dpi=300) # Plot on a A4 format ==> easier implementation in text
# PRESSURE plot
plt.subplot(3,1,2)
plt.plot(t, pressure, color='black', label = "Pressure measured inside the pressure vessel (kPa)")

plt.title('Pressure measured inside the pressure vessel\nduring the pseudo thermal vacuum preliminary test 12')  
plt.xlabel('Time (sec)', loc = 'right'); plt.ylabel('pressure (kPa)')
plt.xlim(visual_x_lim_low, visual_x_lim_high)
#plt.ylim(0, 12)
plt.grid(axis='x', color='0.95')
plt.grid(axis='y', color='0.95')
plt.legend(loc='upper left', bbox_to_anchor=(0, -0.08), fontsize = 'small')

##insertion 1st plot
plt.subplots_adjust(left = 0.071,bottom=0.043, right = 0.912, top= 0.962, hspace = 0.45)
plt.savefig(os.path.join((os.path.join(file_path, 'plots')), name_image_output + '_pressure.png'), format = 'png')

## THIRD plot
# POWER plot
plt.figure(figsize=(8.7,11), dpi=300) # Plot on a A4 format ==> easier implementation in text
plt.step(t, pw_disc, color='tab:red', where='post', marker = '.', linewidth=1, label = 'Power at disc heater. Average Power: '+ '%.2f' % averge_disc_power +' W. energy consumed: '+ '%.2f' % total_energy_disc + ' J.')
plt.step(t, pw_fluid, color='tab:blue', where='post', marker = '.', linewidth=1, label = 'Power at fluid heater. Average Power: '+ '%.2f' % averge_fluid_power +' W. Total energy consumed: '+ '%.2f' % total_energy_fluid + ' J.')
plt.title('Heaters Power consumption (left axis) linked \nto the temperature regulated inside the pressure vessel (right axis)\nduring the pseudo thermal vacuum preliminary test 12')  
plt.xlabel('Time (sec)', loc = 'right'); plt.ylabel('Power dissipated (Watt)')
plt.grid(axis='x', color=' 0.95')
plt.legend(loc='upper left', bbox_to_anchor=(0, -0.05))
plt.xlim(visual_x_lim_low, visual_x_lim_high)
#plt.ylim(0, 12)
plt.twinx()
plt.plot(t, R2_1, color='salmon',  marker = "+", linewidth=1, label = "RTD 2_1, surface of the disc,\nused to regulate the disc heater. No thermal paste")
plt.plot(t, ex_high_temp_disc, color='coral', dashes=[6, 2], linewidth=0.5, label =  'Extreme high temperature threshold for disc heater regulation')
plt.plot(t, high_temp_disc, color='lightsalmon', dashes=[6, 2], linewidth=0.5, label = 'High temperature threshold for disc heater regulation')
plt.plot(t, low_temp_disc, color='salmon', dashes=[6, 2], linewidth=0.5, label = 'Low temperature threshold for disc heater regulation')
plt.plot(t, ex_low_temp_disc, color='tomato', dashes=[6, 2], linewidth=0.5, label = 'Extreme low temperature threshold for disc heater regulation')

plt.plot(t, R1_3, color='aqua',  marker = "+", linewidth=1, label = "RTD 1_3, on the fluidic bag,\nused regulate the fluidic heater")
plt.plot(t, ex_high_temp_fluid, color='darkcyan', dashes=[6, 2], linewidth=0.5, label =  'Extreme high temperature threshold for fluid heater regulation')
plt.plot(t, high_temp_fluid, color='c', dashes=[6, 2], linewidth=0.5, label = 'High temperature threshold for fluid heater regulation')
plt.plot(t, low_temp_fluid, color='cyan', dashes=[6, 2], linewidth=0.5, label = 'Low temperature threshold for fluid heater regulation')
plt.plot(t, ex_low_temp_fluid, color='dodgerblue', dashes=[6, 2], linewidth=0.5, label = 'Extreme low temperature threshold for fluid heater regulation')

plt.ylabel('Temperature (°C)')
plt.xlim(visual_x_lim_low, visual_x_lim_high)
plt.grid(axis='y', color='0.95')
#plt.ylim(0, 12)
plt.legend(loc='upper left', bbox_to_anchor=(-0.05, -0.15), ncol = 2, fontsize = 'small')
plt.subplots_adjust(left = 0.071,bottom=0.4, right = 0.912, top= 0.9, hspace = 0.37)
#plt.annotate('total energy disc dissipated by the disc heater: '+ str (total_energy_disc) + ' J', )
plt.savefig(os.path.join((os.path.join(file_path, 'plots')), name_image_output + '_pwr.png'), format = 'png')
#plt.show()

## FOURTH PLOT
plt.figure(figsize=(8.7,11), dpi=300) # Plot on a A4 format ==> easier implementation in text
# TEMPERATURE monitoring
plt.subplot(3,1,1)  # (nRows, nColumns, axes number to plot)
plt.plot(tm, R1_1_out, color='blue', marker = "+", linewidth=1, label = "RTD 1_1, the temperature on the pressure vessel")
plt.plot(tm, temp_ADS, color='red', marker = "+",linewidth=1, label = "internal temperature of the ADS1248")
plt.plot(tm, CPU_temp, color='green', marker = "+",linewidth=1, label = "Raspberrypi CPU temperature")
plt.title('Temperatures measured outside the pressure vessel inside the vacuum chamber\nduring the pseudo thermal vacuum preliminary test 12')
plt.xlabel('Time (sec)', loc = 'right'); plt.ylabel('Temperature (Celsius)')
plt.grid(axis='x', color='0.95')
plt.grid(axis='y', color='0.95')
plt.xlim(visual_x_lim_low, visual_x_lim_high)
#plt.ylim(-10, 10)
plt.legend(loc='upper left', bbox_to_anchor=(0, -0.08), fontsize = 'small')

# PRESSURE plot
plt.subplot(3,1,3)
plt.plot(tm, pressure_chamber, color='black', linewidth=1, label = "Pressure measured in the vacuum chamber")
plt.title('Pressure measured outside the pressure vessel inside the vacuum chamber\nduring the pseudo thermal vacuum preliminary test 12')
plt.xlabel('Time (sec)', loc = 'right'); plt.ylabel('Pressure (bar)')
plt.grid(axis='x', color='0.95')
plt.grid(axis='y', color='0.95')
plt.xlim(visual_x_lim_low, visual_x_lim_high)
#plt.ylim(0, 0.04)
plt.legend(loc='upper left', bbox_to_anchor=(0, -0.08), fontsize = 'small')
plt.savefig(os.path.join((os.path.join(file_path, 'plots')), name_image_output + '_mon.png'), format = 'png')
