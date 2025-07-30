import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from datetime import datetime
# Set the style for better-looking plots
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("husl")

# Function to identify and plot outliers

def identify_and_plot_outliers(data, feature_name, date_column, month_year, ax):
    # Filter data for the specified month and year
    if month_year:
        # Extract month and year from date column
        if pd.api.types.is_datetime64_any_dtype(data[date_column]):
            month = pd.to_datetime(month_year).month
            year = pd.to_datetime(month_year).year
            monthly_data = data[
                (data[date_column].dt.month == month) & 
                (data[date_column].dt.year == year)
            ]
        else:
            # If date column is not datetime, try to convert it
            try:
                data[date_column] = pd.to_datetime(data[date_column])
                month = pd.to_datetime(month_year).month
                year = pd.to_datetime(month_year).year
                monthly_data = data[
                    (data[date_column].dt.month == month) & 
                    (data[date_column].dt.year == year)
                ]
            except:
                print(f"Warning: Could not filter by {month_year}, using all data")
                monthly_data = data
    else:
        monthly_data = data
    
    # Calculate statistics on the filtered data
    mean_val = float(monthly_data[feature_name].mean())
    std_val = float(monthly_data[feature_name].std())
    lower_bound = mean_val - 3*std_val
    upper_bound = mean_val + 3*std_val
    
    # Identify outliers
    outliers_below = monthly_data[monthly_data[feature_name] < lower_bound]
    outliers_above = monthly_data[monthly_data[feature_name] > upper_bound]
    outliers = pd.concat([outliers_below, outliers_above])
    
    # Plot histogram of the feature
    sns.histplot(monthly_data[feature_name], kde=True, ax=ax)
    
    # Add mean line
    ax.axvline(mean_val, color='red', linestyle='--', linewidth=1.5, 
               label=f'Mean: {mean_val:.2f}')
    
    # Add ±3 std dev lines
    ax.axvline(lower_bound, color='green', linestyle='--', linewidth=1.5,
               label=f'Mean-3σ: {lower_bound:.2f}')
    ax.axvline(upper_bound, color='green', linestyle='--', linewidth=1.5,
               label=f'Mean+3σ: {upper_bound:.2f}')
    
    # Highlight outliers
    if not outliers.empty:
        sns.rugplot(outliers[feature_name], ax=ax, color='red', height=0.05, 
                    label=f'Outliers ({len(outliers)})')
    
    # Set title and labels
    month_year_str = month_year if month_year else "All Data"
    ax.set_title(f'Distribution of {feature_name} ({month_year_str})')
    ax.set_xlabel(feature_name)
    ax.set_ylabel('Frequency')
    
    # Add legend
    ax.legend(fontsize='small')
    
    return {
        'feature': feature_name,
        'total_outliers': len(outliers),
        'percent_outliers': (len(outliers) / len(monthly_data)) * 100 if len(monthly_data) > 0 else 0,
        'lower_bound': lower_bound,
        'upper_bound': upper_bound,
        'outliers': outliers
    }
