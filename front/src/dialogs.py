"""
Dialog components for parameter selection and data filtering
"""

import dash_bootstrap_components as dbc
from dash import dcc, html


def create_single_cells_dialog():
    """Dialog for single cell selection and visualization parameters"""

    return dbc.Card([
        dbc.CardHeader([
            html.I(className="fas fa-neuron me-2"),
            "Single Cell Selection"
        ]),
        dbc.CardBody([
            # Cell selector
            html.Label("Select Cells:", className="fw-bold"),
            dcc.Dropdown(
                id='cell-selector',
                options=[],
                multi=True,
                placeholder="Load data first...",
                disabled=True
            ),

            html.Hr(),

            # Plot type selector
            html.Label("Visualization Type:", className="fw-bold"),
            dcc.Dropdown(
                id='cell-plot-type',
                options=[
                    {'label': '📊 Raster Plot', 'value': 'raster'},
                    {'label': '📈 PSTH', 'value': 'psth'},
                    {'label': '🎯 Tuning Curve', 'value': 'tuning'},
                    {'label': '🗺️ Rate Map', 'value': 'ratemap'},
                    {'label': '📉 Waveform', 'value': 'waveform'},
                ],
                value='raster'
            ),

            html.Hr(),

            # Additional options (collapsible)
            dbc.Accordion([
                dbc.AccordionItem([
                    dbc.Row([
                        dbc.Col([
                            html.Label("Smoothing (ms):", className="small"),
                            dbc.Input(
                                id="cell-smoothing",
                                type="number",
                                value=50,
                                min=0,
                                step=10,
                                size="sm"
                            ),
                        ], width=6),
                        dbc.Col([
                            html.Label("Bin size (ms):", className="small"),
                            dbc.Input(
                                id="cell-binsize",
                                type="number",
                                value=10,
                                min=1,
                                step=1,
                                size="sm"
                            ),
                        ], width=6),
                    ])
                ], title="Plot Options", className="mb-2"),
            ], start_collapsed=True),

            # Update button
            dbc.Button(
                [html.I(className="fas fa-sync-alt me-2"), "Update Plot"],
                id="btn-update-cells",
                color="primary",
                className="w-100 mt-3",
                disabled=True
            ),
        ])
    ], className="h-100")


def create_decoding_dialog():
    """Dialog for decoding analysis selection and visualization"""

    return dbc.Card([
        dbc.CardHeader([
            html.I(className="fas fa-brain me-2"),
            "Decoding Analysis"
        ]),
        dbc.CardBody([
            # Decoder selector
            html.Label("Select Decoder:", className="fw-bold"),
            dcc.Dropdown(
                id='decoder-selector',
                options=[],
                placeholder="Run analysis first...",
                disabled=True
            ),

            html.Hr(),

            # Visualization type
            html.Label("Visualization:", className="fw-bold"),
            dcc.Dropdown(
                id='decoder-viz-type',
                options=[
                    {'label': '📊 Confusion Matrix', 'value': 'confusion'},
                    {'label': '📈 Performance Over Time', 'value': 'performance'},
                    {'label': '🎯 Decoded vs Actual', 'value': 'decoded'},
                    {'label': '📉 Error Distribution', 'value': 'errors'},
                ],
                value='confusion'
            ),

            html.Hr(),

            # Decoder info display
            html.Div(
                id="decoder-info",
                className="small text-muted"
            ),

            # Update button
            dbc.Button(
                [html.I(className="fas fa-sync-alt me-2"), "Update Plot"],
                id="btn-update-decoder",
                color="primary",
                className="w-100 mt-3",
                disabled=True
            ),
        ])
    ], className="h-100")


def create_behavior_dialog():
    """Dialog for behavioral data visualization"""

    return dbc.Card([
        dbc.CardHeader([
            html.I(className="fas fa-running me-2"),
            "Behavior Visualization"
        ]),
        dbc.CardBody([
            # Variable selector
            html.Label("Behavioral Variable:", className="fw-bold"),
            dcc.Dropdown(
                id='behavior-variable',
                options=[],
                placeholder="Load data first...",
                disabled=True
            ),

            html.Hr(),

            # Plot type
            html.Label("Plot Type:", className="fw-bold"),
            dcc.Dropdown(
                id='behavior-plot-type',
                options=[
                    {'label': '🗺️ Trajectory (2D)', 'value': 'trajectory'},
                    {'label': '📈 Time Series', 'value': 'timeseries'},
                    {'label': '📊 Distribution', 'value': 'distribution'},
                    {'label': '🔥 Heatmap', 'value': 'heatmap'},
                ],
                value='trajectory'
            ),

            html.Hr(),

            # Time range selector
            dbc.Accordion([
                dbc.AccordionItem([
                    html.Label("Time Range (s):", className="small mb-2"),
                    dcc.RangeSlider(
                        id='behavior-time-range',
                        min=0,
                        max=100,
                        step=1,
                        value=[0, 100],
                        marks=None,
                        tooltip={"placement": "bottom", "always_visible": True}
                    ),
                ], title="Time Selection", className="mb-2"),
            ], start_collapsed=True),

            # Update button
            dbc.Button(
                [html.I(className="fas fa-sync-alt me-2"), "Update Plot"],
                id="btn-update-behavior",
                color="primary",
                className="w-100 mt-3",
                disabled=True
            ),
        ])
    ], className="h-100")
