
# PV Systems Data Analysis

This repository contains resources and tools for analyzing photovoltaic (PV) systems, focusing on optimizing panel tilt and azimuth angles to maximize energy output in the Netherlands.

## Overview

The primary components of this repository include:

- **Jupyter Notebook**: Performs simulations using the `pvlib` library and the PVWatts model to estimate and optimize the energy output of solar panels based on their tilt and azimuth angles.

- **Datasets**:
  - `Netherlands_Energy_Grid_Results.csv`: Contains results related to the energy grid in the Netherlands.
  - `shape_files/`: Directory containing shapefiles pertinent to the analysis.

## Key Features

1. **Data Handling**:
   - Loads measured solar field data, focusing on Polycrystalline Silicon (Poly-Si) panels.
   - Filters datasets to include specific time frames for accurate comparison and analysis.
   - Removes anomalies and ensures alignment between measured and simulated data.

2. **Simulation with PVWatts**:
   - Implements the PVWatts model via `pvlib` to simulate energy production.
   - Considers parameters like panel tilt, azimuth, ambient temperature, wind speed, and irradiance (GHI, DNI, DHI).
   - Applies calibration factors to align simulated data with measured values.
   - Validates simulations to ensure a strong fit between simulated and measured data.

3. **Optimization**:
   - Conducts grid searches for optimal tilt and azimuth angles.
   - Identifies optimal settings per location for maximum energy yield.

4. **Visualization**:
   - Generates heatmaps and visualizations of energy outputs across various azimuth and tilt angles.
   - Displays optimized results for different locations within the Netherlands.

## Getting Started

### Prerequisites

Ensure you have the following installed:

- Python 3.8 or higher
- Jupyter Notebook
- Required Python packages:
  - `pvlib`
  - `numpy`
  - `pandas`
  - `matplotlib`
  - `geopandas`
  - `shapely`

You can install the necessary packages using:

```bash
pip install pvlib numpy pandas matplotlib geopandas shapely
```

### Installation

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/Qrax/PV-Systems-Data.git
   cd PV-Systems-Data
   ```

2. **Set Up the Environment**:

   It's recommended to use a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies**:

   Install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

### Usage

1. **Open the Jupyter Notebook**:

   Start Jupyter Notebook:

   ```bash
   jupyter notebook
   ```

2. **Run the Notebook**:

   - Navigate to `Simulaties_na_ceck_met_amolf.ipynb` and open it.
   - Run the cells sequentially to perform data loading, simulation, optimization, and visualization.

## Data Sources

- Measured solar field data from AMOLF, focusing on Polycrystalline Silicon (Poly-Si) panels.
- Simulation data generated using the PVWatts model via `pvlib`.

## Results

- Optimal tilt and azimuth angles for maximizing energy production in various locations within the Netherlands.
- Comparisons between measured and simulated performance, highlighting regional differences and ideal panel configurations.
