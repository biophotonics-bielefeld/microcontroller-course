from kennlinienschreiber import *
import matplotlib.pyplot as plt
import numpy as np


ser = open_unoR4_port()

# set at which DAC values to sample
dac_values = np.arange(0, 4096, 128, dtype=int)
adc_a1_values = np.empty_like(dac_values)
adc_a2_values = np.empty_like(dac_values)

# set the DAC, read the ADC for pin 1 and pin 2
for i in range(dac_values.size):
    set_dac(ser,dac_values[i])
    adc_a1_values[i] = read_adc(ser, 1)
    adc_a2_values[i] = read_adc(ser, 2)
   
# compute the difference between a2 and a1
adc_a2a1 = np.subtract(adc_a2_values, adc_a1_values)

# scale by voltages
dac_volts = dac_values.astype('float64')
dac_volts /= 4096. / 5.
adc_volts = adc_a2a1.astype('float64')
adc_volts /= 16384. / 5.

# plot
plt.plot(dac_volts, adc_volts)
plt.show()





