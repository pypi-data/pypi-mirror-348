import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from datetime import datetime

# Set the style for better-looking plots
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("husl")

def plot_histogram_with_markers(data, feature_name, ax):
    mean_val = float(data[feature_name].mean())
    std_val = float(data[feature_name].std())
    
    sns.histplot(data[feature_name], kde=True, ax=ax)
    ax.axvline(mean_val, color='red', linestyle='--', linewidth=1.5, label=f'Mean: {mean_val:.2f}')
    ax.axvline(mean_val - 3*std_val, color='green', linestyle='--', linewidth=1.5, label=f'Mean-3σ: {mean_val - 3*std_val:.2f}')
    ax.axvline(mean_val + 3*std_val, color='green', linestyle='--', linewidth=1.5, label=f'Mean+3σ: {mean_val + 3*std_val:.2f}')
    ax.set_title(f'Distribution of {feature_name}')
    ax.set_xlabel(feature_name)
    ax.set_ylabel('Frequency')
    ax.legend(fontsize='small')
    
    return {
        'mean': mean_val,
        'std': std_val,
        'lower_bound': mean_val - 3*std_val,
        'upper_bound': mean_val + 3*std_val
    }
