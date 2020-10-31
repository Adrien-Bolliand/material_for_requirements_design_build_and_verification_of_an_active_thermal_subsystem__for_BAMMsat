In all test, The system include inside the flight BAMMsat pressure vessel:
- one of the flight MCSD
    - 4 RTD inside chambers spread at 90°
    - 2 RTD on the surface of the disc
        -1 on the exterior on the disc, without thermal past, that regulate the disc bang bang controller
        -1 on closer to the center with thermal past
    - a 1st iteration of the motor mount on top of the MCSD
    - the flight fan continuously functioning connected to 5 V
    - 1 fluidic bag filled with water
    - 3 ADS1248
    - 1 pressure sensor
    - 1 RPi with software similar to flight to read sensor and control heater
    - flight disc heater bellow the disc. Spacer between the disc and the fluidic plate: 1 nylon spacer + 2 M2 spacer


TEST_10
The freezer temperature was set to -50°C
13.5 difference between monitoring data and PV data. Monitor in advance
Realised that the bang bangs were not using the right sensor to regulate the heater ==> STOP recording.
updated the code started TEST 11

TEST_11
The freezer temperature was set to -50°C
10.8 sec difference between monitoring data and PV data. Monitor in advance
176  sec on the monitoring data, sprayed water on the feedthroughs
1057 sec on the monitoring data, sprayed water on the feedthroughs
2434 sec on the monitoring data, sprayed water on the feedthroughs
3051 sec on the monitoring data, sprayed water on the feedthroughs
before 7800 sec put cable-ties on the USB cables 


TEST_12
The freezer temperature was set to -50°C
10.8 sec difference between monitoring data and PV data. Monitor in advance
it seems that the temperature of the disc is becoming stable. But with stability it seems that the temperature difference between the surface and inside the disc is getting larger. In this particular case, noise on the sensors seems problematic.
If on the monitoring data, the pressure drop it is because water where sprayed on the feedthroughs.

TEST_14
The freezer temperature was set to -50°C
10.8 sec difference between monitoring data and PV data. Monitor in advance
The pressure environment was left to it stable, but higher value of 80 mbar instead of regularly spraying water on the feedthroughs.
If on the monitoring data, the pressure drop it is because water where sprayed on the feedthroughs.

TEST_15
The freezer temperature was set to -50°C
13 sec difference between monitoring data and PV data. Monitor in advance
looks like RTD 2_4 failed.

TEST_16
The freezer temperature was set to -50°C
10.8 sec difference between monitoring data and PV data. Monitor in advance
decided to lower by two °C the previous bang-bang temperature thresholds
RTD 2_4 failed still down
seems to have kept the temperature inside chamber within requirement.
At t= 6674 the pump was stopped.  Manual ON/OFF cycles of the vacuum pump were performed to keep the pressure between 300 and 400 mbar. 350 mab corresponding to the 8000 altitude viewed as the worst thermal environment of the flight.
The fact that this cycle would induce the pressure vessel cycle stress was considered.
Those following elements give a green light:
- variation of pressure relatively small compared to the 3 bar that the pressure survived, during the verification process
- Since the campaign is delayed, if the vessel does break, there is enough time to order a new one.

TEST_17
The freezer temperature was set to -60°C
10.8 sec difference between monitoring data and PV data. Monitor in advance
Between 0 to 6000 sec (1h40min),aimed to reproduce the cold environment: ~ 400 mbar at -60 °C  <==> bellow 8000 m of altitude at -60 °C.  Manual ON/OFF cycles of the vacuum pump were performed to keep the pressure between 300 and 400 mbar. 350 mab corresponding to the 8000 altitude viewed as the worst thermal environment of the flight.
The fact that this cycle would induce the pressure vessel cycle stress was considered.
Between 6000 to 17000 sec (~3h), aimed to reproduce the flight environment. But the low-pressure environment was around 80 mbar instead of 20 mbar which correspond to an altitude around 20000m instead of 25000m. This can be viewed as the worst condition for the thermal subsystem. The temperature was set at -60°C.
After 6000 sec, if on the monitoring data, the pressure drop it is because water where sprayed on the feedthroughs.