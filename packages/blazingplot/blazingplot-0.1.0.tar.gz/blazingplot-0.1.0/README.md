# BlazingPlot

[![Test](https://github.com/username/blazingplot/actions/workflows/test.yml/badge.svg)](https://github.com/username/blazingplot/actions/workflows/test.yml)
[![PyPI version](https://badge.fury.io/py/blazingplot.svg)](https://badge.fury.io/py/blazingplot)
[![Python Version](https://img.shields.io/pypi/pyversions/blazingplot.svg)](https://pypi.org/project/blazingplot/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A Fast and Fully Controlled Data Visualization Library built on top of Plotly, Dash, and Polars.

## Features

- Interactive dashboards in both Jupyter Notebooks and standalone web applications
- High-performance data transformations using Polars
- Customizable visualizations with full control over chart elements
- Export capabilities for charts (PNG, HTML) and data (CSV)
- Customizable color palettes
- Modular, object-oriented design for extensibility

## Installation

```bash
pip install blazingplot
```

## Quick Start

```python
import polars as pl
from blazingplot import Dashboard

# Create a sample DataFrame
data = pl.DataFrame({
    'x': [1, 2, 3, 4, 5],
    'y': [10, 20, 15, 25, 30],
    'category': ['A', 'B', 'A', 'B', 'A']
})

# Create a dashboard
dashboard = Dashboard(data, title="My Dashboard")

# Run the dashboard in a Jupyter notebook
dashboard.run(mode="jupyter")

# Or run as a standalone web application
# dashboard.run(mode="standalone", port=8050)
```

## Visualization Types

BlazingPlot supports the following visualization types:

- Scatter Plot
- Line Chart
- Bar Chart
- Bubble Chart
- Pie Chart
- Box Plot
- Histogram
- 2D Histogram
- Time Series
- Stock Chart
- Error Bars
- Map Visualizations (Bubble Map, Tile Choropleth, Line on Tiles)
- Tables (Simple Table, Pivot Table)

## Using Individual Visualizations

You can also use the visualization classes directly:

```python
from blazingplot.visualizations.base import ScatterPlot

# Create a scatter plot
scatter = ScatterPlot(data, x='x', y='y', color='category', title="My Scatter Plot")

# Plot the visualization
fig = scatter.plot()

# Export to HTML
scatter.export_html("scatter.html")

# Export to PNG
scatter.export_png("scatter.png")
```

## Dashboard Layout

The dashboard is divided into three main sections:

1. **Column Selector**: Select columns from your dataset
2. **Visualization Controls**: Configure your visualization
3. **Visualization Display**: View and interact with your visualization

## Performance

BlazingPlot is designed for performance, leveraging Polars for data transformations
and Plotly for rendering. It can handle large datasets efficiently.

## Customization

You can customize the appearance of your visualizations using color palettes:

```python
# Create a dashboard with a custom color palette
dashboard = Dashboard(data, title="My Dashboard", custom_palette="viridis")
```

## Development

### Setup

1. Clone the repository
```bash
git clone https://github.com/username/blazingplot.git
cd blazingplot
```

2. Install development dependencies
```bash
pip install -e ".[dev]"
```

### Testing

```bash
pytest
```

### Building

```bash
python -m build
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
