import pandas as pd
from io import StringIO
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import tkinter as tk
from pandastable import Table
import time

# Set up Selenium Chrome options
options = Options()
options.add_argument('--ignore-certificate-errors')  # Ignore SSL certificate errors
options.add_argument('--incognito')  # Run in incognito mode
options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-usb"])

# Define major European leagues and their corresponding codes for scraping
# The last number represents the competition identifier used in URLs
european_leagues = [
    ("Premier League", "ENG", 9),
    ("La Liga", "SPA", 12),
    ("Serie A", "ITA", 11),
    ("Bundesliga", "GER", 20),
    ("Ligue 1", "FRA", 13),
    ("UEFA Champions League", "UCL", 8),
    ("UEFA Europa League", "UEL", 19),
    ("UEFA Conference League", "UECL", 882),
    ("Big 5 European Leagues", "EUR", "Big5")
]

def comp_stat_display(selected_stat="stats", season=None, comp='EUR', f_a_ind=None):
    # If no season is specified, determine the current season dynamically
    year = time.gmtime()[0]
    current_season = year if time.gmtime()[1] > 8 else (year - 1)
    if season is None:
        season = f"{current_season}-{current_season+1}"
    
    # Ensure statistics are available for the requested season
    if int(season[:4]) < 2017 and selected_stat == "":
        print("Sorry, but this stat wasn't tracked until the 2017-2018 season; only overall, goalkeeping, passing, shooting, and play time stats were tracked!")
        return None
    
    # Find the corresponding league details from the predefined list
    for item in european_leagues:
        if comp == item[1]:
            comps = item
    
    # Initialize the web driver
    driver = webdriver.Chrome(options=options)
    
    # Construct the URL based on selected competition and season
    url_df = f"https://fbref.com/en/comps/{comps[2]}/{season}/{selected_stat}/players/{season}-{(comps[0].replace(' ', '-'))}-Stats"
    
    driver.get(url_df)  # Open the webpage
    
    # Wait until the relevant table is loaded on the page
    WebDriverWait(driver, 100).until(EC.presence_of_all_elements_located((By.ID, f'stats_{selected_stat}' if selected_stat != "stats" else 'stats_standard')))
    
    # Extract table data
    page_source = driver.page_source
    tables = pd.read_html(StringIO(page_source))[-3:]
    driver.quit()  # Close the browser
    
    if f_a_ind.lower() == "individual":
        df = tables[2]  # Select the third table
        df = dataframe_cleaning(df, comp, "player")
        print(df.head())
    else:
        df = pd.read_html(url_df, flavor='bs4')[0]
        df = dataframe_cleaning(df, comp)
        
        if comp != "EUR":
            df2 = pd.read_html(url_df, flavor='bs4')[1]
            df2 = dataframe_cleaning(df2, comp)
            print(df.head())
            print(df2.head())
            
            # Return the appropriate dataframe based on 'for' or 'against' indication
            if f_a_ind.lower() == "for":
                return df
            elif f_a_ind.lower() == "against":
                return df2
    
    df.to_csv(f'{comp}_{selected_stat}_{season}_{f_a_ind}.csv', index=False)
    
    return df

# Function to filter a DataFrame based on conditions
def range_trimming(dataframe, column, condition, comparison=None):
    if isinstance(condition, (int, float)):
        if comparison == ">":
            dataframe = dataframe[dataframe[column] > condition]
        elif comparison == '<':
            dataframe = dataframe[dataframe[column] < condition]
    elif isinstance(condition, str):
        dataframe = dataframe[dataframe[column] == condition]
    print(dataframe.head())
    return dataframe

# Function to clean and process the DataFrame
def dataframe_cleaning(dataframe, comp, type = "squad"):
    dataframe = dataframe_name_replacement(dataframe)  # Replace specific team names
    dataframe.columns = [' '.join(col).strip() for col in dataframe.columns]  # Flatten multi-level columns
    dataframe = dataframe.reset_index(drop=True)
    
    new_columns = []
    for col in dataframe.columns:
        if 'level_0' in col or 'Playing Time' in col:
            new_col = col.split()[-1]  # Extract meaningful column names
        elif "Performance" in col:
            new_col = "Raw " + col.split()[-1]
        elif "Per 90 Minutes" in col:
            new_col = col.split()[-1] + "/90 Min"
        else:
            new_col = col.split()[1:]
            if isinstance(new_col, list):
                new_col = ' '.join(new_col)
        new_columns.append(new_col)
    dataframe.columns = new_columns  # Rename columns
    
    print(dataframe.dtypes)
    for col in dataframe.columns:
        print(dataframe[col].head())
        # dataframe[col] = pd.to_numeric(dataframe[col], errors='ignore')

    df = df.fillna(0)
    
    if type.lower() == "squad":
        if comp == "EUR":
            dataframe['Position'] = dataframe['Pos'].str[:2]  # Extract position data
            dataframe['Position 2'] = dataframe['Pos'].str[3:]
            dataframe['Nation'] = dataframe['Nation'].str.split(' ').str.get(1)  # Extract country code
            dataframe['League'] = dataframe['Comp'].str.split(' ').str.get(1) + ' ' + dataframe['Comp'].str.split(' ').str.get(2)
            dataframe = dataframe.drop(columns=['League_', 'Comp', 'Rk', 'Pos', 'Matches'])
            dataframe['Position'] = dataframe['Position'].replace({'MF': 'Midfielder', 'DF': 'Defender', 'FW': 'Forward', 'GK': 'Goalkeeper'})
        else:
            dataframe = dataframe.drop(columns=['Pl'])
    return dataframe

# Function to replace incorrect team names with correct ones
def dataframe_name_replacement(dataframe):
    replacements = [["Nott'ham Forest", "Nottingham Forest"], ["Eint Frankfurt", "Eintracht Frankfurt"]]
    for item in replacements:
        dataframe = dataframe.replace(f"{item[0]}", f"{item[1]}")
        dataframe = dataframe.replace(f"vs {item[0]}", f"vs {item[1]}")
    return dataframe

# Uncomment below lines to display data using a GUI
df = comp_stat_display(comp='ENG', selected_stat ="gca", season = "2023-2024", f_a_ind="individual")
