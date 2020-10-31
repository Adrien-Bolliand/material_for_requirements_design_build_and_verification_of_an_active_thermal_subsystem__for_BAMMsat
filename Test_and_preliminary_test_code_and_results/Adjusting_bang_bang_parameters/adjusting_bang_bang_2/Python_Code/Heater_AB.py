# Description:
#  This is a very simple class to store physical data about the heater used during test and/or for flight
#  Written by Adrien Bolliand
#
 #list of attributs:
  # name        (str)   meaningfull name for the heater
  # resistor    (float) value of the resistor in ohms
  # voltage_in  (float) value of the heater voltage input
 
class Heater:
  def __init__(self, name, resistor_value, voltage_in):
      self.name = name
      self.resistor = resistor_value
      self.voltage_in = voltage_in