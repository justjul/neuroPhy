"""
neuroPhy Layout - Main UI structure

Defines the overall layout including navbar, tabs, and page content
"""

import dash_bootstrap_components as dbc
from dash import dcc, html
from dialogs import (
    create_behavior_dialog,
    create_decoding_dialog,
    create_single_cells_dialog,
)
from navbar import create_navbar


def create_layout():
    """Create the main application layout"""

    return html.Div([
        # Store components for app state (client-side storage)
        dcc.Store(id='session-store', storage_type='session'),
        dcc.Store(id='exp-data-store', storage_type='session'),

        # Modals
        create_load_session_modal(),
        create_analysis_modal(),

        # Navigation bar
        create_navbar(),

        # Main content container
        dbc.Container([
            # Status bar
            dbc.Row([
                dbc.Col([
                    html.Div(
                        id='status-bar',
                        children=[
                            html.I(className="fas fa-circle text-secondary me-2"),
                            html.Small("No data loaded",
                                       className="text-muted")
                        ],
                        className="p-2 border-bottom"
                    )
                ])
            ]),

            # Main tabs
            dbc.Row([
                dbc.Col([
                    dbc.Tabs(
                        id="main-tabs",
                        active_tab="tab-cells",
                        children=[
                            # Single Cells Tab
                            dbc.Tab(
                                label="Single Cells",
                                tab_id="tab-cells",
                                children=[
                                    create_tab_content(
                                        dialog=create_single_cells_dialog(),
                                        plot_id="plot-single-cells"
                                    )
                                ]
                            ),

                            # Decoding Tab
                            dbc.Tab(
                                label="Decoding",
                                tab_id="tab-decoding",
                                children=[
                                    create_tab_content(
                                        dialog=create_decoding_dialog(),
                                        plot_id="plot-decoding"
                                    )
                                ]
                            ),

                            # Behavior Tab
                            dbc.Tab(
                                label="Behavior",
                                tab_id="tab-behavior",
                                children=[
                                    create_tab_content(
                                        dialog=create_behavior_dialog(),
                                        plot_id="plot-behavior"
                                    )
                                ]
                            ),
                        ]
                    )
                ], width=12)
            ], className="mt-3")
        ], fluid=True)
    ])


def create_tab_content(dialog, plot_id):
    """
    Create content for a tab with dialog on left and plot on right

    Args:
        dialog: Dialog component for parameters
        plot_id: ID for the plot graph component
    """
    return dbc.Row([
        # Left side: Dialog
        dbc.Col(
            dialog,
            width=3,
            className="border-end"
        ),

        # Right side: Plot
        dbc.Col(
            dcc.Loading(
                id=f"loading-{plot_id}",
                type="default",
                children=[
                    dcc.Graph(
                        id=plot_id,
                        config={
                            'displayModeBar': True,
                            'displaylogo': False,
                            'toImageButtonOptions': {
                                'format': 'svg',
                                'filename': 'neurophy_plot'
                            }
                        },
                        style={'height': '85vh'}
                    )
                ]
            ),
            width=9
        )
    ], className="g-0")


def create_load_session_modal():
    """Modal for loading session data"""
    return dbc.Modal([
        dbc.ModalHeader(
            dbc.ModalTitle("Load Session"),
            close_button=True
        ),
        dbc.ModalBody([
            dbc.Row([
                dbc.Col([
                    dbc.Label("Project Directory",
                              html_for="input-project-dir"),
                    dbc.Input(
                        id="input-project-dir",
                        placeholder="/path/to/project",
                        type="text"
                    ),
                ], width=12)
            ], className="mb-3"),

            dbc.Row([
                dbc.Col([
                    dbc.Label("Animal ID", html_for="input-animal"),
                    dbc.Input(
                        id="input-animal",
                        placeholder="e.g., m1, rat01",
                        type="text"
                    ),
                ], width=4),

                dbc.Col([
                    dbc.Label("Series", html_for="input-series"),
                    dbc.Input(
                        id="input-series",
                        placeholder="e.g., 1",
                        type="text"
                    ),
                ], width=4),

                dbc.Col([
                    dbc.Label("Experiment", html_for="input-exp"),
                    dbc.Input(
                        id="input-exp",
                        placeholder="e.g., 1",
                        type="text"
                    ),
                ], width=4),
            ]),

            html.Div(
                id="load-error-message",
                className="mt-3"
            )
        ]),
        dbc.ModalFooter([
            dbc.Button(
                "Cancel",
                id="btn-cancel-load",
                color="secondary",
                className="me-2"
            ),
            dbc.Button(
                "Load",
                id="btn-confirm-load",
                color="primary"
            ),
        ]),
    ], id="modal-load-session", is_open=False, size="lg")


def create_analysis_modal():
    """Modal for running analyses"""
    return dbc.Modal([
        dbc.ModalHeader(
            dbc.ModalTitle("Run Analysis"),
            close_button=True
        ),
        dbc.ModalBody([
            dbc.Label("Select Analysis Type"),
            dcc.Dropdown(
                id="dropdown-analysis-type",
                options=[
                    {"label": "Compute Maps", "value": "maps"},
                    {"label": "Run GLMs", "value": "glm"},
                    {"label": "Run Decoders", "value": "decoders"},
                    {"label": "Custom Analysis", "value": "custom"},
                ],
                placeholder="Choose analysis..."
            ),

            html.Div(
                id="analysis-options",
                className="mt-3"
            ),

            html.Div(
                id="analysis-status-message",
                className="mt-3"
            )
        ]),
        dbc.ModalFooter([
            dbc.Button(
                "Cancel",
                id="btn-cancel-analysis",
                color="secondary",
                className="me-2"
            ),
            dbc.Button(
                "Run",
                id="btn-run-analysis",
                color="primary"
            ),
        ]),
    ], id="modal-analysis", is_open=False, size="lg")
