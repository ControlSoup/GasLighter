import numpy as np
import plotly.graph_objects as go
from tqdm import tqdm

from ..integration import np_rk4
from ..units import convert

"""
Source: https://www-udc.ig.utexas.edu/external/becker/teaching/557/problem_sets/problem_set_fd_explicit.pdf
Source 2: https://en.wikipedia.org/wiki/Numerical_solution_of_the_convection%E2%80%93diffusion_equation
"""


def conduction_fdm_dT_dt(
    diffusivity: float,
    next_node_t: float,
    current_node_t: float,
    last_node_t: float,
    dx: float,
):
    """Discreteized 1D Conduction Heat equation"""
    heat_comp = next_node_t - (2 * current_node_t) + last_node_t

    return diffusivity * heat_comp / dx**2


def plot_fdm_solution(
    diffusivity: float,
    start_t: float,
    end_t: float,
    nodes: int,
    distance: float,
    max_time: float,
    dt: float = None,
    export_path=None,
    imperial_results=True,
):

    print("___ Starting FDM Solution ___")
    """1D Heat Transfer solution, assuming all notes start at end condition temp"""
    dx = distance / nodes

    print(f"FDM Dx: {dx}")
    # Stability estimate
    if dt is None:
        dt = dx**2 / (2 * diffusivity)
        print(f"FDM Dt: {dt}")

    d = np.arange(0, distance, dx)
    time = np.arange(0, max_time, dt)
    temps = np.zeros_like(d) + end_t

    temp_history = np.zeros((len(time), len(d)))

    # Boundary conditions
    temps[0] = start_t

    max_boundary = max(temps)
    min_boundary = min(temps)

    for i, _ in tqdm(enumerate(time), total=len(time)):

        if i == 0:
            temp_history[i] = temps
            continue

        for j, _ in enumerate(temps):

            if j == 0:
                continue

            if j == len(temps) - 1:
                next = temps[j]
            else:
                next = temps[j + 1]

            current = temps[j]
            last = temps[j-1]

            dTdt = conduction_fdm_dT_dt(
                diffusivity, next, current, last, dx
            )
            new_t = np_rk4([dTdt, temps[j]], dt)

            if new_t > max_boundary:
                raise ValueError(
                    f"Calcualted Temp: {new_t} > Max Boundary: {max_boundary} at t = {time[i]}"
                )

            if new_t < min_boundary:
                raise ValueError(
                    f"Calcualted Temp: {new_t} > Max Boundary: {max_boundary} at t = {time[i]}"
                )

            temps[j] = new_t

        temp_history[i] = temps

    try:
        temp_history = temp_history[:: int(max_time / (dt * 20))]
        time = time[:: int(max_time / (dt * 20))]
    except ValueError:
        pass

    overall_min_temp = np.min(temp_history)
    overall_max_temp = np.max(temp_history)

    if imperial_results:
        temp_history = convert(temp_history, "degK", "degF")
        d = convert(d, "m", "in")
        overall_min_temp = convert(overall_min_temp, "degK", "degF")
        overall_max_temp = convert(overall_max_temp, "degK", "degF")
        fig_title = "Imperial Temperature [degF] vs Distance [in]"
    else:
        fig_title = "SI Temperature [degK] vs Distance [m]"

    fig = go.Figure()

    fig.add_trace(
        go.Heatmap(
            z=temp_history[0],
            y=[time[0]] * len(d),
            x=d,
            colorscale="Viridis",
            zmin=overall_min_temp,
            zmax=overall_max_temp
        )
    )

    fig.update_layout(
        title=fig_title,
        xaxis_title="Distance",
        yaxis=dict(showticklabels=False),
        sliders=[
            {
                "active": 0,
                "steps": [
                    {
                        "label": f"Time: {t}",
                        "method": "update",
                        "args": [
                            {"z": [temp_history[i]]},
                            {"title": f"Temperature vs Distance - Time: {t}"},
                        ],
                    }
                    for i, t in enumerate(time)
                ],
                "pad": {"t": 50},
                "currentvalue": {"visible": True, "prefix": "Time: "},
                "transition": {"duration": 300, "easing": "cubic-in-out"},
            }
        ],
    )

    if export_path is not None:
        fig.write_html(export_path)

    fig.show()