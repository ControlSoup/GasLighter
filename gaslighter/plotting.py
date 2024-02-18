from __future__ import annotations
import numpy as np
import plotly.graph_objects as go

# TODO Add titles
# TODO Implement plottly yaml?
def graph_by_key(
    datadict: dict[str,list],
    key_list: list[str],
    x_key: str,
    title: str,
    export_path: bool = None,
    show_fig = True,
    fig = None
):
    if fig == None:
        fig = go.Figure()

    for y_key in key_list:
        fig.add_trace(
            go.Scatter(
                x=datadict[x_key],
                y=datadict[y_key],
                name=y_key,
                mode="lines"
            )
        )
    fig.update_layout(
        title = title,
        xaxis_title = x_key
    )

    if export_path:
        fig.write_html(export_path)

    if show_fig:
        fig.show()


def graph_datadict(
    datadict: str,
    x_key: str,
    title: str,
    export_path: str = None,
    show_fig = True,
    fig = None
):
    key_list = [key for key in datadict]

    graph_by_key(
        datadict=datadict,
        key_list=key_list,
        x_key=x_key,
        title=title,
        export_path=export_path,
        show_fig=show_fig,
        fig=fig
    )

def graph_countour(
    x_str, x_data,
    y_str, y_data,
    z_str, z_fn: function | list[list,list],
    title: str = "" ,
    export_path: bool = None,
    show_fig = True,
    fig = None,
):
    if fig is None:
        fig = go.Figure()

    if callable(z_fn):
        row = []
        for _y in y_data:
            col = []
            for _x in x_data:
                col.append(z_fn(_x, _y))
            row.append(col)
        z_data = np.array(row)
    else:
        raise ValueError("ERROR| z_fn must be callable with format fn(x,y)")

    fig.add_trace(go.Surface(z = z_data, x = x_data, y = y_data))
    fig.update_layout(
        title=title,
        scene=dict(
            xaxis_title=x_str,
            yaxis_title=y_str,
            zaxis_title=z_str
        )
    )

    if export_path:
        fig.write_html(export_path)

    if show_fig:
        fig.show()