# pandas is a software library written for the Python programming language for data manipulation and analysis.
import pandas as pd
#NumPy is a library for the Python programming language, adding support for large, multi-dimensional arrays and matrices, along with a large collection of high-level mathematical functions to operate on these arrays
import numpy as np
# Matplotlib is a plotting library for python and pyplot gives us a MatLab like plotting framework. We will use this in our plotter function to plot data.
import matplotlib.pyplot as plt
#Seaborn is a Python data visualization library based on matplotlib. It provides a high-level interface for drawing attractive and informative statistical graphics
import seaborn as sns

df=pd.read_csv("dataset_part_2.csv")
df.head(5)

sns.catplot(y="PayloadMass", x="FlightNumber", hue="Class", data=df, aspect = 5)
plt.xlabel("Flight Number",fontsize=20)
plt.ylabel("Pay load Mass (kg)",fontsize=20)
plt.show()

# Plot a scatter point chart with x axis to be Flight Number and y axis to be the launch site, and hue to be the class value
sns.catplot(y='LaunchSite',x='FlightNumber', hue='Class',  data=df, aspect=5)
plt.xlabel("Flight Number",fontsize=20)
plt.ylabel("LaunchSite",fontsize=20)
plt.show()

# Plot a scatter point chart with x axis to be Pay Load Mass (kg) and y axis to be the launch site, and hue to be the class value
sns.catplot(y='LaunchSite',x='PayloadMass', hue='Class',  data=df, aspect=5)
plt.xlabel("PayloadMass",fontsize=20)
plt.ylabel("LaunchSite",fontsize=20)
plt.show()

# HINT use groupby method on Orbit column and get the mean of Class column
# Calculate success rate per orbit
success_rate = df.groupby('Orbit')['Class'].mean().reset_index()

# Rename 'class' column to 'success_rate' for clarity
success_rate.rename(columns={'Class': 'success_rate'}, inplace=True)

# Plot bar chart
sns.barplot(x='Orbit', y='success_rate', data=success_rate)

plt.title('Success Rate by Orbit Type')
plt.ylabel('Success Rate')
plt.xlabel('Orbit')
plt.ylim(0,1)  # Since success rate is a proportion between 0 and 1

plt.show()

# Plot a scatter point chart with x axis to be FlightNumber and y axis to be the Orbit, and hue to be the class value
sns.scatterplot(x='FlightNumber', y='Orbit', hue='Class', data=df)

plt.title('FlightNumber vs Orbit colored by class')
plt.xlabel('FlightNumber')
plt.ylabel('Orbit')

plt.show()

# Plot a scatter point chart with x axis to be Payload Mass and y axis to be the Orbit, and hue to be the class value
sns.scatterplot(x='PayloadMass', y='Orbit', hue='Class', data=df)

plt.title('PayloadMass vs Orbit colored by class')
plt.xlabel('PayloadMass')
plt.ylabel('Orbit')

plt.show()

# A function to Extract years from the date 
year=[]
def Extract_year():
    for i in df["Date"]:
        year.append(i.split("-")[0])
    return year
Extract_year()
df['Date'] = year
df.head()

# Plot a line chart with x axis to be the extracted year and y axis to be the success rate
# Calculate success rate per year
success_rate_year = df.groupby('Date')['Class'].mean().reset_index()

# Plot line chart
sns.lineplot(x='Date', y='Class', data=success_rate_year, marker='o')

plt.title('Success Rate by Year')
plt.xlabel('Year')
plt.ylabel('Success Rate')
plt.ylim(0, 1)  # Success rate between 0 and 1

plt.show()

features = df[['FlightNumber', 'PayloadMass', 'Orbit', 'LaunchSite', 'Flights', 'GridFins', 'Reused', 'Legs', 'LandingPad', 'Block', 'ReusedCount', 'Serial']]
features.head()

# HINT: Use get_dummies() function on the categorical columns
# Apply one-hot encoding to the specified columns
features_one_hot = pd.get_dummies(features, columns=['Orbit', 'LaunchSite', 'LandingPad', 'Serial'])

# Display the first few rows of the resulting DataFrame
features_one_hot.head()

features_one_hot = features_one_hot.astype('float64')
features_one_hot.to_csv('dataset_part_3.csv', index=False)
    

