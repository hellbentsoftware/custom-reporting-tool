# application/view/dashboard.py

from dash import Dash, dcc, html, dash_table, Input, Output, State
from data_processing import generate_summary_table  # Function to process CSV
from flask import session, redirect
import logging

logger = logging.getLogger(__name__)

def create_dashboard(server):
    # Define unique blueprint name components
    dash_app_name = 'dashboard_app'

    # Check if the Dash assets blueprint is already registered
    assets_blueprint_name = f'_{dash_app_name}_dash_assets'
    if assets_blueprint_name in server.blueprints:
        logger.info("Dash app already registered, skipping creation.")
        return

    logger.info("Initializing Dash app...")

    # Initialize Dash app within Flask server with unique parameters
    dash_app = Dash(
        name=dash_app_name,
        server=server,
        routes_pathname_prefix='/dashboard/',
        assets_url_path='/dashboard/assets',  # Ensure unique assets path
        suppress_callback_exceptions=True
    )

    # Define the layout of the Dash app
    dash_app.layout = html.Div([
        html.H1("Sales Data Summary", style={'text-align': 'center'}),
        html.Div(
            dcc.Upload(
                id='upload-data',
                children=html.Button('Upload CSV', style={'background-color': '#4CAF50', 'color': 'white'}),
                multiple=False
            ),
            style={'text-align': 'center', 'padding-top': '20px'}
        ),
        html.Div(id='table-container', style={'padding-top': '20px'})
    ])

    # Callback to update the table based on uploaded CSV
    @dash_app.callback(
        Output('table-container', 'children'),
        [Input('upload-data', 'contents')],
        [State('upload-data', 'filename')]
    )
    def update_table(contents, filename):
        if contents is None:
            return html.Div("Please upload a CSV file.")

        try:
            # Process the uploaded file and generate summary table
            summary_table = generate_summary_table(contents)

            # Display the summary table using dash_table.DataTable
            table_columns = [{"name": col, "id": col} for col in summary_table.columns]
            table = dash_table.DataTable(
                columns=table_columns,
                data=summary_table.to_dict('records'),
                style_table={'overflowX': 'auto'},
                style_cell={
                    'textAlign': 'left',
                    'padding': '10px',
                    'font-family': 'Arial, sans-serif'
                }
            )

            return table
        except Exception as e:
            logger.error(f"Error processing CSV file {filename}: {e}")
            return html.Div("There was an error processing your file.")

    logger.info("Dash app initialized successfully.")

    return dash_app
