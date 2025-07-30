"""
Unit tests for BlazingPlot.

This module provides unit tests for the BlazingPlot library.
"""

import unittest
import polars as pl
import numpy as np
import pandas as pd
import plotly.graph_objects as go

from blazingplot.visualizations.base import (
    BaseVisualization, ScatterPlot, LineChart, BarChart, BubbleChart, PieChart
)
from blazingplot.dashboard.dashboard import Dashboard
from blazingplot.utils.export import ExportManager, PaletteManager


class TestBaseVisualization(unittest.TestCase):
    """Test cases for the BaseVisualization class."""
    
    def setUp(self):
        """Set up test data."""
        # Create test data
        self.data = pl.DataFrame({
            'x': [1, 2, 3, 4, 5],
            'y': [10, 20, 15, 25, 30],
            'category': ['A', 'B', 'A', 'B', 'A']
        })
    
    def test_initialization(self):
        """Test initialization of visualization classes."""
        # Test ScatterPlot
        scatter = ScatterPlot(self.data, 'x', 'y', title="Test Scatter")
        self.assertEqual(scatter.x, 'x')
        self.assertEqual(scatter.y, 'y')
        self.assertEqual(scatter.title, "Test Scatter")
        
        # Test LineChart
        line = LineChart(self.data, 'x', 'y', title="Test Line")
        self.assertEqual(line.x, 'x')
        self.assertEqual(line.y, 'y')
        self.assertEqual(line.title, "Test Line")
        
        # Test BarChart
        bar = BarChart(self.data, 'category', 'y', title="Test Bar")
        self.assertEqual(bar.x, 'category')
        self.assertEqual(bar.y, 'y')
        self.assertEqual(bar.title, "Test Bar")
        
        # Test BubbleChart
        bubble = BubbleChart(self.data, 'x', 'y', 'y', title="Test Bubble")
        self.assertEqual(bubble.x, 'x')
        self.assertEqual(bubble.y, 'y')
        self.assertEqual(bubble.size, 'y')
        self.assertEqual(bubble.title, "Test Bubble")
        
        # Test PieChart
        pie = PieChart(self.data, 'category', 'y', title="Test Pie")
        self.assertEqual(pie.names, 'category')
        self.assertEqual(pie.values, 'y')
        self.assertEqual(pie.title, "Test Pie")
    
    def test_plot_methods(self):
        """Test plot methods of visualization classes."""
        # Test ScatterPlot
        scatter = ScatterPlot(self.data, 'x', 'y')
        fig = scatter.plot()
        self.assertIsInstance(fig, go.Figure)
        
        # Test LineChart
        line = LineChart(self.data, 'x', 'y')
        fig = line.plot()
        self.assertIsInstance(fig, go.Figure)
        
        # Test BarChart
        bar = BarChart(self.data, 'category', 'y')
        fig = bar.plot()
        self.assertIsInstance(fig, go.Figure)
        
        # Test BubbleChart
        bubble = BubbleChart(self.data, 'x', 'y', 'y')
        fig = bubble.plot()
        self.assertIsInstance(fig, go.Figure)
        
        # Test PieChart
        pie = PieChart(self.data, 'category', 'y')
        fig = pie.plot()
        self.assertIsInstance(fig, go.Figure)
    
    def test_export_methods(self):
        """Test export methods of visualization classes."""
        # Test HTML export
        scatter = ScatterPlot(self.data, 'x', 'y')
        scatter.plot()
        html = scatter.export_html()
        self.assertIsInstance(html, str)
        self.assertIn("<html>", html)
        
        # PNG export would require a more complex test setup
        # so we'll skip it for this simple unit test


class TestDashboard(unittest.TestCase):
    """Test cases for the Dashboard class."""
    
    def setUp(self):
        """Set up test data."""
        # Create test data
        self.data = pl.DataFrame({
            'x': [1, 2, 3, 4, 5],
            'y': [10, 20, 15, 25, 30],
            'category': ['A', 'B', 'A', 'B', 'A']
        })
    
    def test_initialization(self):
        """Test initialization of Dashboard class."""
        dashboard = Dashboard(self.data, title="Test Dashboard")
        self.assertEqual(dashboard.title, "Test Dashboard")
        self.assertEqual(dashboard.data, self.data)
        self.assertIsNotNone(dashboard.app)
    
    # More complex dashboard tests would require a running Dash server
    # which is beyond the scope of these simple unit tests


class TestExportManager(unittest.TestCase):
    """Test cases for the ExportManager class."""
    
    def setUp(self):
        """Set up test data."""
        # Create test data
        self.data = pl.DataFrame({
            'x': [1, 2, 3, 4, 5],
            'y': [10, 20, 15, 25, 30],
            'category': ['A', 'B', 'A', 'B', 'A']
        })
        
        # Create a test figure
        scatter = ScatterPlot(self.data, 'x', 'y')
        self.fig = scatter.plot()
    
    def test_to_html(self):
        """Test HTML export."""
        html = ExportManager.to_html(self.fig)
        self.assertIsInstance(html, str)
        self.assertIn("<html>", html)
    
    def test_to_csv(self):
        """Test CSV export."""
        csv = ExportManager.to_csv(self.data)
        self.assertIsInstance(csv, str)
        self.assertIn("x,y,category", csv)


class TestPaletteManager(unittest.TestCase):
    """Test cases for the PaletteManager class."""
    
    def test_initialization(self):
        """Test initialization of PaletteManager class."""
        palette_manager = PaletteManager()
        self.assertIn("pastel", palette_manager.get_palette_names())
        self.assertIn("plotly", palette_manager.get_palette_names())
    
    def test_add_palette(self):
        """Test adding a custom palette."""
        palette_manager = PaletteManager()
        custom_palette = ["#ff0000", "#00ff00", "#0000ff"]
        palette_manager.add_palette("custom", custom_palette)
        self.assertIn("custom", palette_manager.get_palette_names())
        self.assertEqual(palette_manager.get_palette("custom"), custom_palette)


if __name__ == "__main__":
    unittest.main()
