import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Import data
df = pd.read_csv('medical_examination.csv')

# Add 'overweight' column+
BMI = df['weight']/((df['height']/100)**2)
df['overweight'] = pd.Series(BMI > 25, dtype='int64')

# Normalize data by making 0 always good and 1 always bad. If the value of 'cholesterol' or 'gluc' is 1, make the value 0. If the value is more than 1, make the value 1.
df['cholesterol'] = pd.Series(df['cholesterol'] > 1, dtype='int64')
df['gluc'] = pd.Series(df['gluc'] > 1, dtype='int64')

# Draw Categorical Plot
def draw_cat_plot():
    # Create DataFrame for cat plot using `pd.melt` using just the values from 'cholesterol', 'gluc', 'smoke', 'alco', 'active', and 'overweight'.
    list_vars = ['active', 'alco', 'cholesterol', 'gluc', 'overweight', 'smoke']
    df_cat = pd.melt(df, id_vars='cardio', value_vars=list_vars)

    # Group and reformat the data to split it by 'cardio'. Show the counts of each feature. You will have to rename one of the columns for the catplot to work correctly.
    df_cat = pd.concat([df_cat.loc[df_cat['cardio'] == 0], df_cat.loc[df_cat['cardio'] == 1]])

    frames = []
    for j in range(2):
        for k in range(2):
            for i in list_vars:
                frames.append(pd.DataFrame({'cardio': [j], 'variable': i, 'value': k, 'total': [df_cat.loc[(df_cat['cardio'] == j) & (df_cat['variable'] == i) & (df_cat['value'] == k)].shape[0]]}))
    
    df_cat = pd.concat(frames)

    # Draw the catplot with 'sns.catplot()'
    fig = sns.catplot(x="variable", y="total", hue="value", kind="bar", data=df_cat, col_wrap=2, col='cardio')

    # Do not modify the next two lines
    fig.savefig('catplot.png')
    return fig


# Draw Heat Map
def draw_heat_map():
    # Clean the data
    df_heat = df.drop(df.index[(df['ap_lo'] > df['ap_hi']) | (df['height'] < df['height'].quantile(0.025)) | (df['height'] > df['height'].quantile(0.975)) |
     (df['weight'] < df['weight'].quantile(0.025)) | (df['weight'] > df['weight'].quantile(0.975))])

    # Calculate the correlation matrix
    corr = df_heat.corr()

    # Generate a mask for the upper triangle
    mask = np.zeros_like(corr)
    mask[np.triu_indices_from(mask)] = True

    # Set up the matplotlib figure
    fig, ax = plt.subplots()

    # Draw the heatmap with 'sns.heatmap()'
    with sns.axes_style("white"):
        ax = sns.heatmap(corr, mask=mask, square=True, annot=True, fmt=".1f")

    fig.set_size_inches(15, 15)
    # Do not modify the next two lines
    fig.savefig('heatmap.png')
    return fig

