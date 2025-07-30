"""
Dashboard layout and controls module for BlazingPlot.

This module provides the components for creating the dashboard layout
and interactive controls for the BlazingPlot dashboard.
"""

import dash
from dash import dcc, html, Input, Output, State, callback_context
import dash_bootstrap_components as dbc
import plotly.express as px
import polars as pl
from typing import Dict, List, Optional, Any, Union

from blazingplot.visualizations.base import BaseVisualization


class DashboardControls:
    """
    Class for generating dynamic dashboard controls based on visualization type.
    
    This class handles the creation and management of control elements
    for different visualization types in the BlazingPlot dashboard.
    """
    
    def __init__(self, dashboard_id: str):
        """
        Initialize the dashboard controls.
        
        Parameters
        ----------
        dashboard_id : str
            The unique identifier for the dashboard.
        """
        self.dashboard_id = dashboard_id
        self.viz_controls = {
            "scatter": self._scatter_controls,
            "line": self._line_controls,
            "bar": self._bar_controls,
            "bubble": self._bubble_controls,
            "pie": self._pie_controls,
            "box": self._box_controls,
            "histogram": self._histogram_controls,
            "histogram2d": self._histogram2d_controls,
            "timeseries": self._timeseries_controls,
            "stock": self._stock_controls,
            "error": self._error_controls,
            "bubblemap": self._bubblemap_controls,
            "choropleth": self._choropleth_controls,
            "mapline": self._mapline_controls,
            "area": self._area_controls,
            "table": self._table_controls,
            "pivot": self._pivot_controls
        }
    
    def get_controls(self, viz_type: str, columns: List[str]) -> List:
        """
        Get the controls for a specific visualization type.
        
        Parameters
        ----------
        viz_type : str
            The type of visualization.
        columns : list
            The list of available columns.
            
        Returns
        -------
        list
            A list of Dash components for the controls.
        """
        if viz_type in self.viz_controls:
            return self.viz_controls[viz_type](columns)
        else:
            # Default controls
            return self._default_controls(columns)
    
    def _default_controls(self, columns: List[str]) -> List:
        """
        Generate default controls.
        
        Parameters
        ----------
        columns : list
            The list of available columns.
            
        Returns
        -------
        list
            A list of Dash components for the controls.
        """
        return [
            html.Div([
                html.Label("X Axis:"),
                dcc.Dropdown(
                    id=f"x-axis-{self.dashboard_id}",
                    options=[{"label": col, "value": col} for col in columns],
                    value=columns[0] if columns else None,
                    clearable=False
                )
            ], className="mb-3"),
            
            html.Div([
                html.Label("Y Axis:"),
                dcc.Dropdown(
                    id=f"y-axis-{self.dashboard_id}",
                    options=[{"label": col, "value": col} for col in columns],
                    value=columns[1] if len(columns) > 1 else columns[0] if columns else None,
                    clearable=False
                )
            ], className="mb-3")
        ]
    
    def _scatter_controls(self, columns: List[str]) -> List:
        """
        Generate controls for scatter plots.
        
        Parameters
        ----------
        columns : list
            The list of available columns.
            
        Returns
        -------
        list
            A list of Dash components for the controls.
        """
        return [
            html.Div([
                html.Label("X Axis:"),
                dcc.Dropdown(
                    id=f"x-axis-{self.dashboard_id}",
                    options=[{"label": col, "value": col} for col in columns],
                    value=columns[0] if columns else None,
                    clearable=False
                )
            ], className="mb-3"),
            
            html.Div([
                html.Label("Y Axis:"),
                dcc.Dropdown(
                    id=f"y-axis-{self.dashboard_id}",
                    options=[{"label": col, "value": col} for col in columns],
                    value=columns[1] if len(columns) > 1 else columns[0] if columns else None,
                    clearable=False
                )
            ], className="mb-3"),
            
            html.Div([
                html.Label("Color By (optional):"),
                dcc.Dropdown(
                    id=f"color-{self.dashboard_id}",
                    options=[{"label": col, "value": col} for col in columns],
                    value=None,
                    clearable=True
                )
            ], className="mb-3"),
            
            html.Div([
                html.Label("Size By (optional):"),
                dcc.Dropdown(
                    id=f"size-{self.dashboard_id}",
                    options=[{"label": col, "value": col} for col in columns],
                    value=None,
                    clearable=True
                )
            ], className="mb-3"),
            
            html.Div([
                html.Label("Hover Data (optional):"),
                dcc.Dropdown(
                    id=f"hover-data-{self.dashboard_id}",
                    options=[{"label": col, "value": col} for col in columns],
                    value=[],
                    multi=True,
                    clearable=True
                )
            ], className="mb-3")
        ]
    
    def _line_controls(self, columns: List[str]) -> List:
        """
        Generate controls for line charts.
        
        Parameters
        ----------
        columns : list
            The list of available columns.
            
        Returns
        -------
        list
            A list of Dash components for the controls.
        """
        return [
            html.Div([
                html.Label("X Axis:"),
                dcc.Dropdown(
                    id=f"x-axis-{self.dashboard_id}",
                    options=[{"label": col, "value": col} for col in columns],
                    value=columns[0] if columns else None,
                    clearable=False
                )
            ], className="mb-3"),
            
            html.Div([
                html.Label("Y Axis:"),
                dcc.Dropdown(
                    id=f"y-axis-{self.dashboard_id}",
                    options=[{"label": col, "value": col} for col in columns],
                    value=columns[1] if len(columns) > 1 else columns[0] if columns else None,
                    clearable=False,
                    multi=True
                )
            ], className="mb-3"),
            
            html.Div([
                html.Label("Color By (optional):"),
                dcc.Dropdown(
                    id=f"color-{self.dashboard_id}",
                    options=[{"label": col, "value": col} for col in columns],
                    value=None,
                    clearable=True
                )
            ], className="mb-3"),
            
            html.Div([
                html.Label("Line Dash (optional):"),
                dcc.Dropdown(
                    id=f"line-dash-{self.dashboard_id}",
                    options=[{"label": col, "value": col} for col in columns],
                    value=None,
                    clearable=True
                )
            ], className="mb-3")
        ]
    
    def _bar_controls(self, columns: List[str]) -> List:
        """
        Generate controls for bar charts.
        
        Parameters
        ----------
        columns : list
            The list of available columns.
            
        Returns
        -------
        list
            A list of Dash components for the controls.
        """
        return [
            html.Div([
                html.Label("X Axis:"),
                dcc.Dropdown(
                    id=f"x-axis-{self.dashboard_id}",
                    options=[{"label": col, "value": col} for col in columns],
                    value=columns[0] if columns else None,
                    clearable=False
                )
            ], className="mb-3"),
            
            html.Div([
                html.Label("Y Axis:"),
                dcc.Dropdown(
                    id=f"y-axis-{self.dashboard_id}",
                    options=[{"label": col, "value": col} for col in columns],
                    value=columns[1] if len(columns) > 1 else columns[0] if columns else None,
                    clearable=False
                )
            ], className="mb-3"),
            
            html.Div([
                html.Label("Color By (optional):"),
                dcc.Dropdown(
                    id=f"color-{self.dashboard_id}",
                    options=[{"label": col, "value": col} for col in columns],
                    value=None,
                    clearable=True
                )
            ], className="mb-3"),
            
            html.Div([
                html.Label("Orientation:"),
                dcc.RadioItems(
                    id=f"orientation-{self.dashboard_id}",
                    options=[
                        {"label": "Vertical", "value": "v"},
                        {"label": "Horizontal", "value": "h"}
                    ],
                    value="v",
                    inline=True
                )
            ], className="mb-3")
        ]
    
    def _bubble_controls(self, columns: List[str]) -> List:
        """
        Generate controls for bubble charts.
        
        Parameters
        ----------
        columns : list
            The list of available columns.
            
        Returns
        -------
        list
            A list of Dash components for the controls.
        """
        return [
            html.Div([
                html.Label("X Axis:"),
                dcc.Dropdown(
                    id=f"x-axis-{self.dashboard_id}",
                    options=[{"label": col, "value": col} for col in columns],
                    value=columns[0] if columns else None,
                    clearable=False
                )
            ], className="mb-3"),
            
            html.Div([
                html.Label("Y Axis:"),
                dcc.Dropdown(
                    id=f"y-axis-{self.dashboard_id}",
                    options=[{"label": col, "value": col} for col in columns],
                    value=columns[1] if len(columns) > 1 else columns[0] if columns else None,
                    clearable=False
                )
            ], className="mb-3"),
            
            html.Div([
                html.Label("Size By:"),
                dcc.Dropdown(
                    id=f"size-{self.dashboard_id}",
                    options=[{"label": col, "value": col} for col in columns],
                    value=columns[2] if len(columns) > 2 else columns[0] if columns else None,
                    clearable=False
                )
            ], className="mb-3"),
            
            html.Div([
                html.Label("Color By (optional):"),
                dcc.Dropdown(
                    id=f"color-{self.dashboard_id}",
                    options=[{"label": col, "value": col} for col in columns],
                    value=None,
                    clearable=True
                )
            ], className="mb-3")
        ]
    
    def _pie_controls(self, columns: List[str]) -> List:
        """
        Generate controls for pie charts.
        
        Parameters
        ----------
        columns : list
            The list of available columns.
            
        Returns
        -------
        list
            A list of Dash components for the controls.
        """
        return [
            html.Div([
                html.Label("Names:"),
                dcc.Dropdown(
                    id=f"names-{self.dashboard_id}",
                    options=[{"label": col, "value": col} for col in columns],
                    value=columns[0] if columns else None,
                    clearable=False
                )
            ], className="mb-3"),
            
            html.Div([
                html.Label("Values:"),
                dcc.Dropdown(
                    id=f"values-{self.dashboard_id}",
                    options=[{"label": col, "value": col} for col in columns],
                    value=columns[1] if len(columns) > 1 else columns[0] if columns else None,
                    clearable=False
                )
            ], className="mb-3"),
            
            html.Div([
                html.Label("Hole Size (0-1):"),
                dcc.Slider(
                    id=f"hole-{self.dashboard_id}",
                    min=0,
                    max=1,
                    step=0.1,
                    value=0,
                    marks={i/10: str(i/10) for i in range(11)}
                )
            ], className="mb-3")
        ]
    
    def _box_controls(self, columns: List[str]) -> List:
        """
        Generate controls for box plots.
        
        Parameters
        ----------
        columns : list
            The list of available columns.
            
        Returns
        -------
        list
            A list of Dash components for the controls.
        """
        return [
            html.Div([
                html.Label("X Axis (Category):"),
                dcc.Dropdown(
                    id=f"x-axis-{self.dashboard_id}",
                    options=[{"label": col, "value": col} for col in columns],
                    value=columns[0] if columns else None,
                    clearable=False
                )
            ], className="mb-3"),
            
            html.Div([
                html.Label("Y Axis (Values):"),
                dcc.Dropdown(
                    id=f"y-axis-{self.dashboard_id}",
                    options=[{"label": col, "value": col} for col in columns],
                    value=columns[1] if len(columns) > 1 else columns[0] if columns else None,
                    clearable=False
                )
            ], className="mb-3"),
            
            html.Div([
                html.Label("Color By (optional):"),
                dcc.Dropdown(
                    id=f"color-{self.dashboard_id}",
                    options=[{"label": col, "value": col} for col in columns],
                    value=None,
                    clearable=True
                )
            ], className="mb-3"),
            
            html.Div([
                html.Label("Notched:"),
                dcc.RadioItems(
                    id=f"notched-{self.dashboard_id}",
                    options=[
                        {"label": "Yes", "value": True},
                        {"label": "No", "value": False}
                    ],
                    value=False,
                    inline=True
                )
            ], className="mb-3")
        ]
    
    def _histogram_controls(self, columns: List[str]) -> List:
        """
        Generate controls for histograms.
        
        Parameters
        ----------
        columns : list
            The list of available columns.
            
        Returns
        -------
        list
            A list of Dash components for the controls.
        """
        return [
            html.Div([
                html.Label("Values:"),
                dcc.Dropdown(
                    id=f"x-axis-{self.dashboard_id}",
                    options=[{"label": col, "value": col} for col in columns],
                    value=columns[0] if columns else None,
                    clearable=False
                )
            ], className="mb-3"),
            
            html.Div([
                html.Label("Color By (optional):"),
                dcc.Dropdown(
                    id=f"color-{self.dashboard_id}",
                    options=[{"label": col, "value": col} for col in columns],
                    value=None,
                    clearable=True
                )
            ], className="mb-3"),
            
            html.Div([
                html.Label("Number of Bins:"),
                dcc.Slider(
                    id=f"nbins-{self.dashboard_id}",
                    min=5,
                    max=100,
                    step=5,
                    value=30,
                    marks={i: str(i) for i in range(0, 101, 10)}
                )
            ], className="mb-3"),
            
            html.Div([
                html.Label("Histogram Type:"),
                dcc.RadioItems(
                    id=f"histnorm-{self.dashboard_id}",
                    options=[
                        {"label": "Count", "value": ""},
                        {"label": "Percent", "value": "percent"},
                        {"label": "Probability", "value": "probability"},
                        {"label": "Density", "value": "density"}
                    ],
                    value="",
                    inline=True
                )
            ], className="mb-3")
        ]
    
    def _histogram2d_controls(self, columns: List[str]) -> List:
        """
        Generate controls for 2D histograms.
        
        Parameters
        ----------
        columns : list
            The list of available columns.
            
        Returns
        -------
        list
            A list of Dash components for the controls.
        """
        return [
            html.Div([
                html.Label("X Axis:"),
                dcc.Dropdown(
                    id=f"x-axis-{self.dashboard_id}",
                    options=[{"label": col, "value": col} for col in columns],
                    value=columns[0] if columns else None,
                    clearable=False
                )
            ], className="mb-3"),
            
            html.Div([
                html.Label("Y Axis:"),
                dcc.Dropdown(
                    id=f"y-axis-{self.dashboard_id}",
                    options=[{"label": col, "value": col} for col in columns],
                    value=columns[1] if len(columns) > 1 else columns[0] if columns else None,
                    clearable=False
                )
            ], className="mb-3"),
            
            html.Div([
                html.Label("Number of X Bins:"),
                dcc.Slider(
                    id=f"nbinsx-{self.dashboard_id}",
                    min=5,
                    max=100,
                    step=5,
                    value=30,
                    marks={i: str(i) for i in range(0, 101, 10)}
                )
            ], className="mb-3"),
            
            html.Div([
                html.Label("Number of Y Bins:"),
                dcc.Slider(
                    id=f"nbinsy-{self.dashboard_id}",
                    min=5,
                    max=100,
                    step=5,
                    value=30,
                    marks={i: str(i) for i in range(0, 101, 10)}
                )
            ], className="mb-3"),
            
            html.Div([
                html.Label("Color Scale:"),
                dcc.Dropdown(
                    id=f"colorscale-{self.dashboard_id}",
                    options=[
                        {"label": "Viridis", "value": "viridis"},
                        {"label": "Plasma", "value": "plasma"},
                        {"label": "Inferno", "value": "inferno"},
                        {"label": "Magma", "value": "magma"},
                        {"label": "Cividis", "value": "cividis"},
                        {"label": "Warm", "value": "warm"},
                        {"label": "Cool", "value": "cool"},
                        {"label": "Blues", "value": "blues"},
                        {"label": "Reds", "value": "reds"},
                        {"label": "Greens", "value": "greens"},
                        {"label": "YlOrRd", "value": "ylorrd"},
                        {"label": "YlGnBu", "value": "ylgnbu"},
                        {"label": "RdBu", "value": "rdbu"},
                        {"label": "Jet", "value": "jet"}
                    ],
                    value="viridis",
                    clearable=False
                )
            ], className="mb-3")
        ]
    
    # Implement other control methods similarly
    def _timeseries_controls(self, columns: List[str]) -> List:
        """
        Generate controls for time series plots.
        
        Parameters
        ----------
        columns : list
            The list of available columns.
            
        Returns
        -------
        list
            A list of Dash components for the controls.
        """
        return [
            html.Div([
                html.Label("Time Column:"),
                dcc.Dropdown(
                    id=f"x-axis-{self.dashboard_id}",
                    options=[{"label": col, "value": col} for col in columns],
                    value=columns[0] if columns else None,
                    clearable=False
                )
            ], className="mb-3"),
            
            html.Div([
                html.Label("Value Column:"),
                dcc.Dropdown(
                    id=f"y-axis-{self.dashboard_id}",
                    options=[{"label": col, "value": col} for col in columns],
                    value=columns[1] if len(columns) > 1 else columns[0] if columns else None,
                    clearable=False,
                    multi=True
                )
            ], className="mb-3"),
            
            html.Div([
                html.Label("Group By (optional):"),
                dcc.Dropdown(
                    id=f"color-{self.dashboard_id}",
                    options=[{"label": col, "value": col} for col in columns],
                    value=None,
                    clearable=True
                )
            ], className="mb-3"),
            
            html.Div([
                html.Label("Line Type:"),
                dcc.RadioItems(
                    id=f"line-type-{self.dashboard_id}",
                    options=[
                        {"label": "Linear", "value": "linear"},
                        {"label": "Spline", "value": "spline"},
                        {"label": "Step", "value": "hv"}
                    ],
                    value="linear",
                    inline=True
                )
            ], className="mb-3")
        ]
    
    def _stock_controls(self, columns: List[str]) -> List:
        """
        Generate controls for stock charts.
        
        Parameters
        ----------
        columns : list
            The list of available columns.
            
        Returns
        -------
        list
            A list of Dash components for the controls.
        """
        return [
            html.Div([
                html.Label("Date Column:"),
                dcc.Dropdown(
                    id=f"date-{self.dashboard_id}",
                    options=[{"label": col, "value": col} for col in columns],
                    value=columns[0] if columns else None,
                    clearable=False
                )
            ], className="mb-3"),
            
            html.Div([
                html.Label("Open:"),
                dcc.Dropdown(
                    id=f"open-{self.dashboard_id}",
                    options=[{"label": col, "value": col} for col in columns],
                    value=None,
                    clearable=True
                )
            ], className="mb-3"),
            
            html.Div([
                html.Label("High:"),
                dcc.Dropdown(
                    id=f"high-{self.dashboard_id}",
                    options=[{"label": col, "value": col} for col in columns],
                    value=None,
                    clearable=True
                )
            ], className="mb-3"),
            
            html.Div([
                html.Label("Low:"),
                dcc.Dropdown(
                    id=f"low-{self.dashboard_id}",
                    options=[{"label": col, "value": col} for col in columns],
                    value=None,
                    clearable=True
                )
            ], className="mb-3"),
            
            html.Div([
                html.Label("Close:"),
                dcc.Dropdown(
                    id=f"close-{self.dashboard_id}",
                    options=[{"label": col, "value": col} for col in columns],
                    value=None,
                    clearable=True
                )
            ], className="mb-3"),
            
            html.Div([
                html.Label("Volume (optional):"),
                dcc.Dropdown(
                    id=f"volume-{self.dashboard_id}",
                    options=[{"label": col, "value": col} for col in columns],
                    value=None,
                    clearable=True
                )
            ], className="mb-3")
        ]
    
    def _error_controls(self, columns: List[str]) -> List:
        """
        Generate controls for error bar plots.
        
        Parameters
        ----------
        columns : list
            The list of available columns.
            
        Returns
        -------
        list
            A list of Dash components for the controls.
        """
        return [
            html.Div([
                html.Label("X Axis:"),
                dcc.Dropdown(
                    id=f"x-axis-{self.dashboard_id}",
                    options=[{"label": col, "value": col} for col in columns],
                    value=columns[0] if columns else None,
                    clearable=False
                )
            ], className="mb-3"),
            
            html.Div([
                html.Label("Y Axis:"),
                dcc.Dropdown(
                    id=f"y-axis-{self.dashboard_id}",
                    options=[{"label": col, "value": col} for col in columns],
                    value=columns[1] if len(columns) > 1 else columns[0] if columns else None,
                    clearable=False
                )
            ], className="mb-3"),
            
            html.Div([
                html.Label("Error Y:"),
                dcc.Dropdown(
                    id=f"error-y-{self.dashboard_id}",
                    options=[{"label": col, "value": col} for col in columns],
                    value=columns[2] if len(columns) > 2 else None,
                    clearable=True
                )
            ], className="mb-3"),
            
            html.Div([
                html.Label("Color By (optional):"),
                dcc.Dropdown(
                    id=f"color-{self.dashboard_id}",
                    options=[{"label": col, "value": col} for col in columns],
                    value=None,
                    clearable=True
                )
            ], className="mb-3")
        ]
    
    # Placeholder methods for other visualization types
    def _bubblemap_controls(self, columns: List[str]) -> List:
        return self._default_controls(columns)
    
    def _choropleth_controls(self, columns: List[str]) -> List:
        return self._default_controls(columns)
    
    def _mapline_controls(self, columns: List[str]) -> List:
        return self._default_controls(columns)
    
    def _area_controls(self, columns: List[str]) -> List:
        return self._default_controls(columns)
    
    def _table_controls(self, columns: List[str]) -> List:
        return self._default_controls(columns)
    
    def _pivot_controls(self, columns: List[str]) -> List:
        return self._default_controls(columns)


class DashboardLayout:
    """
    Class for creating and managing the dashboard layout.
    
    This class handles the creation of the dashboard layout and
    the registration of callbacks for interactivity.
    """
    
    def __init__(
        self,
        dashboard_id: str,
        data: pl.DataFrame,
        figsize: tuple = (1200, 800),
        title: str = "BlazingPlot Dashboard",
        palettes: Dict[str, List] = None
    ):
        """
        Initialize the dashboard layout.
        
        Parameters
        ----------
        dashboard_id : str
            The unique identifier for the dashboard.
        data : polars.DataFrame
            The data to visualize.
        figsize : tuple, optional
            The size of the dashboard.
        title : str, optional
            The title of the dashboard.
        palettes : dict, optional
            A dictionary of color palettes.
        """
        self.dashboard_id = dashboard_id
        self.data = data
        self.figsize = figsize
        self.title = title
        self.palettes = palettes or {
            "pastel": px.colors.qualitative.Pastel1,
            "plotly": px.colors.qualitative.Plotly,
            "d3": px.colors.qualitative.D3,
            "g10": px.colors.qualitative.G10,
            "t10": px.colors.qualitative.T10
        }
        self.controls = DashboardControls(dashboard_id)
    
    def create_layout(self) -> html.Div:
        """
        Create the dashboard layout.
        
        Returns
        -------
        dash.html.Div
            The dashboard layout.
        """
        # Header
        header = dbc.Row([
            # Left: Title
            dbc.Col(html.H1(self.title), width=4),
            
            # Center: Palette selector
            dbc.Col([
                html.Label("Color Palette:"),
                dcc.Dropdown(
                    id=f"palette-dropdown-{self.dashboard_id}",
                    options=[{"label": k.capitalize(), "value": k} for k in self.palettes.keys()],
                    value="pastel",
                    clearable=False
                )
            ], width=4),
            
            # Right: Export buttons
            dbc.Col([
                dbc.ButtonGroup([
                    dbc.Button("Export PNG", id=f"export-png-{self.dashboard_id}", color="primary", className="me-1"),
                    dbc.Button("Export HTML", id=f"export-html-{self.dashboard_id}", color="primary", className="me-1"),
                    dbc.Button("Export CSV", id=f"export-csv-{self.dashboard_id}", color="primary")
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
                            id=f"column-selector-{self.dashboard_id}",
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
                        id=f"viz-type-{self.dashboard_id}",
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
                html.Div(id=f"dynamic-controls-{self.dashboard_id}"),
                
                # Filter section
                html.Div([
                    html.H5("Filters", className="mt-4"),
                    html.Div(id=f"filter-controls-{self.dashboard_id}")
                ]),
                
                # Update button
                html.Div([
                    dbc.Button(
                        "Update Visualization",
                        id=f"update-viz-{self.dashboard_id}",
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
                            id=f"fullscreen-{self.dashboard_id}",
                            className="btn btn-sm btn-outline-secondary position-absolute top-0 end-0 m-2"
                        ),
                        dcc.Dropdown(
                            id=f"chart-elements-{self.dashboard_id}",
                            multi=True,
                            placeholder="Toggle chart elements...",
                            className="position-absolute top-0 end-5 m-2",
                            style={"width": "200px"}
                        )
                    ], className="position-relative"),
                    dcc.Loading(
                        id=f"loading-{self.dashboard_id}",
                        type="circle",
                        children=dcc.Graph(
                            id=f"main-chart-{self.dashboard_id}",
                            style={"height": f"{self.figsize[1]-100}px"}
                        )
                    )
                ])
            ], width=7)
        ])
        
        return dbc.Container([header, main_body], fluid=True)
    
    def register_callbacks(self, app: dash.Dash) -> None:
        """
        Register callbacks for the dashboard.
        
        Parameters
        ----------
        app : dash.Dash
            The Dash application.
        """
        # Callback to update dynamic controls based on visualization type
        @app.callback(
            Output(f"dynamic-controls-{self.dashboard_id}", "children"),
            Input(f"viz-type-{self.dashboard_id}", "value"),
            Input(f"column-selector-{self.dashboard_id}", "value")
        )
        def update_dynamic_controls(viz_type, selected_columns):
            return self.controls.get_controls(viz_type, selected_columns)
        
        # Callback to update filter controls based on selected columns
        @app.callback(
            Output(f"filter-controls-{self.dashboard_id}", "children"),
            Input(f"column-selector-{self.dashboard_id}", "value")
        )
        def update_filter_controls(selected_columns):
            # Create a filter control for each selected column
            filters = []
            for col in selected_columns[:3]:  # Limit to first 3 columns for simplicity
                # Get column data type
                col_type = self.data[col].dtype
                
                # Create appropriate filter control based on data type
                if col_type in [pl.Int64, pl.Int32, pl.Int16, pl.Int8, pl.Float64, pl.Float32]:
                    # Numeric column - use range slider
                    min_val = float(self.data[col].min())
                    max_val = float(self.data[col].max())
                    
                    filters.append(html.Div([
                        html.Label(f"Filter {col}:"),
                        dcc.RangeSlider(
                            id=f"filter-{col}-{self.dashboard_id}",
                            min=min_val,
                            max=max_val,
                            step=(max_val - min_val) / 100,
                            marks={min_val: f"{min_val:.1f}", max_val: f"{max_val:.1f}"},
                            value=[min_val, max_val]
                        )
                    ], className="mb-3"))
                else:
                    # Categorical column - use multi-select dropdown
                    unique_values = self.data[col].unique().to_list()
                    if len(unique_values) <= 20:  # Only for columns with reasonable number of unique values
                        filters.append(html.Div([
                            html.Label(f"Filter {col}:"),
                            dcc.Dropdown(
                                id=f"filter-{col}-{self.dashboard_id}",
                                options=[{"label": str(val), "value": str(val)} for val in unique_values],
                                value=unique_values,
                                multi=True
                            )
                        ], className="mb-3"))
            
            return filters
        
        # Callback to update chart elements dropdown based on visualization type
        @app.callback(
            Output(f"chart-elements-{self.dashboard_id}", "options"),
            Output(f"chart-elements-{self.dashboard_id}", "value"),
            Input(f"viz-type-{self.dashboard_id}", "value")
        )
        def update_chart_elements(viz_type):
            # Define elements for each visualization type
            elements = {
                "scatter": ["title", "legend", "x_axis", "y_axis", "grid"],
                "line": ["title", "legend", "x_axis", "y_axis", "grid"],
                "bar": ["title", "legend", "x_axis", "y_axis", "grid"],
                "bubble": ["title", "legend", "x_axis", "y_axis", "grid", "colorbar"],
                "pie": ["title", "legend"],
                "box": ["title", "legend", "x_axis", "y_axis", "grid"],
                "histogram": ["title", "legend", "x_axis", "y_axis", "grid"],
                "histogram2d": ["title", "x_axis", "y_axis", "colorbar"],
                "timeseries": ["title", "legend", "x_axis", "y_axis", "grid"],
                "stock": ["title", "x_axis", "y_axis", "grid", "legend"],
                "error": ["title", "legend", "x_axis", "y_axis", "grid"],
                "bubblemap": ["title", "legend", "colorbar"],
                "choropleth": ["title", "legend", "colorbar"],
                "mapline": ["title", "legend"],
                "area": ["title", "legend", "x_axis", "y_axis", "grid"],
                "table": ["title"],
                "pivot": ["title"]
            }
            
            # Get elements for the selected visualization type
            viz_elements = elements.get(viz_type, ["title", "legend", "x_axis", "y_axis", "grid"])
            
            # Create options for the dropdown
            options = [{"label": e.replace("_", " ").title(), "value": e} for e in viz_elements]
            
            # All elements are visible by default
            value = viz_elements
            
            return options, value
