"""
Example usage of BlazingPlot.

This script demonstrates how to use BlazingPlot for data visualization.
"""

import polars as pl
import numpy as np
import pandas as pd
from blazingplot import Dashboard
from blazingplot.visualizations.base import (
    ScatterPlot, LineChart, BarChart, BubbleChart, PieChart
)

# Generate sample data
def generate_sample_data(rows=1000):
    """Generate sample data for demonstration."""
    # Create date range
    dates = pd.date_range(start='2023-01-01', periods=rows)
    
    # Create categories
    categories = np.random.choice(['A', 'B', 'C', 'D', 'E'], size=rows)
    
    # Create numeric data
    x = np.linspace(0, 10, rows)
    y = np.sin(x) + np.random.normal(0, 0.2, rows)
    z = np.cos(x) + np.random.normal(0, 0.2, rows)
    values = np.random.randint(10, 100, rows)
    
    # Create DataFrame
    data = {
        'date': dates,
        'category': categories,
        'x': x,
        'y': y,
        'z': z,
        'values': values
    }
    
    return pl.DataFrame(data)

# Create sample data
data = generate_sample_data()

# Example 1: Using the Dashboard
print("Example 1: Creating a Dashboard")
dashboard = Dashboard(data, title="BlazingPlot Demo Dashboard")
print("Dashboard created. Run dashboard.run(mode='jupyter') in a Jupyter notebook")
print("or dashboard.run(mode='standalone') for a standalone web application.")

# Example 2: Using individual visualizations
print("\nExample 2: Using individual visualizations")

# Scatter Plot
scatter = ScatterPlot(
    data, 
    x='x', 
    y='y', 
    color='category',
    title="Scatter Plot Example"
)
scatter_fig = scatter.plot()
print("Scatter plot created")

# Line Chart
line = LineChart(
    data, 
    x='x', 
    y=['y', 'z'], 
    title="Line Chart Example"
)
line_fig = line.plot()
print("Line chart created")

# Bar Chart
# Group by category and calculate mean values
bar_data = data.group_by('category').agg(pl.col('values').mean())
bar = BarChart(
    bar_data, 
    x='category', 
    y='values', 
    title="Bar Chart Example"
)
bar_fig = bar.plot()
print("Bar chart created")

# Bubble Chart
bubble = BubbleChart(
    data, 
    x='x', 
    y='y', 
    size='values',
    color='category',
    title="Bubble Chart Example"
)
bubble_fig = bubble.plot()
print("Bubble chart created")

# Pie Chart
pie_data = data.group_by('category').agg(pl.col('values').sum())
pie = PieChart(
    pie_data, 
    names='category', 
    values='values', 
    title="Pie Chart Example"
)
pie_fig = pie.plot()
print("Pie chart created")

print("\nTo display these plots in a Jupyter notebook, simply call:")
print("scatter_fig.show()")
print("line_fig.show()")
print("bar_fig.show()")
print("bubble_fig.show()")
print("pie_fig.show()")

print("\nTo export plots:")
print("scatter.export_html('scatter.html')")
print("scatter.export_png('scatter.png')")

# Example 3: Customizing palettes
print("\nExample 3: Customizing palettes")
from blazingplot.utils.export import PaletteManager

palette_manager = PaletteManager()
print(f"Available palettes: {palette_manager.get_palette_names()}")

print("\nTo create a dashboard with a custom palette:")
print("dashboard = Dashboard(data, title='Custom Palette Dashboard', custom_palette='viridis')")

print("\nTo add a custom palette:")
print("palette_manager.add_palette('my_palette', ['#ff0000', '#00ff00', '#0000ff'])")
print("dashboard = Dashboard(data, title='My Dashboard', custom_palette='my_palette')")

# Example 4: Performance considerations
print("\nExample 4: Performance considerations")
print("For large datasets, BlazingPlot leverages Polars for efficient data transformations.")
print("When working with millions of rows, consider:")
print("1. Pre-aggregate data when possible")
print("2. Use filtering to reduce dataset size")
print("3. For time series, consider resampling to reduce points")

print("\nExample of pre-aggregation:")
print("aggregated_data = data.group_by(['category', 'date']).agg(")
print("    pl.col('values').mean().alias('avg_value'),")
print("    pl.col('values').count().alias('count')")
print(")")

print("\nBlazingPlot is now ready to use! Enjoy fast and fully controlled data visualization.")
