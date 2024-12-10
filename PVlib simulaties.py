import pvlib
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from pvlib.location import Location

# Gegevens voor Amsterdam
latitude_amsterdam = 52.3676
longitude_amsterdam = 4.9041
timezone_amsterdam = 'Europe/Amsterdam'
name_amsterdam = 'Amsterdam'

# Gegevens voor Sydney
latitude_sydney = -33.8688
longitude_sydney = 151.2093
timezone_sydney = 'Australia/Sydney'
name_sydney = 'Sydney'

# Gegevens voor McMurdo Station, Antarctica
latitude_antarctica = -77.8419
longitude_antarctica = 166.6863
timezone_antarctica = 'Antarctica/McMurdo'
name_antarctica = 'Antarctica (McMurdo Station)'

# Initialiseer locaties
location_amsterdam = Location(latitude=latitude_amsterdam, longitude=longitude_amsterdam, tz=timezone_amsterdam, name=name_amsterdam)
location_sydney = Location(latitude=latitude_sydney, longitude=longitude_sydney, tz=timezone_sydney, name=name_sydney)
location_antarctica = Location(latitude=latitude_antarctica, longitude=longitude_antarctica, tz=timezone_antarctica, name=name_antarctica)

# Definieer de tijdstippen in UTC over een jaar
times = pd.date_range(start='2023-06-01', end='2024-06-01', freq='1H', tz='UTC')

# Bereken de zonnepositie
solar_position_amsterdam = location_amsterdam.get_solarposition(times)
solar_position_sydney = location_sydney.get_solarposition(times)
solar_position_antarctica = location_antarctica.get_solarposition(times)

# Bereken de clear-sky straling met het Ineichen-model
clearsky_amsterdam = location_amsterdam.get_clearsky(times, model='ineichen')
clearsky_sydney = location_sydney.get_clearsky(times, model='ineichen')
clearsky_antarctica = location_antarctica.get_clearsky(times, model='ineichen')

# Voeg temperatuur en windsnelheid toe aan de weergegevens
weather_amsterdam = clearsky_amsterdam.copy()
weather_amsterdam['temp_air'] = 15  # Luchttemperatuur in graden Celsius
weather_amsterdam['wind_speed'] = 2  # Windsnelheid in m/s

weather_sydney = clearsky_sydney.copy()
weather_sydney['temp_air'] = 20
weather_sydney['wind_speed'] = 3

weather_antarctica = clearsky_antarctica.copy()
weather_antarctica['temp_air'] = -20
weather_antarctica['wind_speed'] = 5

# Haal module- en omvormerparameters op
sandia_modules = pvlib.pvsystem.retrieve_sam('SandiaMod')
cec_inverters = pvlib.pvsystem.retrieve_sam('cecinverter')

module = sandia_modules['Canadian_Solar_CS5P_220M___2009_']
inverter = cec_inverters['ABB__MICRO_0_25_I_OUTD_US_208__208V_']

# Definieer PV-systemen met module_type en racking_model
system_amsterdam = pvlib.pvsystem.PVSystem(
    surface_tilt=30,
    surface_azimuth=180,
    module_parameters=module,
    inverter_parameters=inverter,
    module_type='glass_polymer',
    racking_model='open_rack'
)

system_sydney = pvlib.pvsystem.PVSystem(
    surface_tilt=0,
    surface_azimuth=0,
    module_parameters=module,
    inverter_parameters=inverter,
    module_type='glass_polymer',
    racking_model='open_rack'
)

system_antarctica = pvlib.pvsystem.PVSystem(
    surface_tilt=10,
    surface_azimuth=0,
    module_parameters=module,
    inverter_parameters=inverter,
    module_type='glass_polymer',
    racking_model='open_rack'
)

# Maak ModelChain-objecten
mc_amsterdam = pvlib.modelchain.ModelChain(system_amsterdam, location_amsterdam)
mc_sydney = pvlib.modelchain.ModelChain(system_sydney, location_sydney)
mc_antarctica = pvlib.modelchain.ModelChain(system_antarctica, location_antarctica)

# Voer de berekeningen uit met weergegevens
mc_amsterdam.run_model(weather_amsterdam)
mc_sydney.run_model(weather_sydney)
mc_antarctica.run_model(weather_antarctica)

# Voer de berekeningen uit met weergegevens
mc_amsterdam.run_model(weather_amsterdam)
mc_sydney.run_model(weather_sydney)
mc_antarctica.run_model(weather_antarctica)


# Haal de AC-vermogenoutput op
ac_power_amsterdam = mc_amsterdam.results.ac
ac_power_sydney = mc_sydney.results.ac
ac_power_antarctica = mc_antarctica.results.ac

# Bereken de totale energieopbrengst in kWh
energy_amsterdam = ac_power_amsterdam.sum() / 1000  # van Wh naar kWh
energy_sydney = ac_power_sydney.sum() / 1000
energy_antarctica = ac_power_antarctica.sum() / 1000

print('Totale jaarlijkse energieopbrengst:')
print('Amsterdam: {:.2f} kWh'.format(energy_amsterdam))
print('Sydney: {:.2f} kWh'.format(energy_sydney))
print('Antarctica: {:.2f} kWh'.format(energy_antarctica))

# Visualiseer de AC-vermogenoutput
fig, axes = plt.subplots(3, 1, figsize=(15, 12), sharex=True)

# Plot voor Amsterdam
ac_power_amsterdam.plot(ax=axes[0], label='AC Vermogen')
axes[0].set_ylabel('AC Vermogen (W)')
axes[0].set_title('AC Vermogen in {}'.format(name_amsterdam))
axes[0].legend()

# Plot voor Sydney
ac_power_sydney.plot(ax=axes[1], label='AC Vermogen', color='orange')
axes[1].set_ylabel('AC Vermogen (W)')
axes[1].set_title('AC Vermogen in {}'.format(name_sydney))
axes[1].legend()

# Plot voor Antarctica
ac_power_antarctica.plot(ax=axes[2], label='AC Vermogen', color='green')
axes[2].set_ylabel('AC Vermogen (W)')
axes[2].set_title('AC Vermogen in {}'.format(name_antarctica))
axes[2].legend()

plt.xlabel('Tijd (UTC)')
plt.tight_layout()
plt.show()

# Visualiseer de cumulatieve energieopbrengst
cumulative_energy_amsterdam = ac_power_amsterdam.cumsum() / 1000  # in kWh
cumulative_energy_sydney = ac_power_sydney.cumsum() / 1000
cumulative_energy_antarctica = ac_power_antarctica.cumsum() / 1000

plt.figure(figsize=(15, 5))
plt.plot(cumulative_energy_amsterdam.index, cumulative_energy_amsterdam, label='Amsterdam')
plt.plot(cumulative_energy_sydney.index, cumulative_energy_sydney, label='Sydney')
plt.plot(cumulative_energy_antarctica.index, cumulative_energy_antarctica, label='Antarctica')
plt.ylabel('Cumulatieve Energie (kWh)')
plt.xlabel('Tijd (UTC)')
plt.title('Cumulatieve Energieopbrengst over een Jaar')
plt.legend()
plt.show()
