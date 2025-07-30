import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from datetime import datetime
# Set the style for better-looking plots
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("husl")

def plot_feature_line_graph(data, feature_name, date_column, highlight_month_year=None):
    """
    Creates a line plot showing a feature's values over time with outliers highlighted.
    
    Args:
        data: DataFrame containing the data
        feature_name: Name of the feature to plot
        date_column: Name of the date column
        highlight_month_year: Optional month/year to highlight (e.g., 'Nov 2023')
    """
    # Ensure date column is datetime type
    if not pd.api.types.is_datetime64_any_dtype(data[date_column]):
        data = data.copy()
        data[date_column] = pd.to_datetime(data[date_column])
    
    # Sort by date
    data_sorted = data.sort_values(by=date_column)
    
    # Calculate statistics for the entire dataset
    mean_val = float(data[feature_name].mean())
    std_val = float(data[feature_name].std())
    lower_bound = mean_val - 3*std_val
    upper_bound = mean_val + 3*std_val
    
    # Create figure
    plt.figure(figsize=(14, 8))
    
    # Plot the feature values
    plt.plot(data_sorted[date_column], data_sorted[feature_name], 
             linestyle='-', marker='.', markersize=5, alpha=0.6, label=feature_name)
    
    # Add horizontal lines for mean and ±3 std devs
    plt.axhline(y=mean_val, color='red', linestyle='--', 
                label=f'Mean: {mean_val:.2f}')
    plt.axhline(y=lower_bound, color='green', linestyle='--', 
                label=f'Mean-3σ: {lower_bound:.2f}')
    plt.axhline(y=upper_bound, color='green', linestyle='--', 
                label=f'Mean+3σ: {upper_bound:.2f}')
    
    # Highlight outliers
    outliers = data_sorted[(data_sorted[feature_name] < lower_bound) | 
                         (data_sorted[feature_name] > upper_bound)]
    if not outliers.empty:
        plt.scatter(outliers[date_column], outliers[feature_name], 
                   color='red', s=80, alpha=0.8, marker='X', 
                   label=f'Outliers ({len(outliers)})')
    
    # Highlight specific month/year if provided
    if highlight_month_year:
        try:
            highlight_date = pd.to_datetime(highlight_month_year)
            month, year = highlight_date.month, highlight_date.year
            
            highlighted_data = data_sorted[
                (data_sorted[date_column].dt.month == month) & 
                (data_sorted[date_column].dt.year == year)
            ]
            
            if not highlighted_data.empty:
                plt.scatter(highlighted_data[date_column], highlighted_data[feature_name],
                           color='orange', s=120, alpha=0.5, marker='o', edgecolors='k',
                           label=f'{highlight_month_year} ({len(highlighted_data)} points)')
                
                # Add shaded background for highlighted month
                date_min = highlighted_data[date_column].min()
                date_max = highlighted_data[date_column].max()
                plt.axvspan(date_min, date_max, alpha=0.1, color='orange')
        except:
            print(f"Could not highlight {highlight_month_year}")
    
    # Add labels and title
    plt.title(f'Time Series of {feature_name}', fontsize=16)
    plt.xlabel('Date', fontsize=12)
    plt.ylabel(feature_name, fontsize=12)
    plt.grid(True, alpha=0.3)
    
    # Format x-axis for dates
    plt.gcf().autofmt_xdate()
    
    # Add legend
    plt.legend(loc='best')
    
    return plt

def plot_feature_line_graph_date_range(data, feature_name, date_column, start_date=None, end_date=None, highlight_ranges=None):
    """
    Creates a line plot showing a feature's values over a specific date range with optional highlighted periods.
    
    Args:
        data: DataFrame containing the data
        feature_name: Name of the feature to plot
        date_column: Name of the date column
        start_date: Start date for filtering (string or datetime)
        end_date: End date for filtering (string or datetime)
        highlight_ranges: List of tuples with (start_date, end_date, label) for highlighting
    """
    # Ensure date column is datetime type
    if not pd.api.types.is_datetime64_any_dtype(data[date_column]):
        data = data.copy()
        data[date_column] = pd.to_datetime(data[date_column])
    
    # Filter by date range if specified
    if start_date or end_date:
        data_filtered = data.copy()
        if start_date:
            start_date = pd.to_datetime(start_date)
            data_filtered = data_filtered[data_filtered[date_column] >= start_date]
        if end_date:
            end_date = pd.to_datetime(end_date)
            data_filtered = data_filtered[data_filtered[date_column] <= end_date]
    else:
        data_filtered = data
    
    # Sort by date
    data_sorted = data_filtered.sort_values(by=date_column)
    
    # Calculate statistics for the filtered dataset
    mean_val = float(data_sorted[feature_name].mean())
    std_val = float(data_sorted[feature_name].std())
    lower_bound = mean_val - 3*std_val
    upper_bound = mean_val + 3*std_val
    
    # Create figure
    plt.figure(figsize=(14, 8))
    
    # Plot the feature values
    plt.plot(data_sorted[date_column], data_sorted[feature_name], 
             linestyle='-', marker='.', markersize=5, alpha=0.6, label=feature_name)
    
    # Add horizontal lines for mean and ±3 std devs
    plt.axhline(y=mean_val, color='red', linestyle='--', 
                label=f'Mean: {mean_val:.2f}')
    plt.axhline(y=lower_bound, color='green', linestyle='--', 
                label=f'Mean-3σ: {lower_bound:.2f}')
    plt.axhline(y=upper_bound, color='green', linestyle='--', 
                label=f'Mean+3σ: {upper_bound:.2f}')
    
    # Highlight outliers
    outliers = data_sorted[(data_sorted[feature_name] < lower_bound) | 
                         (data_sorted[feature_name] > upper_bound)]
    if not outliers.empty:
        plt.scatter(outliers[date_column], outliers[feature_name], 
                   color='red', s=80, alpha=0.8, marker='X', 
                   label=f'Outliers ({len(outliers)})')
    
    # Highlight specific date ranges if provided
    if highlight_ranges:
        colors = ['orange', 'purple', 'cyan', 'magenta', 'yellow']  # Multiple colors for different ranges
        
        for i, (range_start, range_end, range_label) in enumerate(highlight_ranges):
            try:
                range_start = pd.to_datetime(range_start)
                range_end = pd.to_datetime(range_end)
                
                highlighted_data = data_sorted[
                    (data_sorted[date_column] >= range_start) & 
                    (data_sorted[date_column] <= range_end)
                ]
                
                if not highlighted_data.empty:
                    color = colors[i % len(colors)]  # Cycle through colors
                    
                    plt.scatter(highlighted_data[date_column], highlighted_data[feature_name],
                               color=color, s=80, alpha=0.7, marker='o', edgecolors='k',
                               label=f'{range_label} ({len(highlighted_data)} points)')
                    
                    # Add shaded background for highlighted range
                    plt.axvspan(range_start, range_end, alpha=0.1, color=color)
            except Exception as e:
                print(f"Could not highlight range {range_label}: {e}")
    
    # Add rolling average
    try:
        window_size = max(7, len(data_sorted) // 20)  # Adaptive window size
        rolling_avg = data_sorted[feature_name].rolling(window=window_size, center=True).mean()
        plt.plot(data_sorted[date_column], rolling_avg, 
                color='blue', linewidth=2, linestyle='-.',
                label=f'{window_size}-point Rolling Avg')
    except Exception as e:
        print(f"Could not calculate rolling average: {e}")
    
    # Add labels and title
    date_range_text = ""
    if start_date and end_date:
        date_range_text = f" ({start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')})"
    elif start_date:
        date_range_text = f" (from {start_date.strftime('%Y-%m-%d')})"
    elif end_date:
        date_range_text = f" (until {end_date.strftime('%Y-%m-%d')})"
        
    plt.title(f'Time Series of {feature_name}{date_range_text}', fontsize=16)
    plt.xlabel('Date', fontsize=12)
    plt.ylabel(feature_name, fontsize=12)
    plt.grid(True, alpha=0.3)
    
    # Format x-axis for dates
    plt.gcf().autofmt_xdate()
    
    # Add legend
    plt.legend(loc='best')
    return plt
    