"""
Base visualization class and implementations for BlazingPlot.

This module contains the abstract base class for all visualizations
and implementations of specific visualization types.
"""

import polars as pl
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from abc import ABC, abstractmethod
from typing import Optional, Dict, List, Any, Union, Tuple
import io
import base64


class BaseVisualization(ABC):
    """
    Abstract base class for all visualizations in BlazingPlot.
    
    This class defines the interface that all visualization classes must implement.
    It provides common functionality for data transformation, rendering, and exporting.
    
    Parameters
    ----------
    data : polars.DataFrame
        The data to visualize.
    title : str, optional
        The title of the visualization.
    palette : list or str, optional
        A color palette to use for the visualization.
    """
    
    def __init__(
        self,
        data: pl.DataFrame,
        title: Optional[str] = None,
        palette: Optional[List[str]] = None
    ):
        if not isinstance(data, pl.DataFrame):
            raise TypeError("Data must be a polars DataFrame")
        
        self.data = data
        self.title = title
        self.palette = palette or px.colors.qualitative.Plotly
        self.figure = None
        self.metadata = {
            "type": self.__class__.__name__,
            "elements": self._get_default_elements(),
            "interactivity": True
        }
    
    @abstractmethod
    def plot(self, **kwargs) -> go.Figure:
        """
        Create and return the visualization figure.
        
        This method must be implemented by all subclasses.
        
        Parameters
        ----------
        **kwargs
            Additional keyword arguments specific to the visualization type.
            
        Returns
        -------
        plotly.graph_objects.Figure
            The plotly figure object.
        """
        pass
    
    def _transform_data(self) -> pl.DataFrame:
        """
        Transform the data for visualization.
        
        This method can be overridden by subclasses to perform
        specific data transformations.
        
        Returns
        -------
        polars.DataFrame
            The transformed data.
        """
        return self.data
    
    def _get_default_elements(self) -> Dict[str, bool]:
        """
        Get the default elements for this visualization type.
        
        Returns
        -------
        dict
            A dictionary of element names and their default visibility.
        """
        return {
            "title": True,
            "legend": True,
            "x_axis": True,
            "y_axis": True,
            "grid": True,
            "colorbar": True
        }
    
    def update_element_visibility(self, elements: Dict[str, bool]) -> None:
        """
        Update the visibility of chart elements.
        
        Parameters
        ----------
        elements : dict
            A dictionary of element names and their visibility.
        """
        if self.figure is None:
            self.plot()
        
        for element, visible in elements.items():
            if element == "title":
                self.figure.update_layout(title_text="" if not visible else self.title)
            elif element == "legend":
                self.figure.update_layout(showlegend=visible)
            elif element == "x_axis":
                self.figure.update_xaxes(visible=visible)
            elif element == "y_axis":
                self.figure.update_yaxes(visible=visible)
            elif element == "grid":
                self.figure.update_xaxes(showgrid=visible)
                self.figure.update_yaxes(showgrid=visible)
            elif element == "colorbar":
                # This is more complex and depends on the chart type
                for trace in self.figure.data:
                    if hasattr(trace, "colorbar"):
                        trace.colorbar.visible = visible
    
    def export_html(self, filename: Optional[str] = None) -> Optional[str]:
        """
        Export the visualization to HTML.
        
        Parameters
        ----------
        filename : str, optional
            The filename to save the HTML to. If None, returns the HTML as a string.
            
        Returns
        -------
        str or None
            The HTML as a string if filename is None, otherwise None.
        """
        if self.figure is None:
            self.plot()
        
        if filename:
            self.figure.write_html(filename)
            return None
        else:
            return self.figure.to_html(include_plotlyjs=True, full_html=True)
    
    def export_png(self, filename: Optional[str] = None) -> Optional[bytes]:
        """
        Export the visualization to PNG.
        
        Parameters
        ----------
        filename : str, optional
            The filename to save the PNG to. If None, returns the PNG as bytes.
            
        Returns
        -------
        bytes or None
            The PNG as bytes if filename is None, otherwise None.
        """
        if self.figure is None:
            self.plot()
        
        if filename:
            self.figure.write_image(filename)
            return None
        else:
            img_bytes = self.figure.to_image(format="png")
            return img_bytes


class ScatterPlot(BaseVisualization):
    """
    Scatter plot visualization.
    
    Parameters
    ----------
    data : polars.DataFrame
        The data to visualize.
    x : str
        The column to use for the x-axis.
    y : str
        The column to use for the y-axis.
    color : str, optional
        The column to use for color encoding.
    size : str, optional
        The column to use for size encoding.
    hover_data : list, optional
        Additional columns to show in hover data.
    title : str, optional
        The title of the visualization.
    palette : list or str, optional
        A color palette to use for the visualization.
    """
    
    def __init__(
        self,
        data: pl.DataFrame,
        x: str,
        y: str,
        color: Optional[str] = None,
        size: Optional[str] = None,
        hover_data: Optional[List[str]] = None,
        title: Optional[str] = None,
        palette: Optional[List[str]] = None
    ):
        super().__init__(data, title, palette)
        self.x = x
        self.y = y
        self.color = color
        self.size = size
        self.hover_data = hover_data or []
        
        # Update metadata
        self.metadata["mapping"] = {
            "x": x,
            "y": y,
            "color": color,
            "size": size
        }
    
    def plot(self, **kwargs) -> go.Figure:
        """
        Create and return a scatter plot figure.
        
        Parameters
        ----------
        **kwargs
            Additional keyword arguments to pass to plotly.express.scatter.
            
        Returns
        -------
        plotly.graph_objects.Figure
            The scatter plot figure.
        """
        # Transform data using Polars for performance
        df = self._transform_data()
        
        # Convert to pandas for Plotly
        pdf = df.to_pandas()
        
        # Create the figure
        fig = px.scatter(
            pdf,
            x=self.x,
            y=self.y,
            color=self.color,
            size=self.size,
            hover_data=self.hover_data,
            title=self.title,
            color_discrete_sequence=self.palette,
            **kwargs
        )
        
        self.figure = fig
        return fig


class LineChart(BaseVisualization):
    """
    Line chart visualization.
    
    Parameters
    ----------
    data : polars.DataFrame
        The data to visualize.
    x : str
        The column to use for the x-axis.
    y : str or list
        The column(s) to use for the y-axis.
    color : str, optional
        The column to use for color encoding.
    line_dash : str, optional
        The column to use for line dash encoding.
    hover_data : list, optional
        Additional columns to show in hover data.
    title : str, optional
        The title of the visualization.
    palette : list or str, optional
        A color palette to use for the visualization.
    """
    
    def __init__(
        self,
        data: pl.DataFrame,
        x: str,
        y: Union[str, List[str]],
        color: Optional[str] = None,
        line_dash: Optional[str] = None,
        hover_data: Optional[List[str]] = None,
        title: Optional[str] = None,
        palette: Optional[List[str]] = None
    ):
        super().__init__(data, title, palette)
        self.x = x
        self.y = y
        self.color = color
        self.line_dash = line_dash
        self.hover_data = hover_data or []
        
        # Update metadata
        self.metadata["mapping"] = {
            "x": x,
            "y": y,
            "color": color,
            "line_dash": line_dash
        }
    
    def plot(self, **kwargs) -> go.Figure:
        """
        Create and return a line chart figure.
        
        Parameters
        ----------
        **kwargs
            Additional keyword arguments to pass to plotly.express.line.
            
        Returns
        -------
        plotly.graph_objects.Figure
            The line chart figure.
        """
        # Transform data using Polars for performance
        df = self._transform_data()
        
        # Convert to pandas for Plotly
        pdf = df.to_pandas()
        
        # Create the figure
        fig = px.line(
            pdf,
            x=self.x,
            y=self.y,
            color=self.color,
            line_dash=self.line_dash,
            hover_data=self.hover_data,
            title=self.title,
            color_discrete_sequence=self.palette,
            **kwargs
        )
        
        self.figure = fig
        return fig


class BarChart(BaseVisualization):
    """
    Bar chart visualization.
    
    Parameters
    ----------
    data : polars.DataFrame
        The data to visualize.
    x : str
        The column to use for the x-axis.
    y : str
        The column to use for the y-axis.
    color : str, optional
        The column to use for color encoding.
    pattern_shape : str, optional
        The column to use for pattern shape encoding.
    hover_data : list, optional
        Additional columns to show in hover data.
    title : str, optional
        The title of the visualization.
    palette : list or str, optional
        A color palette to use for the visualization.
    orientation : str, optional
        The orientation of the bars ('v' for vertical, 'h' for horizontal).
    """
    
    def __init__(
        self,
        data: pl.DataFrame,
        x: str,
        y: str,
        color: Optional[str] = None,
        pattern_shape: Optional[str] = None,
        hover_data: Optional[List[str]] = None,
        title: Optional[str] = None,
        palette: Optional[List[str]] = None,
        orientation: str = 'v'
    ):
        super().__init__(data, title, palette)
        self.x = x
        self.y = y
        self.color = color
        self.pattern_shape = pattern_shape
        self.hover_data = hover_data or []
        self.orientation = orientation
        
        # Update metadata
        self.metadata["mapping"] = {
            "x": x,
            "y": y,
            "color": color,
            "pattern_shape": pattern_shape,
            "orientation": orientation
        }
    
    def _transform_data(self) -> pl.DataFrame:
        """
        Transform the data for the bar chart.
        
        For bar charts, we might want to aggregate the data.
        
        Returns
        -------
        polars.DataFrame
            The transformed data.
        """
        # Example of data transformation using Polars
        # This could be customized based on specific needs
        df = self.data
        
        # If color is specified, we might want to group by it
        if self.color:
            group_cols = [self.x, self.color]
        else:
            group_cols = [self.x]
        
        # Check if we need to aggregate
        if len(group_cols) < len(df):
            df = df.group_by(group_cols).agg(pl.col(self.y).mean())
        
        return df
    
    def plot(self, **kwargs) -> go.Figure:
        """
        Create and return a bar chart figure.
        
        Parameters
        ----------
        **kwargs
            Additional keyword arguments to pass to plotly.express.bar.
            
        Returns
        -------
        plotly.graph_objects.Figure
            The bar chart figure.
        """
        # Transform data using Polars for performance
        df = self._transform_data()
        
        # Convert to pandas for Plotly
        pdf = df.to_pandas()
        
        # Create the figure
        fig = px.bar(
            pdf,
            x=self.x if self.orientation == 'v' else self.y,
            y=self.y if self.orientation == 'v' else self.x,
            color=self.color,
            pattern_shape=self.pattern_shape,
            hover_data=self.hover_data,
            title=self.title,
            color_discrete_sequence=self.palette,
            orientation=self.orientation,
            **kwargs
        )
        
        self.figure = fig
        return fig


class BubbleChart(BaseVisualization):
    """
    Bubble chart visualization.
    
    Parameters
    ----------
    data : polars.DataFrame
        The data to visualize.
    x : str
        The column to use for the x-axis.
    y : str
        The column to use for the y-axis.
    size : str
        The column to use for bubble size.
    color : str, optional
        The column to use for color encoding.
    hover_data : list, optional
        Additional columns to show in hover data.
    title : str, optional
        The title of the visualization.
    palette : list or str, optional
        A color palette to use for the visualization.
    """
    
    def __init__(
        self,
        data: pl.DataFrame,
        x: str,
        y: str,
        size: str,
        color: Optional[str] = None,
        hover_data: Optional[List[str]] = None,
        title: Optional[str] = None,
        palette: Optional[List[str]] = None
    ):
        super().__init__(data, title, palette)
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.hover_data = hover_data or []
        
        # Update metadata
        self.metadata["mapping"] = {
            "x": x,
            "y": y,
            "size": size,
            "color": color
        }
    
    def plot(self, **kwargs) -> go.Figure:
        """
        Create and return a bubble chart figure.
        
        Parameters
        ----------
        **kwargs
            Additional keyword arguments to pass to plotly.express.scatter.
            
        Returns
        -------
        plotly.graph_objects.Figure
            The bubble chart figure.
        """
        # Transform data using Polars for performance
        df = self._transform_data()
        
        # Convert to pandas for Plotly
        pdf = df.to_pandas()
        
        # Create the figure
        fig = px.scatter(
            pdf,
            x=self.x,
            y=self.y,
            size=self.size,
            color=self.color,
            hover_data=self.hover_data,
            title=self.title,
            color_discrete_sequence=self.palette,
            **kwargs
        )
        
        self.figure = fig
        return fig


class PieChart(BaseVisualization):
    """
    Pie chart visualization.
    
    Parameters
    ----------
    data : polars.DataFrame
        The data to visualize.
    names : str
        The column to use for slice names.
    values : str
        The column to use for slice values.
    color : str, optional
        The column to use for color encoding.
    hover_data : list, optional
        Additional columns to show in hover data.
    title : str, optional
        The title of the visualization.
    palette : list or str, optional
        A color palette to use for the visualization.
    """
    
    def __init__(
        self,
        data: pl.DataFrame,
        names: str,
        values: str,
        color: Optional[str] = None,
        hover_data: Optional[List[str]] = None,
        title: Optional[str] = None,
        palette: Optional[List[str]] = None
    ):
        super().__init__(data, title, palette)
        self.names = names
        self.values = values
        self.color = color
        self.hover_data = hover_data or []
        
        # Update metadata
        self.metadata["mapping"] = {
            "names": names,
            "values": values,
            "color": color
        }
    
    def _transform_data(self) -> pl.DataFrame:
        """
        Transform the data for the pie chart.
        
        For pie charts, we typically need to aggregate the data.
        
        Returns
        -------
        polars.DataFrame
            The transformed data.
        """
        # Group by the names column and sum the values
        df = self.data.group_by(self.names).agg(pl.col(self.values).sum())
        return df
    
    def plot(self, **kwargs) -> go.Figure:
        """
        Create and return a pie chart figure.
        
        Parameters
        ----------
        **kwargs
            Additional keyword arguments to pass to plotly.express.pie.
            
        Returns
        -------
        plotly.graph_objects.Figure
            The pie chart figure.
        """
        # Transform data using Polars for performance
        df = self._transform_data()
        
        # Convert to pandas for Plotly
        pdf = df.to_pandas()
        
        # Create the figure
        fig = px.pie(
            pdf,
            names=self.names,
            values=self.values,
            color=self.color or self.names,
            hover_data=self.hover_data,
            title=self.title,
            color_discrete_sequence=self.palette,
            **kwargs
        )
        
        self.figure = fig
        return fig
