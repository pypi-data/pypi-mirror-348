"""
Performance testing and validation for BlazingPlot.

This module provides utilities for testing the performance and
interactivity of BlazingPlot visualizations and dashboards.
"""

import polars as pl
import pandas as pd
import numpy as np
import time
import plotly.express as px
from typing import Dict, List, Optional, Union, Tuple, Any

from blazingplot.visualizations.base import (
    ScatterPlot, LineChart, BarChart, BubbleChart, PieChart
)


def generate_test_data(rows: int = 10000, cols: int = 10) -> pl.DataFrame:
    """
    Generate test data for performance testing.
    
    Parameters
    ----------
    rows : int, optional
        The number of rows to generate.
    cols : int, optional
        The number of columns to generate.
        
    Returns
    -------
    polars.DataFrame
        A DataFrame with random data.
    """
    # Generate column names
    col_names = [f"col_{i}" for i in range(cols)]
    
    # Generate random data
    data = {}
    for i, col in enumerate(col_names):
        if i == 0:
            # First column as dates
            data[col] = pd.date_range(start='2020-01-01', periods=rows).tolist()
        elif i == 1:
            # Second column as categories
            categories = ['A', 'B', 'C', 'D', 'E']
            data[col] = np.random.choice(categories, size=rows).tolist()
        else:
            # Numeric columns
            data[col] = np.random.randn(rows).tolist()
    
    # Create DataFrame
    df = pl.DataFrame(data)
    return df


def benchmark_visualization(viz_class, data: pl.DataFrame, **kwargs) -> Dict[str, float]:
    """
    Benchmark the performance of a visualization class.
    
    Parameters
    ----------
    viz_class : class
        The visualization class to benchmark.
    data : polars.DataFrame
        The data to visualize.
    **kwargs
        Additional keyword arguments to pass to the visualization class.
        
    Returns
    -------
    dict
        A dictionary of benchmark results.
    """
    results = {}
    
    # Measure initialization time
    start_time = time.time()
    viz = viz_class(data, **kwargs)
    init_time = time.time() - start_time
    results['init_time'] = init_time
    
    # Measure plot time
    start_time = time.time()
    fig = viz.plot()
    plot_time = time.time() - start_time
    results['plot_time'] = plot_time
    
    # Measure export time
    start_time = time.time()
    viz.export_html()
    export_html_time = time.time() - start_time
    results['export_html_time'] = export_html_time
    
    start_time = time.time()
    viz.export_png()
    export_png_time = time.time() - start_time
    results['export_png_time'] = export_png_time
    
    # Total time
    results['total_time'] = init_time + plot_time + export_html_time + export_png_time
    
    return results


def run_performance_tests(data_sizes: List[int] = [1000, 10000, 100000]) -> Dict[str, Dict[str, Dict[str, float]]]:
    """
    Run performance tests on various visualization types with different data sizes.
    
    Parameters
    ----------
    data_sizes : list, optional
        The data sizes to test.
        
    Returns
    -------
    dict
        A dictionary of benchmark results.
    """
    results = {}
    
    for size in data_sizes:
        print(f"Testing with {size} rows...")
        data = generate_test_data(rows=size)
        
        size_results = {}
        
        # Test ScatterPlot
        print("  Testing ScatterPlot...")
        size_results['scatter'] = benchmark_visualization(
            ScatterPlot, data, x='col_2', y='col_3', color='col_1'
        )
        
        # Test LineChart
        print("  Testing LineChart...")
        size_results['line'] = benchmark_visualization(
            LineChart, data, x='col_0', y='col_3', color='col_1'
        )
        
        # Test BarChart
        print("  Testing BarChart...")
        size_results['bar'] = benchmark_visualization(
            BarChart, data, x='col_1', y='col_3'
        )
        
        # Test BubbleChart
        print("  Testing BubbleChart...")
        size_results['bubble'] = benchmark_visualization(
            BubbleChart, data, x='col_2', y='col_3', size='col_4', color='col_1'
        )
        
        # Test PieChart (with smaller subset for performance)
        print("  Testing PieChart...")
        pie_data = data.filter(pl.col('col_1') == 'A').head(100)
        size_results['pie'] = benchmark_visualization(
            PieChart, pie_data, names='col_1', values='col_3'
        )
        
        results[str(size)] = size_results
    
    return results


def print_benchmark_results(results: Dict[str, Dict[str, Dict[str, float]]]) -> None:
    """
    Print benchmark results in a readable format.
    
    Parameters
    ----------
    results : dict
        The benchmark results.
    """
    print("\nBenchmark Results (times in seconds):")
    print("=" * 80)
    
    # Print header
    header = "| Data Size | Visualization | Init Time | Plot Time | HTML Export | PNG Export | Total Time |"
    separator = "|" + "-" * 10 + "|" + "-" * 14 + "|" + "-" * 10 + "|" + "-" * 10 + "|" + "-" * 12 + "|" + "-" * 11 + "|" + "-" * 11 + "|"
    
    print(header)
    print(separator)
    
    # Print results
    for size, size_results in results.items():
        for viz_type, viz_results in size_results.items():
            row = f"| {size:>9} | {viz_type:>12} | {viz_results['init_time']:>9.4f} | {viz_results['plot_time']:>9.4f} | {viz_results['export_html_time']:>11.4f} | {viz_results['export_png_time']:>10.4f} | {viz_results['total_time']:>10.4f} |"
            print(row)
    
    print("=" * 80)


if __name__ == "__main__":
    # Run performance tests
    results = run_performance_tests()
    
    # Print results
    print_benchmark_results(results)
