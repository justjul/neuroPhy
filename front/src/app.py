
"""
neuroPhy Dash GUI - Main Application

Interactive web interface for neurophysiological data analysis
"""

import dash
import dash_bootstrap_components as dbc
from config import API_URL, FRONTEND_DEBUG, FRONTEND_HOST, FRONTEND_PORT
from dash import dcc, html
from layout import create_layout

# Initialize the Dash app with Bootstrap theme
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME],
    suppress_callback_exceptions=True,
    title="neuroPhy Analysis"
)

# Set layout
app.layout = create_layout()

# Server for deployment
server = app.server


def main():
    """Run the Dash server"""
    app.run(
        debug=FRONTEND_DEBUG,
        host=FRONTEND_HOST,
        port=FRONTEND_PORT
    )


if __name__ == "__main__":
    main()
