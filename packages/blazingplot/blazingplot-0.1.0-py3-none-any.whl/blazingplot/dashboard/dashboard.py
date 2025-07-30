"""
Dashboard module for BlazingPlot.

This module provides the main Dashboard class that serves as the entry point
for creating interactive data visualizations in both Jupyter notebooks and
standalone web applications.
"""

import polars as pl
import plotly.io as pio
import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
from IPython.display import display, HTML
import matplotlib.pyplot as plt
import uuid
from typing import Optional, Dict, List, Any, Union

from blazingplot.visualizations.base import BaseVisualization


class Dashboard:
    """
    Main dashboard class for BlazingPlot.
    
    This class provides a unified interface for creating interactive dashboards
    in both Jupyter notebooks and as standalone web applications.
    
    Parameters
    ----------
    data : polars.DataFrame
        The main data source for the dashboard.
    figsize : tuple, optional
        Default dashboard size as (width, height) in pixels.
    title : str, optional
        Dashboard title displayed in the header.
    custom_palette : list or str, optional
        A Matplotlib-compatible color palette.
    """
    
    def __init__(
        self,
        data: pl.DataFrame,
        figsize: tuple = (1200, 800),
        title: str = "BlazingPlot Dashboard",
        custom_palette: Optional[Union[List[str], str]] = None
    ):
        if not isinstance(data, pl.DataFrame):
            raise TypeError("Data must be a polars DataFrame")
        
        self.data = data
        self.figsize = figsize
        self.title = title
        self.id = str(uuid.uuid4())[:8]  # Generate a unique ID for this dashboard
        
        # Set up color palettes
        self.palettes = {
            "pastel": plt.cm.Pastel1.colors,
            "viridis": plt.cm.viridis.colors,
            "plasma": plt.cm.plasma.colors,
            "inferno": plt.cm.inferno.colors,
            "magma": plt.cm.magma.colors,
        }
        
        self.current_palette = "pastel"
        if custom_palette:
            if isinstance(custom_palette, str):
                if custom_palette in plt.colormaps():
                    cmap = plt.get_cmap(custom_palette)
                    self.palettes["custom"] = [cmap(i) for i in range(10)]
                    self.current_palette = "custom"
            elif isinstance(custom_palette, list):
                self.palettes["custom"] = custom_palette
                self.current_palette = "custom"
        
        # Initialize visualization container
        self.current_viz = None
        self.app = None
        self._init_app()
    
    def _init_app(self):
        """Initialize the Dash application."""
        self.app = dash.Dash(
            __name__,
            external_stylesheets=[dbc.themes.BOOTSTRAP],
            suppress_callback_exceptions=True
        )
        
        # Set up the layout
        self.app.layout = self._create_layout()
        
        # Register callbacks
        self._register_callbacks()
    
    def _create_layout(self):
        """Create the dashboard layout."""
        # Header
        header = dbc.Row([
            # Left: Title
            dbc.Col(html.H1(self.title), width=4),
            
            # Center: Palette selector
            dbc.Col([
                html.Label("Color Palette:"),
                dcc.Dropdown(
                    id=f"palette-dropdown-{self.id}",
                    options=[{"label": k.capitalize(), "value": k} for k in self.palettes.keys()],
                    value=self.current_palette,
                    clearable=False
                )
            ], width=4),
            
            # Right: Export buttons
            dbc.Col([
                dbc.ButtonGroup([
                    dbc.Button("Export PNG", id=f"export-png-{self.id}", color="primary", className="me-1"),
                    dbc.Button("Export HTML", id=f"export-html-{self.id}", color="primary", className="me-1"),
                    dbc.Button("Export CSV", id=f"export-csv-{self.id}", color="primary")
                ])
            ], width=4, className="d-flex justify-content-end")
        ], className="mb-4")
        
        # Main body
        main_body = dbc.Row([
            # Left: Column selector
            dbc.Col([
                html.H4("Columns"),
                html.Div(
                    [
                        dbc.Checklist(
                            id=f"column-selector-{self.id}",
                            options=[{"label": col, "value": col} for col in self.data.columns],
                            value=self.data.columns[:2].to_list(),  # Default select first two columns
                            inline=False
                        )
                    ],
                    style={"maxHeight": "600px", "overflowY": "auto"}
                )
            ], width=2, className="border-end"),
            
            # Center: Visualization controls
            dbc.Col([
                html.H4("Controls"),
                # Visualization type selector
                html.Div([
                    html.Label("Visualization Type:"),
                    dcc.Dropdown(
                        id=f"viz-type-{self.id}",
                        options=[
                            {"label": "Scatter Plot", "value": "scatter"},
                            {"label": "Line Chart", "value": "line"},
                            {"label": "Bar Chart", "value": "bar"},
                            {"label": "Bubble Chart", "value": "bubble"},
                            {"label": "Pie Chart", "value": "pie"},
                            {"label": "Box Plot", "value": "box"},
                            {"label": "Histogram", "value": "histogram"},
                            {"label": "2D Histogram", "value": "histogram2d"},
                            {"label": "Time Series", "value": "timeseries"},
                            {"label": "Stock Chart", "value": "stock"},
                            {"label": "Error Bars", "value": "error"},
                            {"label": "Bubble Map", "value": "bubblemap"},
                            {"label": "Tile Choropleth", "value": "choropleth"},
                            {"label": "Line on Tiles", "value": "mapline"},
                            {"label": "Filled Area", "value": "area"},
                            {"label": "Simple Table", "value": "table"},
                            {"label": "Pivot Table", "value": "pivot"}
                        ],
                        value="scatter",  # Default visualization
                        clearable=False
                    )
                ], className="mb-3"),
                
                # Dynamic controls container
                html.Div(id=f"dynamic-controls-{self.id}"),
                
                # Update button
                html.Div([
                    dbc.Button(
                        "Update Visualization",
                        id=f"update-viz-{self.id}",
                        color="success",
                        className="mt-3 w-100"
                    )
                ])
            ], width=3, className="border-end"),
            
            # Right: Visualization display
            dbc.Col([
                html.Div([
                    html.Div([
                        html.Button(
                            "⛶",  # Fullscreen icon
                            id=f"fullscreen-{self.id}",
                            className="btn btn-sm btn-outline-secondary position-absolute top-0 end-0 m-2"
                        ),
                        dcc.Dropdown(
                            id=f"chart-elements-{self.id}",
                            multi=True,
                            placeholder="Toggle chart elements...",
                            className="position-absolute top-0 end-5 m-2",
                            style={"width": "200px"}
                        )
                    ], className="position-relative"),
                    dcc.Loading(
                        id=f"loading-{self.id}",
                        type="circle",
                        children=dcc.Graph(
                            id=f"main-chart-{self.id}",
                            style={"height": f"{self.figsize[1]-100}px"}
                        )
                    )
                ])
            ], width=7)
        ])
        
        return dbc.Container([header, main_body], fluid=True)
    
    def _register_callbacks(self):
        """Register all the necessary Dash callbacks."""
        # Callback to update dynamic controls based on visualization type
        @self.app.callback(
            Output(f"dynamic-controls-{self.id}", "children"),
            Input(f"viz-type-{self.id}", "value"),
            Input(f"column-selector-{self.id}", "value")
        )
        def update_dynamic_controls(viz_type, selected_columns):
            # This will be implemented to generate controls specific to each visualization type
            # For now, return a placeholder
            return html.Div([
                html.Label("X Axis:"),
                dcc.Dropdown(
                    id=f"x-axis-{self.id}",
                    options=[{"label": col, "value": col} for col in selected_columns],
                    value=selected_columns[0] if selected_columns else None
                ),
                html.Label("Y Axis:"),
                dcc.Dropdown(
                    id=f"y-axis-{self.id}",
                    options=[{"label": col, "value": col} for col in selected_columns],
                    value=selected_columns[1] if len(selected_columns) > 1 else None
                )
            ])
        
        # Callback to update the visualization
        @self.app.callback(
            Output(f"main-chart-{self.id}", "figure"),
            Input(f"update-viz-{self.id}", "n_clicks"),
            State(f"viz-type-{self.id}", "value"),
            State(f"x-axis-{self.id}", "value"),
            State(f"y-axis-{self.id}", "value"),
            State(f"palette-dropdown-{self.id}", "value")
        )
        def update_visualization(n_clicks, viz_type, x_axis, y_axis, palette):
            # This will be implemented to create and update visualizations
            # For now, return a placeholder figure
            import plotly.express as px
            
            if not n_clicks:
                # Initial load, show a table view
                return px.scatter(
                    self.data.head(100).to_pandas(),
                    x=self.data.columns[0],
                    y=self.data.columns[1] if len(self.data.columns) > 1 else self.data.columns[0],
                    title="Initial View - Click Update to Refresh"
                )
            
            if viz_type == "scatter":
                return px.scatter(
                    self.data.to_pandas(),
                    x=x_axis,
                    y=y_axis,
                    title=f"Scatter Plot: {x_axis} vs {y_axis}",
                    color_discrete_sequence=list(self.palettes[palette])
                )
            
            # More visualization types will be implemented
            return px.scatter(
                self.data.to_pandas(),
                x=x_axis,
                y=y_axis,
                title=f"Placeholder for {viz_type}"
            )
    
    def run(self, mode="jupyter", port=8050, debug=False):
        """
        Run the dashboard.
        
        Parameters
        ----------
        mode : str, optional
            The mode to run the dashboard in. Options are:
            - 'jupyter': Run in a Jupyter notebook
            - 'standalone': Run as a standalone web application
        port : int, optional
            The port to run the standalone application on.
        debug : bool, optional
            Whether to run in debug mode.
            
        Returns
        -------
        None
        """
        if mode == "jupyter":
            # For Jupyter notebooks, use JupyterDash
            try:
                from jupyter_dash import JupyterDash
                app = JupyterDash(__name__)
                app.layout = self.app.layout
                
                # Copy callbacks
                for callback in self.app.callback_map:
                    app.callback_map[callback] = self.app.callback_map[callback]
                
                app.run_server(mode="inline", port=port, debug=debug)
            except ImportError:
                # Fallback if jupyter_dash is not available
                iframe_html = f"""
                <iframe
                    src="http://localhost:{port}"
                    width="{self.figsize[0]}"
                    height="{self.figsize[1]}"
                    style="border:none;"
                ></iframe>
                """
                display(HTML(iframe_html))
                self.app.run_server(port=port, debug=debug)
        else:
            # For standalone mode
            self.app.run_server(port=port, debug=debug)
    
    def to_html(self, filename=None):
        """
        Export the current visualization to HTML.
        
        Parameters
        ----------
        filename : str, optional
            The filename to save the HTML to. If None, returns the HTML as a string.
            
        Returns
        -------
        str or None
            The HTML as a string if filename is None, otherwise None.
        """
        if self.current_viz:
            html_content = self.current_viz.export_html()
            if filename:
                with open(filename, 'w') as f:
                    f.write(html_content)
            else:
                return html_content
        return None
    
    def to_png(self, filename=None):
        """
        Export the current visualization to PNG.
        
        Parameters
        ----------
        filename : str, optional
            The filename to save the PNG to. If None, returns the PNG as bytes.
            
        Returns
        -------
        bytes or None
            The PNG as bytes if filename is None, otherwise None.
        """
        if self.current_viz:
            return self.current_viz.export_png(filename)
        return None
    
    def to_csv(self, filename=None):
        """
        Export the current data to CSV.
        
        Parameters
        ----------
        filename : str, optional
            The filename to save the CSV to. If None, returns the CSV as a string.
            
        Returns
        -------
        str or None
            The CSV as a string if filename is None, otherwise None.
        """
        if filename:
            self.data.write_csv(filename)
        else:
            return self.data.write_csv()
