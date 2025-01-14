import pvlib

from pvlib.modelchain import ModelChain
from pvlib.location import Location
from pvlib.pvsystem import PVSystem
from pvlib.temperature import TEMPERATURE_MODEL_PARAMETERS

import pandas as pd
import matplotlib.pyplot as plt

locatie_naam = "amolf"
latitude = 52.3676
longitude = 4.9041
timezone = "Europe/Amsterdam"
surface_tilt = 45
surface_azimuth = 180 # south

location = Location(latitude, longitude, tz=timezone, name=locatie_naam)

scandia_modules = pvlib.pvsystem.retrieve_sam('SandiaMod')
cec_inverters = pvlib.pvsystem.retrieve_sam('CECInverter')

module = scandia_modules['Canadian_Solar_CS5P_220M___2009_']
inverter = cec_inverters['ABB__MICRO_0_25_I_OUTD_US_208__208V_']

temperature_parameters = TEMPERATURE_MODEL_PARAMETERS['sapm']['open_rack_glass_glass']

system = PVSystem(surface_tilt=surface_tilt, surface_azimuth=surface_azimuth,
                  module_parameters=module, inverter_parameters=inverter,
                  temperature_model_parameters=temperature_parameters,
                  modules_per_string=4, strings_per_inverter=1)

modelchain = ModelChain(system, location)


times = pd.date_range(start='2021-07-01', end='2021-07-07',
                      freq='1min', tz=location.tz)

clear_sky = location.get_clearsky(times)

clear_sky.plot()
plt.show()

modelchain.run_model(weather=clear_sky)
modelchain.results.ac.plot()
plt.show()