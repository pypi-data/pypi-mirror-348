# TS-Viz: Time Series Visualization Library


**ts-viz** is a Python package for visualizing and analyzing time series data, with built-in tools for:
- Outlier detection
- Histograms with statistical markers
- Time series plots with rolling averages
- Feature correlation scatter plots with trendlines

Built using `pandas`, `matplotlib`, and `seaborn`, this library simplifies exploratory data analysis (EDA) for time-series-heavy applications.

## 🧩 Features

* ✅ Plot histograms with mean and ±3 standard deviation lines
* ✅ Detect and visualize outliers for a given feature by month
* ✅ Plot time series trends with outlier and date-range highlights
* ✅ Explore feature-to-feature correlation with outlier and trend detection

## 🚀 Usage Examples

### 1. 📊 Histogram with Statistical Markers

```python
from ts_viz import plot_histogram_with_markers
import matplotlib.pyplot as plt

fig, ax = plt.subplots()
plot_histogram_with_markers(df, 'your_column_name', ax)
plt.show()
```

### 2. 🧯 Outlier Detection (Optional Month-Year Filter)

```python
from ts_viz import identify_and_plot_outliers

fig, ax = plt.subplots()
results = identify_and_plot_outliers(
    data=df,
    feature_name='your_column',
    date_column='timestamp',
    month_year='2023-11',  # optional, can be None
    ax=ax
)
plt.show()

# Access results:
print(results['total_outliers'], results['percent_outliers'])
```

### 3. 📈 Line Plot Over Time

```python
from ts_viz import plot_feature_line_graph

plot = plot_feature_line_graph(
    data=df,
    feature_name='temperature',
    date_column='timestamp',
    highlight_month_year='2023-11'
)
plot.show()
```

### 4. 📅 Line Plot for Custom Date Ranges with Highlights

```python
from ts_viz import plot_feature_line_graph_date_range

plot = plot_feature_line_graph_date_range(
    data=df,
    feature_name='pressure',
    date_column='timestamp',
    start_date='2023-01-01',
    end_date='2023-06-30',
    highlight_ranges=[
        ('2023-02-01', '2023-02-10', 'Batch A'),
        ('2023-05-15', '2023-05-20', 'Batch B')
    ]
)
plot.show()
```

### 5. 🔗 Correlation Between Two Features

```python
from ts_viz import plot_feature_correlation

plot = plot_feature_correlation(
    data=df,
    feature_x='temperature',
    feature_y='pressure',
    date_column='timestamp',
    highlight_month_year='2023-03'
)
plot.show()
```

## 📦 Installation

```bash
pip3 install ts-viz
```

## 🧰 Requirements

* Python >= 3.11
* pandas >= 2.1.0
* numpy >= 1.26.0
* matplotlib
* seaborn
* datetime

## 📄 License

This project is licensed under the MIT License – see the LICENSE file for details.

## 👤 Author

Created by Chitra Kumar Sai Chenuri Venkata. Contributions welcome!

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request
