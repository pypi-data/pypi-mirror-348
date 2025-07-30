import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from datetime import datetime

# Set the style for better-looking plots
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("husl")

def plot_feature_correlation(data, feature_x, feature_y, date_column=None, highlight_month_year=None):
    """
    Creates a scatter plot showing correlation between two features with outliers highlighted.
    
    Args:
        data: DataFrame containing the data
        feature_x: Name of the feature for the x-axis
        feature_y: Name of the feature for the y-axis
        date_column: Optional name of the date column for filtering
        highlight_month_year: Optional month/year to highlight (e.g., 'Nov 2023')
    """
    # Create a copy of data to avoid modifying the original
    plot_data = data.copy()
    
    # Calculate statistics for outlier detection
    mean_x = float(plot_data[feature_x].mean())
    std_x = float(plot_data[feature_x].std())
    lower_x = mean_x - 3*std_x
    upper_x = mean_x + 3*std_x
    
    mean_y = float(plot_data[feature_y].mean())
    std_y = float(plot_data[feature_y].std())
    lower_y = mean_y - 3*std_y
    upper_y = mean_y + 3*std_y
    
    # Create figure
    plt.figure(figsize=(12, 10))
    
    # Default color for all points
    plot_data['color'] = 'blue'
    plot_data['size'] = 50
    plot_data['alpha'] = 0.6
    plot_data['marker'] = 'o'
    
    # Mark outliers
    outliers = plot_data[(plot_data[feature_x] < lower_x) | 
                         (plot_data[feature_x] > upper_x) | 
                         (plot_data[feature_y] < lower_y) | 
                         (plot_data[feature_y] > upper_y)]
    
    if not outliers.empty:
        plot_data.loc[outliers.index, 'color'] = 'red'
        plot_data.loc[outliers.index, 'marker'] = 'X'
        plot_data.loc[outliers.index, 'size'] = 80
    
    # Highlight specific month/year if provided
    highlighted_data = None
    if highlight_month_year and date_column:
        try:
            # Ensure date column is datetime
            if not pd.api.types.is_datetime64_any_dtype(plot_data[date_column]):
                plot_data[date_column] = pd.to_datetime(plot_data[date_column])
                
            highlight_date = pd.to_datetime(highlight_month_year)
            month, year = highlight_date.month, highlight_date.year
            
            highlighted_data = plot_data[
                (plot_data[date_column].dt.month == month) & 
                (plot_data[date_column].dt.year == year)
            ]
            
            if not highlighted_data.empty:
                plot_data.loc[highlighted_data.index, 'color'] = 'orange'
                plot_data.loc[highlighted_data.index, 'size'] = 100
                plot_data.loc[highlighted_data.index, 'alpha'] = 0.8
        except Exception as e:
            print(f"Could not highlight {highlight_month_year}: {e}")
    
    # Create groups for plotting and legend
    regular_points = plot_data[(plot_data['color'] == 'blue')]
    outlier_points = plot_data[(plot_data['color'] == 'red')]
    highlighted_points = plot_data[(plot_data['color'] == 'orange')]
    
    # Plot regular points
    if not regular_points.empty:
        plt.scatter(regular_points[feature_x], regular_points[feature_y], 
                   color='blue', s=50, alpha=0.6, 
                   label=f'Regular points ({len(regular_points)})')
    
    # Plot outliers
    if not outlier_points.empty:
        plt.scatter(outlier_points[feature_x], outlier_points[feature_y], 
                   color='red', s=80, alpha=0.7, marker='X',
                   label=f'Outliers ({len(outlier_points)})')
    
    # Plot highlighted points
    if not highlighted_points.empty:
        plt.scatter(highlighted_points[feature_x], highlighted_points[feature_y], 
                   color='orange', s=100, alpha=0.8, edgecolor='black',
                   label=f'{highlight_month_year} ({len(highlighted_points)})')
    
    # Calculate and display correlation coefficient
    corr = data[feature_x].corr(data[feature_y])
    plt.annotate(f'Correlation: {corr:.3f}', 
                xy=(0.05, 0.95), xycoords='axes fraction',
                bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="gray", alpha=0.8))
    
    # Add reference lines for mean and ±3 std dev
    plt.axvline(x=mean_x, color='gray', linestyle='--', alpha=0.5)
    plt.axvline(x=lower_x, color='gray', linestyle=':', alpha=0.5)
    plt.axvline(x=upper_x, color='gray', linestyle=':', alpha=0.5)
    
    plt.axhline(y=mean_y, color='gray', linestyle='--', alpha=0.5)
    plt.axhline(y=lower_y, color='gray', linestyle=':', alpha=0.5)
    plt.axhline(y=upper_y, color='gray', linestyle=':', alpha=0.5)
    
    # Add trend line
    try:
        # Filter out NaN or infinite values for the trend line calculation
        trend_data = data[[feature_x, feature_y]].dropna()
        trend_data = trend_data[(~np.isinf(trend_data[feature_x])) & (~np.isinf(trend_data[feature_y]))]
        
        if len(trend_data) > 1:  # Need at least two points for a line
            z = np.polyfit(trend_data[feature_x], trend_data[feature_y], 1)
            p = np.poly1d(z)
            
            # Use safe min and max values for the trend line plot
            x_min, x_max = np.percentile(trend_data[feature_x], [0, 100])
            x_trend = np.linspace(x_min, x_max, 100)
            
            plt.plot(x_trend, p(x_trend), "r--", alpha=0.7, linewidth=2, 
                    label=f'Trend: y={z[0]:.3f}x+{z[1]:.3f}')
        else:
            print(f"Not enough valid data points to calculate trend line for {feature_x} vs {feature_y}")
    except Exception as e:
        print(f"Could not calculate trend line: {e}")
        # Continue without trend line
    
    # Add labels and title
    plt.title(f'Correlation between {feature_x} and {feature_y}', fontsize=16)
    plt.xlabel(feature_x, fontsize=12)
    plt.ylabel(feature_y, fontsize=12)
    plt.grid(True, alpha=0.3)
    
    # Add legend
    plt.legend(loc='upper right')
    
    return plt