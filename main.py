import pandas as pd
from tqdm import tqdm
import plotly.graph_objects as go
import plotly.express as px
from refprop import RefpropInterface
from utils import generate_temperature_pressure_samples


INSTALL_PATH = r"C:\users\mcgov-jo\OneDrive - TUV SUD\Desktop\py-refprop\refprop_install_dir"  # path to REFPROP installation
EQUATION_OF_STATE = None  # must be "AGA8", "PR", "GERG" or None (default eos)
FLUIDS = {
    "CO2": 1,
}
PLOTTING_PARAMS = {
    "xaxis": "P",  # Pressure
    "yaxis": "T",  # Temperature
    "zaxis": "D",  # Density
}


def get_refprop_data(
    n_grid_temperature, n_grid_pressure, temperature_range, pressure_range
):
    doe = generate_temperature_pressure_samples(
        n_grid_temperature=n_grid_temperature,
        n_grid_pressure=n_grid_pressure,
        temperature_range=temperature_range,
        pressure_range=pressure_range,
    )
    refprop = RefpropInterface(INSTALL_PATH, EQUATION_OF_STATE)
    df = pd.DataFrame()
    for index, sample in tqdm(doe.iterrows(), total=len(doe)):
        try:
            refprop_output = refprop.refprop2dll(
                ";".join(FLUIDS.keys()),
                "TP",  # Input string of properties (Temperature and Pressure)
                "T,P,D,VIS,PIP",  # Output properties to be calculated
                21,  # mass base SI units
                0,
                sample["Temperature [K]"],  # Temperature in K
                sample["Pressure [Pa]"],  # Pressure in Pa
                FLUIDS.values(),  # Mole fractions
            )
            df = pd.concat([df, pd.DataFrame(refprop_output, index=[index])])
        except Exception as e:
            print(f"Error at index {index}: {e}")
            raise e
    df[["T", "P"]] = doe[["Temperature [K]", "Pressure [Pa]"]]
    return df


def main():
    df = get_refprop_data(
        n_grid_temperature=100,
        n_grid_pressure=100,
        temperature_range=(268.15, 353.15),
        pressure_range=(200, 5.0101325e7),
    )
    pivot_df = df.pivot(
        index=PLOTTING_PARAMS["yaxis"],
        columns=PLOTTING_PARAMS["xaxis"],
        values=PLOTTING_PARAMS["zaxis"],
    )

    fig = go.Figure()
    fig.add_trace(
        go.Surface(
            z=pivot_df.values,
            x=pivot_df.columns,
            y=pivot_df.index,
            colorscale="Viridis",
        )
    )
    fig.update_layout(
        scene=dict(
            xaxis_title=PLOTTING_PARAMS["xaxis"],
            yaxis_title=PLOTTING_PARAMS["yaxis"],
            zaxis_title=PLOTTING_PARAMS["zaxis"],
        ),
    )
    fig.write_html("refprop_surface_plot.html")

    fig = px.scatter_3d(
        df,
        x=PLOTTING_PARAMS["xaxis"],
        y=PLOTTING_PARAMS["yaxis"],
        z=PLOTTING_PARAMS["zaxis"],
        color="PIP",
    )
    fig.update_traces(marker=dict(size=3))
    fig.write_html("refprop_scatter_plot.html")


if __name__ == "__main__":
    main()
