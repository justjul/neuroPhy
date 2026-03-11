"""
Navigation bar component
"""

import dash_bootstrap_components as dbc
from dash import html


def create_navbar():
    """Create the top navigation bar with menus"""

    return dbc.Navbar(
        dbc.Container([
            # Navbar items
            dbc.Nav([
                # File Menu
                dbc.DropdownMenu(
                    children=[
                        dbc.DropdownMenuItem(
                            [html.I(className="fas fa-folder-open me-2"),
                             "Load Session"],
                            id="menu-load-session"
                        ),
                        dbc.DropdownMenuItem(
                            [html.I(className="fas fa-save me-2"),
                             "Save Session"],
                            id="menu-save-session"
                        ),
                        dbc.DropdownMenuItem(divider=True),
                        dbc.DropdownMenuItem(
                            [html.I(className="fas fa-file-import me-2"),
                             "Load Parameters"],
                            id="menu-load-params"
                        ),
                        dbc.DropdownMenuItem(
                            [html.I(className="fas fa-file-export me-2"),
                             "Save Parameters"],
                            id="menu-save-params"
                        ),
                        dbc.DropdownMenuItem(divider=True),
                        dbc.DropdownMenuItem(
                            [html.I(className="fas fa-tasks me-2"),
                             "Run Batch"],
                            id="menu-run-batch",
                            disabled=True  # TODO: Implement
                        ),
                    ],
                    nav=True,
                    in_navbar=True,
                    label="File",
                    className="ms-2"
                ),

                # Analysis Menu
                dbc.DropdownMenu(
                    children=[
                        dbc.DropdownMenuItem(
                            [html.I(className="fas fa-map me-2"),
                             "Compute Maps"],
                            id="menu-compute-maps"
                        ),
                        dbc.DropdownMenuItem(
                            [html.I(className="fas fa-chart-line me-2"),
                             "Run GLMs"],
                            id="menu-run-glms"
                        ),
                        dbc.DropdownMenuItem(
                            [html.I(className="fas fa-brain me-2"),
                             "Run Decoders"],
                            id="menu-run-decoders"
                        ),
                        dbc.DropdownMenuItem(divider=True),
                        dbc.DropdownMenuItem(
                            [html.I(className="fas fa-code me-2"),
                             "Custom Analysis"],
                            id="menu-custom-analysis"
                        ),
                    ],
                    nav=True,
                    in_navbar=True,
                    label="Analysis",
                ),

                # Options Menu (for future use)
                dbc.DropdownMenu(
                    children=[
                        dbc.DropdownMenuItem(
                            [html.I(className="fas fa-cog me-2"),
                             "Analysis Settings"],
                            id="menu-analysis-settings",
                            disabled=True
                        ),
                        dbc.DropdownMenuItem(
                            [html.I(className="fas fa-palette me-2"),
                             "Plot Settings"],
                            id="menu-plot-settings",
                            disabled=True
                        ),
                    ],
                    nav=True,
                    in_navbar=True,
                    label="Options",
                ),

                # Help Menu
                dbc.DropdownMenu(
                    children=[
                        dbc.DropdownMenuItem(
                            [html.I(className="fas fa-book me-2"),
                             "Documentation"],
                            href="https://github.com/justjul/neuroPhy",
                            target="_blank"
                        ),
                        dbc.DropdownMenuItem(
                            [html.I(className="fas fa-info-circle me-2"), "About"],
                            id="menu-about"
                        ),
                    ],
                    nav=True,
                    in_navbar=True,
                    label="Help",
                ),
            ], navbar=True),

            # Brand/Logo
            dbc.Row([
                dbc.Col([
                    html.Div([
                        html.I(className="fas fa-brain me-2"),
                        dbc.NavbarBrand("neuroPhy", className="ms-2"),
                    ], className="d-flex align-items-center")
                ])
            ], className="g-0 flex-nowrap"),

        ], fluid=True),
        color="black",
        dark=True,
        className="mb-3"
    )
