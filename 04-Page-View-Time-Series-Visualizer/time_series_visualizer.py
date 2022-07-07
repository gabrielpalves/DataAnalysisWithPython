import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv', index_col='date', parse_dates=['date'])

# Clean data
df = df.drop( df.index[(df['value'] < df['value'].quantile(0.025)) | (df['value'] > df['value'].quantile(1-0.025))] )


def draw_line_plot():
    # Draw line plot
    x = df.index.values#['date']
    y = df['value']

    fig, ax = plt.subplots(figsize=(7, 4), layout='constrained')
    ax.plot(x, y, linewidth=2.0)
    ax.set_title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019")
    ax.set_xlabel('Date')  # Add an x-label to the axes.
    ax.set_ylabel('Page Views')  # Add a y-label to the axes.

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy()
    df_bar['month'] = df.index.month
    df_bar['Years'] = df.index.year
    df_bar['Months'] = pd.to_datetime(df_bar['month'], format='%m').dt.month_name().str.slice()

    # Draw bar plot
    width = 0.2  # the width of the bars

    fig, ax = plt.subplots()
    rects = []
    l = 0

    # sort months
    arr = df_bar['Months'].unique()
    idx_arr = np.array(0)
    for i in range(arr.shape[0]):
        idx = np.array(df_bar['month'].unique()) == i+1
        idx_arr = np.concatenate((idx_arr, np.where(idx)), axis=None)
    months = arr[idx_arr[1:]]

    # put data in a matrix [number of months x number of years]
    data = np.zeros((months.shape[0], df_bar['Years'].unique().shape[0]))
    for i in months:
        k = 0
        for j in df_bar['Years'].unique():
            if all(df_bar.loc[df_bar['Years'] == j, 'Months'] != i):
                data[l,k] = 0
            else:
                data[l,k] = df_bar.loc[(df_bar['Years'] == j) & (df_bar['Months'] == i), 'value'].mean()
            k = k + 1
        l = l + 1

    x = np.arange(data.shape[1])
    for i in np.arange(data.shape[0]):
        rects.append(ax.bar(x -width/2 + width/12*i, data[i,:], width/12, label=months[i]))

    ax.set_xticks(np.arange(df_bar['Years'].unique().shape[0]), df_bar['Years'].unique())
    ax.set_xlabel('Years')
    ax.set_ylabel('Average Page Views')
    ax.legend()
        
    # plt.show()

    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    print(df_box.head(-3))

    # Draw box plots (using Seaborn)
    
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    sns.boxplot(ax=axes[0], x="year", y="value", data=df_box)

    df_box['month'] = pd.Categorical(df_box['month'], ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
    sns.boxplot(ax=axes[1], x="month", y="value", data=df_box.sort_values('month'))

    axes[0].set_title("Year-wise Box Plot (Trend)")
    axes[1].set_title("Month-wise Box Plot (Seasonality)")

    axes[0].set_xlabel("Year")
    axes[1].set_xlabel("Month")

    axes[0].set_ylabel("Page Views")
    axes[1].set_ylabel("Page Views")

    # plt.show()

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
