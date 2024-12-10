# REFPROP Python Interface

This repository provides a Python interface to [NIST REFPROP 10](https://www.nist.gov/srd/refprop) for generating thermophysical property data and visualizing results using Plotly. The code allows you to:

- Interact with the REFPROP 10 DLL for fluid property calculations.
- Generate data over specified temperature and pressure ranges.
- Visualize the resulting 3D surface and scatter plots of properties.

## Contents

- `refprop_install_dir/`: A directory (excluded from version control) that contains:
  - `REFPRP64.DLL`: The REFPROP 10 DLL.
  - `.FLD` files and other necessary REFPROP data files.

- `main.py`: The main script that:
  - Defines the configuration for the REFPROP calculations (fluids, equation of state, temperature/pressure ranges).
  - Runs the data generation and plotting routines.
  - Produces HTML plots of the results.

- `refprop.py`: A module providing the `RefpropInterface` class, which handles interaction with the REFPROP DLL via ctypes.

- `utils.py`: Utility functions for generating temperature/pressure sample grids or Latin Hypercube samples.

## Prerequisites

1. **REFPROP License & Installation**:  
   You must have a valid REFPROP 10 license and installation. The `refprop_install_dir` should contain:
   - `REFPRP64.DLL`
   - `HMX.BNC`, `FLD` files, and other REFPROP configuration files.

   If you do not have this directory, please follow NIST's official instructions to install REFPROP and copy the necessary files to `refprop_install_dir`.

2. **Python Environment**:  
   Ensure you have Python 3.7+ and the following packages installed:
   - `pandas`
   - `tqdm`
   - `plotly`
   - `pyDOE` (for experimental design)
   - `ctypes` (included with standard Python)

   You can install required packages using:
   ```bash
   pip install pandas tqdm plotly pyDOE
   ```
   
   *Note*: `ctypes` is included by default in most Python installations.

3. **Windows Platform**:  
   The provided interface (`ctypes.WinDLL`) is configured for Windows. For other operating systems, you will need to adjust the DLL loading and possibly compile your own REFPROP shared library.

## Setup

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/josephmcg16/py-refprop
   cd py-refprop
   ```

2. **REFPROP Install Directory**:
   Place your REFPROP files inside `refprop_install_dir/`. The `.gitignore` file is set to ignore this directory, so sensitive license files are not accidentally committed.

3. **Configuration in `main.py`**:
   Open `main.py` in your editor and adjust the following as needed:
   - `INSTALL_PATH`: Set this to the absolute path of the REFPROP installation directory.
   - `EQUATION_OF_STATE`: Choose from `"AGA8"`, `"PR"`, `"GERG"`, or `None` to use REFPROP’s default.
   - `FLUIDS`: Define the fluid(s) and their mole fractions. For example:
     ```python
     FLUIDS = {
         "CO2": 1.0,  # 100% CO2
     }
     ```
   - Temperature and Pressure Ranges & Resolution:
     Adjust `n_grid_temperature`, `n_grid_pressure`, `temperature_range`, and `pressure_range` to specify the DOE (design of experiments):
     ```python
     n_grid_temperature=100,
     n_grid_pressure=100,
     temperature_range=(268.15, 353.15),  # K
     pressure_range=(200, 5.0101325e7),   # Pa
     ```

   - Plotting Parameters:
     If desired, modify the axes for the Plotly 3D plots:
     ```python
     PLOTTING_PARAMS = {
         "xaxis": "P",  # Pressure
         "yaxis": "T",  # Temperature
         "zaxis": "D",  # Density
     }
     ```

4. **Run the Code**:
   After adjusting parameters, run:
   ```bash
   python main.py
   ```
   This will:
   - Compute fluid properties for the specified grid of T and P.
   - Generate a 3D surface plot (`refprop_surface_plot.html`) and a 3D scatter plot (`refprop_scatter_plot.html`) in the current directory.

5. **View the Results**:
   Open the generated HTML files in your web browser to interact with the 3D visualizations.

## Troubleshooting

- **DLL loading errors**:  
  If the REFPROP DLL cannot be loaded, ensure:
  - You are on Windows (or have adapted the code for your OS).
  - `INSTALL_PATH` points to the correct directory containing `REFPRP64.DLL`.
  
- **Property calculation errors**:  
  Check if your chosen fluid and state points are valid. REFPROP may fail if you request properties outside its defined ranges or for unsupported fluid combinations.

- **Missing fluid files**:  
  Ensure your `.FLD` files (e.g., `CO2.FLD`) and `HMX.BNC` file are present in `refprop_install_dir`.

## Customization and Extensions

- **Multiple Fluids**:  
  Update the `FLUIDS` dictionary with multiple entries and their respective mole fractions, for example:
  ```python
  FLUIDS = {
      "N2": 0.8,
      "CH4": 0.2,
  }
  ```
  Make sure all required `.FLD` files are in the `refprop_install_dir`.

- **Equation of State (EOS)**:  
  Change `EQUATION_OF_STATE` to `"AGA8"`, `"PR"`, `"GERG"`, or `None` to explore different EOS models.

- **Sampling Method**:  
  In `utils.py`, you can switch from a regular grid to a Latin Hypercube Sample (LHS) by adjusting the code that calls `generate_temperature_pressure_samples` with `method="lhs"`.  
  ```python
  df = get_refprop_data(
      n_grid_temperature=100,
      n_grid_pressure=100,
      temperature_range=(268.15, 353.15),
      pressure_range=(200, 5.0101325e7),
      # If you want LHS sampling:
      # method="lhs"
  )
  ```

## License & Acknowledgments

- **REFPROP** is a product of the National Institute of Standards and Technology (NIST). You must have a valid license to use REFPROP in your code.
- This repository is intended as a convenience to integrate REFPROP with Python for educational and internal research purposes.