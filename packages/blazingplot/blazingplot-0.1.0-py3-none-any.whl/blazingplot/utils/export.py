"""
Utility functions for export and palette management in BlazingPlot.
"""

import polars as pl
import pandas as pd
import plotly.io as pio
import plotly.express as px
import matplotlib.pyplot as plt
import matplotlib as mpl
import base64
import io
from typing import Dict, List, Optional, Union, Tuple, Any


class ExportManager:
    """
    Handles exporting visualizations and data to various formats.
    
    This class provides methods for exporting visualizations to PNG and HTML,
    and data to CSV.
    """
    
    @staticmethod
    def to_png(fig, filename: Optional[str] = None) -> Optional[bytes]:
        """
        Export a plotly figure to PNG.
        
        Parameters
        ----------
        fig : plotly.graph_objects.Figure
            The figure to export.
        filename : str, optional
            The filename to save the PNG to. If None, returns the PNG as bytes.
            
        Returns
        -------
        bytes or None
            The PNG as bytes if filename is None, otherwise None.
        """
        if filename:
            fig.write_image(filename)
            return None
        else:
            img_bytes = fig.to_image(format="png")
            return img_bytes
    
    @staticmethod
    def to_html(fig, filename: Optional[str] = None) -> Optional[str]:
        """
        Export a plotly figure to HTML.
        
        Parameters
        ----------
        fig : plotly.graph_objects.Figure
            The figure to export.
        filename : str, optional
            The filename to save the HTML to. If None, returns the HTML as a string.
            
        Returns
        -------
        str or None
            The HTML as a string if filename is None, otherwise None.
        """
        if filename:
            fig.write_html(filename)
            return None
        else:
            return fig.to_html(include_plotlyjs=True, full_html=True)
    
    @staticmethod
    def to_csv(data: Union[pl.DataFrame, pd.DataFrame], filename: Optional[str] = None) -> Optional[str]:
        """
        Export data to CSV.
        
        Parameters
        ----------
        data : polars.DataFrame or pandas.DataFrame
            The data to export.
        filename : str, optional
            The filename to save the CSV to. If None, returns the CSV as a string.
            
        Returns
        -------
        str or None
            The CSV as a string if filename is None, otherwise None.
        """
        if isinstance(data, pl.DataFrame):
            if filename:
                data.write_csv(filename)
                return None
            else:
                buffer = io.StringIO()
                data.write_csv(buffer)
                buffer.seek(0)
                return buffer.getvalue()
        elif isinstance(data, pd.DataFrame):
            if filename:
                data.to_csv(filename, index=False)
                return None
            else:
                return data.to_csv(index=False)
        else:
            raise TypeError("Data must be a polars DataFrame or pandas DataFrame")


class PaletteManager:
    """
    Manages color palettes for visualizations.
    
    This class provides methods for creating, managing, and applying
    color palettes to visualizations.
    """
    
    def __init__(self):
        """Initialize the palette manager with default palettes."""
        # Default palettes
        self.palettes = {
            "pastel": px.colors.qualitative.Pastel1,
            "plotly": px.colors.qualitative.Plotly,
            "d3": px.colors.qualitative.D3,
            "g10": px.colors.qualitative.G10,
            "t10": px.colors.qualitative.T10,
            "viridis": self._get_colormap_colors("viridis", 10),
            "plasma": self._get_colormap_colors("plasma", 10),
            "inferno": self._get_colormap_colors("inferno", 10),
            "magma": self._get_colormap_colors("magma", 10),
            "cividis": self._get_colormap_colors("cividis", 10)
        }
    
    def _get_colormap_colors(self, cmap_name: str, n_colors: int = 10) -> List[str]:
        """
        Get colors from a matplotlib colormap.
        
        Parameters
        ----------
        cmap_name : str
            The name of the colormap.
        n_colors : int, optional
            The number of colors to extract.
            
        Returns
        -------
        list
            A list of colors as hex strings.
        """
        cmap = plt.get_cmap(cmap_name)
        colors = [mpl.colors.rgb2hex(cmap(i / (n_colors - 1))) for i in range(n_colors)]
        return colors
    
    def add_palette(self, name: str, colors: List[str]) -> None:
        """
        Add a custom palette.
        
        Parameters
        ----------
        name : str
            The name of the palette.
        colors : list
            A list of colors as hex strings.
        """
        self.palettes[name] = colors
    
    def add_matplotlib_palette(self, name: str, cmap_name: str, n_colors: int = 10) -> None:
        """
        Add a palette from a matplotlib colormap.
        
        Parameters
        ----------
        name : str
            The name to give the palette.
        cmap_name : str
            The name of the matplotlib colormap.
        n_colors : int, optional
            The number of colors to extract.
        """
        self.palettes[name] = self._get_colormap_colors(cmap_name, n_colors)
    
    def get_palette(self, name: str) -> List[str]:
        """
        Get a palette by name.
        
        Parameters
        ----------
        name : str
            The name of the palette.
            
        Returns
        -------
        list
            A list of colors as hex strings.
        """
        if name in self.palettes:
            return self.palettes[name]
        else:
            # Return default palette if not found
            return self.palettes["plotly"]
    
    def get_palette_names(self) -> List[str]:
        """
        Get the names of all available palettes.
        
        Returns
        -------
        list
            A list of palette names.
        """
        return list(self.palettes.keys())
    
    def apply_palette_to_figure(self, fig, palette_name: str) -> None:
        """
        Apply a palette to a plotly figure.
        
        Parameters
        ----------
        fig : plotly.graph_objects.Figure
            The figure to apply the palette to.
        palette_name : str
            The name of the palette to apply.
        """
        if palette_name in self.palettes:
            palette = self.palettes[palette_name]
            fig.update_traces(marker_color=palette)
            
            # Update colorscales for heatmaps, contour plots, etc.
            for trace in fig.data:
                if hasattr(trace, "colorscale"):
                    # Create a custom colorscale from the palette
                    n_colors = len(palette)
                    colorscale = [[i / (n_colors - 1), color] for i, color in enumerate(palette)]
                    trace.colorscale = colorscale
