# -*- coding: utf-8 -*-
"""Data Analysis on EV.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1lQolp2NRpfK_Is53tHbY69JwB91Fkp8K
"""

import pandas as pd

df=pd.read_csv('dataset.csv')
df.head()

#Univariate analysis
#1.Count of vehicles 'Make'
import matplotlib.pyplot as plt
import seaborn as sns

sns.set(style="whitegrid")
plt.figure(figsize=(10, 6))
sns.countplot(data=df, y='Make', order=df['Make'].value_counts().index)
plt.title('Count of Vehicles by Make')
plt.xlabel('Count')
plt.ylabel('Vehicle Make')
plt.show()

#2.Distribution of Model year
plt.figure(figsize=(10, 6))
sns.histplot(data=df, x='Model Year', bins=20, kde=True)
plt.title('Distribution of Vehicle Model Year')
plt.xlabel('Model Year')
plt.ylabel('Frequency')
plt.show()



#3.Distribution of electric vehicle type
plt.figure(figsize=(8, 5))
sns.countplot(data=df, x='Electric Vehicle Type',
              order=df['Electric Vehicle Type'].value_counts().index)
plt.title('Distribution of Electric Vehicle Type')
plt.xlabel('Electric Vehicle Type')
plt.ylabel('Count')
plt.xticks(rotation=45)
plt.show()

#Distribution of 'Electric range'
plt.figure(figsize=(10, 6))
sns.histplot(data=df, x='Electric Range', bins=30, kde=True)
plt.title('Distribution of Electric Range')
plt.xlabel('Electric Range (miles)')
plt.ylabel('Frequency')
plt.show()

#Barplot for Average electrtic range by electric vehicle type
import numpy as np
plt.figure(figsize=(10, 6))
sns.barplot(data=df, x='Electric Vehicle Type', y='Electric Range',
            estimator=np.mean, order=df['Electric Vehicle Type'].value_counts().index)
plt.title('Average Electric Range by Electric Vehicle Type')
plt.xlabel('Electric Vehicle Type')
plt.ylabel('Average Electric Range (miles)')
plt.xticks(rotation=45)
plt.show()

#BEV has higher average electric range compared to PHEV

plt.figure(figsize=(10, 6))
sns.boxplot(data=df, y='Electric Range')
plt.title('Box Plot of Electric Range')
plt.ylabel('Electric Range (miles)')
plt.show()

df['Electric Range'].plot(kind="box",figsize=(10,6))

num_col=df.select_dtypes(include=['float64', 'int64']).columns
for col in num_col:
  plt.figure(figsize=(10,6))
  sns.boxplot(data=df, y=col)
  plt.title(f'Box Plot of {col}')
  plt.ylabel(col)
  plt.show()

#Some vehicles like Tesla offer exceptionally high electric ranges

# Frequency distribution for each categorical column
categorical_columns = ['Electric Vehicle Type', 'Make', 'State']

for column in categorical_columns:
    plt.figure(figsize=(10, 6))
    sns.countplot(data=df, x=column, order=df[column].value_counts().index)
    plt.title(f'Frequency Distribution of {column}')
    plt.xlabel(column)
    plt.ylabel('Count')
    plt.xticks(rotation=45)
    plt.show()

#Bivariare analysis
# Scatter plot to see the relationship between Electric Range and Base MSRP
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df, x='Base MSRP', y='Electric Range')
plt.title('Electric Range vs. Base MSRP')
plt.xlabel('Base MSRP ($)')
plt.ylabel('Electric Range (miles)')
plt.show()

# Hexbin plot for Electric Range vs Base MSRP
df.plot.hexbin(x='Base MSRP', y='Electric Range', gridsize=30, cmap='Blues', figsize=(10, 6))
plt.title('Hexbin Plot: Electric Range vs. Base MSRP')
plt.xlabel('Base MSRP ($)')
plt.ylabel('Electric Range (miles)')
plt.show()

#More expensive vehicles tend to have a longer electric range

# Barplot to show average Electric Range by Vehicle Type
plt.figure(figsize=(10, 6))
sns.barplot(data=df, x='Electric Vehicle Type', y='Electric Range')
plt.title('Average Electric Range by Vehicle Type')
plt.xlabel('Electric Vehicle Type')
plt.ylabel('Average Electric Range (miles)')
plt.show()
#BEV has higher average range compared to PHEV

#stacked bar plot for Make and Electric Vehicle Type
ct = pd.crosstab(df['Make'], df['Electric Vehicle Type'])
ct.plot(kind='bar', stacked=True, figsize=(12, 6), colormap='Set2')
plt.title('Stacked Bar Plot: Make vs Electric Vehicle Type')
plt.xlabel('Make')
plt.ylabel('Count')
plt.xticks(rotation=90)
plt.show()

#Manufacturers focus more in BEV like TESLA

#Choroplet
! pip install plotly

import plotly.express as px

state_ev_count = df.groupby(['State', 'Model Year']).size().reset_index(name='EV Count')
state_ev_count.head()

fig = px.choropleth(state_ev_count,
                    locations='State',
                    locationmode="USA-states",
                    color='EV Count',
                    hover_name='EV Count',
                    scope="usa",
                    title="Number of Electric Vehicles by State",
                    color_continuous_scale="Viridis")
fig.show()

fig1 = px.choropleth(state_ev_count,
                    locations='State',
                    locationmode="USA-states",
                    color='EV Count',
                     hover_name='EV Count',
                    animation_frame='Model Year',
                    scope="usa",
                    title="Electric Vehicles by State Over Time",
                    color_continuous_scale="Viridis")

fig1.show()

#Racing bar plot

! pip install bar-chart-race

import bar_chart_race as bcr

ev_make_year_count = df.groupby(['Model Year', 'Make']).size().unstack(fill_value=0)
ev_make_year_count.head()

bcr.bar_chart_race(
    df=ev_make_year_count,
    filename='ev_racing_bar_plot.mp4',
    orientation='h',
    sort='desc',
    n_bars=10,
    steps_per_period=45,
    period_length=3000,
    title = 'Yearly Count of EV Makes',
    bar_kwargs={'alpha': 0.99},
    period_label={'x': 0.95, 'y': 0.15, 'ha': 'right', 'size': 72, 'weight': 'semibold'},

    filter_column_colors=True
)

from IPython.display import Video
Video('ev_racing_bar_plot.mp4', embed=True)
