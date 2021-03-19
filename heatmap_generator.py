"""TODO..."""

import json

import plotly.graph_objects as go
from plotly.subplots import make_subplots


def get_color_scale():
    """TODO..."""
    ret = [
        [0, "#fc8d59"],
        [1/2, "#ffffbf"],
        [1, "#91bfdb"]
    ]
    return ret


def get_heatmap_center_fig(data):
    """TODO..."""
    ret = make_subplots(
        rows=2,
        cols=1,
        row_heights=[0.1, 0.9],
        vertical_spacing=0.05
    )

    heatmap_center_genes_obj = get_heatmap_center_genes_obj(data)
    ret.add_trace(heatmap_center_genes_obj, row=1, col=1)
    midpoints = []
    endpoints = heatmap_center_genes_obj["x"]
    for i, val in enumerate(endpoints[:-1]):
        midpoint = ((endpoints[i+1] - endpoints[i]) / 2) + endpoints[i]
        midpoints.append(midpoint)
    for i, gene_label in enumerate(heatmap_center_genes_obj["text"][0]):
        x_start = heatmap_center_genes_obj["x"][i]
        x_end = heatmap_center_genes_obj["x"][i+1]
        if (x_end - x_start) < 2:
            continue
        ret.add_annotation(
            xref="x1",
            yref="y1",
            x=midpoints[i],
            y=heatmap_center_genes_obj["y"][0],
            text=gene_label,
            showarrow=False,
            font={"color": "white"}
        )

    heatmap_center_base_obj = get_heatmap_center_base_obj(data)
    ret.add_trace(heatmap_center_base_obj, row=2, col=1)

    for y, _ in enumerate(heatmap_center_base_obj["y"]):
        ret.add_shape({
            "type": "line",
            "xref": "x2",
            "yref": "y2",
            "x0": -0.5,
            "x1": len(heatmap_center_base_obj["x"]) - 0.5,
            "y0": y-0.5,
            "y1": y-0.5
        })

    heatmap_center_insertions_object = get_heatmap_center_insertions_obj(data)
    ret.add_trace(heatmap_center_insertions_object, row=2, col=1)

    heatmap_center_deletions_object = get_heatmap_center_deletions_obj(data)
    ret.add_trace(heatmap_center_deletions_object, row=2, col=1)

    ret.update_layout(xaxis1_visible=False)
    ret.update_layout(xaxis2_type="category")
    ret.update_xaxes(range=[-0.5, len(data["heatmap_x"]) - 0.5])
    ret.update_yaxes(visible=False)
    ret.update_layout(font={
        "size": 18
    })
    ret.update_layout(width=len(data["heatmap_x"]) * 25, autosize=False)
    ret.update_layout(plot_bgcolor="white")
    ret.update_layout(margin={
        "l": 0,
        "r": 0,
        "t": 0,
        "pad": 0
    })

    return ret


def get_heatmap_center_genes_obj(data):
    """TODO..."""
    heatmap_center_genes_obj_x = []
    heatmap_center_genes_obj_labels = []
    last_gene_seen = ""
    for i, heatmap_x_gene in enumerate(data["heatmap_x_genes"]):
        if i == 0:
            heatmap_center_genes_obj_x.append(i-0.5)
            last_gene_seen = heatmap_x_gene
        elif i == (len(data["heatmap_x_genes"]) - 1):
            heatmap_center_genes_obj_x.append(i+0.5)
            heatmap_center_genes_obj_labels.append(last_gene_seen)
        elif heatmap_x_gene != last_gene_seen:
            heatmap_center_genes_obj_x.append(i-0.5)
            heatmap_center_genes_obj_labels.append(last_gene_seen)
            last_gene_seen = heatmap_x_gene

    heatmap_center_genes_obj_z = [[]]
    heatmap_center_genes_obj_colorscale = []
    with open("gene_colors.json") as fp:
        gene_colors = json.load(fp)
    for i, label in enumerate(heatmap_center_genes_obj_labels):
        mock_z_val = i / (len(heatmap_center_genes_obj_labels) - 1)
        heatmap_center_genes_obj_z[0].append(mock_z_val)
        heatmap_center_genes_obj_colorscale.append(gene_colors[label])

    ret = go.Heatmap(
        x=heatmap_center_genes_obj_x,
        y=[1],
        z=heatmap_center_genes_obj_z,
        hoverinfo="skip",
        text=[heatmap_center_genes_obj_labels],
        showscale=False,
        colorscale=heatmap_center_genes_obj_colorscale
    )

    return ret


def get_heatmap_center_base_obj(data):
    """TODO..."""
    ret = go.Heatmap(
        x=data["heatmap_x"],
        y=data["heatmap_y"],
        z=data["heatmap_z"],
        colorscale=get_color_scale(),
        zmin=0,
        zmax=1,
        hoverlabel={
            "font_size": 18
        },
        hoverongaps=False,
        hovertemplate="%{text}<extra></extra>",
        text=data["heatmap_cell_text"],
        xgap=10,
        ygap=10,
        showscale=False
    )
    return ret


def get_heatmap_center_insertions_obj(data):
    """TODO..."""
    ret = go.Scatter(
        x=data["insertions_x"],
        y=data["insertions_y"],
        hoverinfo="skip",
        mode="markers",
        marker={
            "color": "lime",
            "size": 18,
            "symbol": "cross",
            "line": {"width": 2}
        },
        showlegend=False
    )
    return ret


def get_heatmap_center_deletions_obj(data):
    """TODO..."""
    ret = go.Scatter(
        x=data["deletions_x"],
        y=data["deletions_y"],
        hoverinfo="skip",
        mode="markers",
        marker={
            "color": "red",
            "size": 18,
            "symbol": "x",
            "line": {"width": 2}
        },
        showlegend=False
    )
    return ret


def get_heatmap_left_fig(data):
    """TODO..."""
    ret = make_subplots(
        rows=2,
        cols=1,
        row_heights=[0.1, 0.9],
        vertical_spacing=0.05
    )

    heatmap_left_base_obj = get_heatmap_left_base_obj(data)
    heatmap_left_labels_obj = get_heatmap_left_labels_obj(data)

    ret.add_trace(heatmap_left_base_obj, row=2, col=1)
    ret.add_trace(heatmap_left_labels_obj, row=2, col=1)

    ret.update_layout(font={"size": 18})
    ret.update_layout(margin={
        "l": 0,
        "r": 0,
        "t": 0
    })
    ret.update_layout(plot_bgcolor="white")
    ret.update_xaxes(visible=False)
    ret.update_yaxes(visible=False)

    return ret


def get_heatmap_left_base_obj(data):
    """TODO..."""
    """TODO..."""
    ret = go.Heatmap(
        x=[1],
        y=data["heatmap_y"],
        z=[[1] for _ in data["heatmap_y"]],
        showscale=False,
        hoverinfo="none",
        colorscale="Greys",
        zmin=0,
        zmax=1
    )
    return ret


def get_heatmap_left_labels_obj(data):
    """TODO..."""
    ret = go.Scatter(
        y=data["heatmap_y"],
        x=[0 for _ in data["heatmap_y"]],
        hoverinfo="skip",
        mode="markers+text",
        marker={
            "color": "white",
            "size": 1
        },
        text=data["heatmap_y"],
        textposition="middle center"
    )
    return ret


def get_heatmap_right_fig(data):
    """TODO..."""
    ret = make_subplots(
        rows=2,
        cols=1,
        row_heights=[0.1, 0.9],
        vertical_spacing=0.05
    )

    heatmap_right_base_obj = get_heatmap_right_base_obj(data)

    ret.add_trace(heatmap_right_base_obj, row=2, col=1)
    ret.update_layout(font={"size": 18})
    ret.update_layout(plot_bgcolor="white")
    ret.update_xaxes(visible=False)
    ret.update_yaxes(visible=False)
    ret.update_layout(margin={
        "l": 0,
        "r": 0,
        "t": 0
    })
    return ret


def get_heatmap_right_base_obj(data):
    """TODO..."""
    ret = go.Heatmap(
        x=["foo"],
        y=data["heatmap_y"],
        z=[[0] for _ in data["heatmap_y"]],
        colorscale=get_color_scale(),
        colorbar={
            "x": -2,
            "y": 0.4
        },
        zmin=0,
        zmax=1,
        hoverinfo="none"
    )
    return ret
