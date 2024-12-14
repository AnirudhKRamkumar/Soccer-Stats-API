from stat_scraper import comp_stat_display, range_trimming
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

df = comp_stat_display(comp='ENG', selected_stat ="shooting", f_a_ind="against")
df = range_trimming(df, "Gls", 5, ">")

# Set up the plot
plt.figure(figsize=(10, 6))

# Scatter plot
sns.scatterplot(x='Gls', y='xG', data=df, s=100)

for _, row in df.iterrows():
    plt.text(row['Gls'], row['xG'], row['Squad'], fontsize=9, ha='center')

ticks = np.arange(min(df['Gls']) - 1, max(df['Gls']) + 1, 2)  # Adjust the step size
plt.xticks(ticks)

x_vals = np.linspace(min(df['Gls']) - 1, max(df['Gls']) + 1, 100)
plt.plot(x_vals, x_vals, color='red', linestyle='--', label='y = x')

# Add titles and labels
plt.title('Goals vs xG', fontsize=16)
plt.xlabel('Goals', fontsize=12)
plt.ylabel('xG', fontsize=12)

# Display the plot
plt.show()