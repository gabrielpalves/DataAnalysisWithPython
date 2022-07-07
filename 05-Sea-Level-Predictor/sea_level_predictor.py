from unittest import removeResult
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import linregress

def draw_plot():
    # Read data from file
    df = pd.read_csv('epa-sea-level.csv')
    print(df.head(-3))

    # Create scatter plot
    plt.scatter('Year', 'CSIRO Adjusted Sea Level', alpha=0.5, data=df)

    # Create first line of best fit
    res = linregress(df['Year'], df['CSIRO Adjusted Sea Level'])
    x = df['Year']
    to_append = range(x.max()+1, 2051)
    x = x.append(pd.Series(to_append))
    
    plt.plot(x, res.intercept + res.slope*x, 'r', label='fitted line')

    # Create second line of best fit
    df2 = df.loc[df['Year'] >= 2000]
    res2 = linregress(df2['Year'], df2['CSIRO Adjusted Sea Level'])

    x2 = df2['Year']
    to_append = range(x2.max()+1, 2051)
    x2 = x2.append(pd.Series(to_append))
    
    plt.plot(x2, res2.intercept + res2.slope*x2, 'g', label='fitted line from 2000')

    # Add labels and title
    plt.xlabel('Year')
    plt.ylabel('Sea Level (inches)')
    plt.title('Rise in Sea Level')
    
    # Save plot and return data for testing (DO NOT MODIFY)
    plt.savefig('sea_level_plot.png')
    return plt.gca()
