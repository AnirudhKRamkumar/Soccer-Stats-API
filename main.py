import pandas as pd

# Prompt user to input the desired statistic type
selected_stat = input("What stat? ")


## def stat_display(selected_stat):
# Construct the URL based on the selected statistic
url_df = f'https://fbref.com/en/comps/Big5/{selected_stat}/players/Big-5-European-Leagues-Stats'

# Read the HTML table from the URL into a list of DataFrames and select the first DataFrame
df = pd.read_html(url_df)[0]

# Flatten multi-level column headers by joining them with a space and stripping any extra whitespace
df.columns = [' '.join(col).strip() for col in df.columns]
# Reset index to ensure it's a standard range index
df = df.reset_index(drop=True)

# Rename columns to simplify the names by removing 'level_0' and keeping the last part
new_columns = []
for col in df.columns:
    if 'level_0' in col or 'Playing Time' in col or 'Progression' in col:
      new_col = col.split()[-1]  # takes the last name
    elif "Performance" in col:
      new_col = "Raw " + col.split()[-1]
    elif "Per 90 Minutes" in col:
      new_col = col.split()[-1] + "/90 Min"
    else:
      new_col = col
    new_columns.append(new_col)
# Apply new column names to the DataFrame
df.columns = new_columns

# Fill any NaN values with 0
df = df.fillna(0)

# Split the 'Pos' column into 'Position' and 'Position_2' based on character positions
df['Position'] = df['Pos'].str[:2]
df['Position_2'] = df['Pos'].str[3:]

# Extract country code from 'Nation' column
df['Nation'] = df['Nation'].str.split(' ').str.get(1)

# Extract league names from 'Comp' column
df['League'] = df['Comp'].str.split(' ').str.get(1)
df['League_'] = df['Comp'].str.split(' ').str.get(2)
df['League'] = df['League'] + ' ' + df['League_']

# Drop unnecessary columns
df = df.drop(columns=['League_', 'Comp', 'Rk', 'Pos', 'Matches'])
df = df[df['Player'] != 'Player']
df = df.drop([0])

# Replace position abbreviations with full position names
df['Position'] = df['Position'].replace({'MF': 'Midfielder', 'DF': 'Defender', 'FW': 'Forward', 'GK': 'Goalkeeper'})
df['Position_2'] = df['Position_2'].replace({'MF': 'Midfielder', 'DF': 'Defender', 'FW': 'Forward', 'GK': 'Goalkeeper'})

# Fill any remaining NaN values in 'League' column with 'Bundesliga'
df['League'] = df['League'].fillna('Bundesliga')

# Print the first few rows of the processed DataFrame
print(df.head())

def range_shortening(column, condition):
  for row in df.iterrows():
    row = row[1]
    if column in range(len(row)):
      if isinstance(condition, int): 
        value = row[column]
        try:
            if int(value) > condition:
                print(row.to_string(), "\n")
        except ValueError:
            # Skip rows where conversion to integer fails
            continue
      elif isinstance(condition, str):
        value = row[column]
        try:
          if value == condition:
            print(row.to_string(), "\n")
        except ValueError:
          continue

# Export to HTML
df.to_html('dataframe.html')

# Open HTML file in default web browser (optional)
import webbrowser
webbrowser.open('dataframe.html')


# range_shortening(9, 21)
# range_shortening(1, "AUT")