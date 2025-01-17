### **Purpose**
The Jupyter Notebook supports the research on photovoltaic (PV) systems optimization described in the paper titled **"PV-Optimalisatie in Nederland: Invloed van Azimuth- en Kantelhoek"**. It performs simulations using the Python library `pvlib` and the PVWatts model to estimate and optimize the energy output of solar panels based on their tilt and azimuth angles in the Netherlands.

---

### **Key Functionalities**
1. **Data Handling**:
   - Loads measured solar field data from AMOLF, focusing on Polycrystalline Silicon (Poly-Si) panels.
   - Filters the dataset to include data from May and June 2021 for a fair comparison and analysis.
   - Removes anomalies and ensures alignment between measured and simulated data.

2. **Simulation with PVWatts**:
   - Implements the PVWatts model via `pvlib` to simulate energy production.
   - Considers parameters like panel tilt, azimuth, ambient temperature, wind speed, and irradiance (GHI, DNI, DHI).
   - Applies a calibration factor (1.32) to align simulated data with measured values.
   - Validates the simulation with an R² value of 0.90, indicating a strong fit between simulated and measured data.

3. **Optimization**:
   - Conducts a fine-tuned grid search for tilt angles (38°–42°) and azimuth angles (250°–260°).
   - Identifies optimal settings per location for maximum energy yield.

4. **Visualization**:
   - Generates heatmaps and visualizations of energy outputs across various azimuth and tilt angles.
   - Displays optimized results for Amsterdam and other provincial capitals in the Netherlands.

5. **Results Summary**:
   - Provides insights into optimal angles for maximizing energy production.
   - Compares measured vs. simulated performance, emphasizing regional differences and ideal panel configurations.

---

### **Relationship to the Paper**
- **Data and Methods**: The notebook underpins the paper's methodology section by handling data preprocessing, simulations, and optimization tasks.
- **Results and Discussion**: Outputs from the notebook (e.g., optimal tilt and azimuth angles, heatmaps, and energy yield tables) directly support the paper's findings.
- **Validation**: The paper cites the notebook's calibration and validation process to ensure the reliability of simulations.

