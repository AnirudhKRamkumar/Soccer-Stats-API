from stat_scraper import comp_stat_display, range_trimming
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

df = comp_stat_display(comp='ENG', selected_stat ="gca", season = "2023-2024", f_a_ind="individual")
df = range_trimming(df, 'SCA', 100, ">")

df2 = comp_stat_display(comp='ENG', selected_stat ="stats", season = "2023-2024", f_a_ind="individual")
df2 = range_trimming(df2, 'xG+xAG/90 Min', 0.4, ">")
print(df2.columns)
df2['xG+xAG/90 Min'] = df2['xG+xAG/90 Min'] * df2['90s']

# Set up the plot
plt.figure(figsize=(10, 6))

# Scatter plot
sns.scatterplot(x=df['SCA'], y=df2['xG+xAG/90 Min'], s=100)

for i, row in df.iterrows():
    if row['Player'] in df2['Player'].values:
        plt.text(row['SCA'], df2.loc[i, 'xG+xAG/90 Min'], row['Player'], fontsize=9, ha='center')
    else:
        pass

# Add titles and labels
plt.title('Shot-Creating Actions vs xG + xAG', fontsize=16)
plt.xlabel('Shot-Creating Actions', fontsize=12)
plt.ylabel('xG + xAG', fontsize=12)

# Display the plot
plt.show()