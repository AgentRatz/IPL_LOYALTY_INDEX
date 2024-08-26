import pandas as pd
import re
import streamlit as st
from display import display_player_profile

def filter_and_display_players(file_path):
    # Column names for the data
    column_names = ["Profile_Link", "Player_Name_short", "Player_Name_Full", "Player_Type", "Player_Face", "Player_Jersey", "TEAM_CODE", "Year", "Teams_Playing_That_Year"]

    # Load the Excel file into a DataFrame
    df = pd.read_excel(file_path, sheet_name="Sheet1", names=column_names, header=0)

    # Create a search box
    search_query = st.sidebar.text_input("Search for a player:")

    # Filter the DataFrame based on the search query
    filtered_df = df[df['Player_Name_Full'].str.contains(search_query, case=False)]

    # Function to remove suffixes from player short names
    def remove_suffix(name):
        return re.sub(r'\s?\(.*\)', '', name)

    # Apply the function to remove suffixes from player short names
    filtered_df['Player_Name_short'] = filtered_df['Player_Name_short'].apply(remove_suffix)

    # Group by profile link and filter only those profiles which match the given search query
    grouped_df = filtered_df.groupby('Profile_Link').filter(lambda x: len(x) > 1)

    # Get unique players based on profile link
    unique_players = grouped_df.groupby('Profile_Link').first()

    # Display a selection dropdown for choosing the player
    selected_player = st.sidebar.selectbox("Select a player:", options=unique_players['Player_Name_Full'].tolist())

    # Filter the DataFrame based on the selected player
    selected_player_df = grouped_df[grouped_df['Player_Name_Full'] == selected_player]

    # Calculate loyalty
    loyalty_df = calculate_loyalty(selected_player_df)

    # Display the filtered DataFrame and loyalty percentage
    if not selected_player_df.empty:
        display_player_profile(selected_player_df, loyalty_df)
    else:
        st.write("No matching players found.")

import pandas as pd

import pandas as pd

def calculate_loyalty(player_df):
    # Sort the DataFrame by Year in ascending order
    player_df = player_df.sort_values(by="Year")

    # Initialize variables
    previous_team = None
    previous_year = None
    loyalty_dict = {}
    last_known_loyalty = 100

    # Iterate over each row in the DataFrame
    for i, row in player_df.iterrows():
        current_team = row["TEAM_CODE"]
        current_year = row["Year"]

        if previous_team is not None:
            # Check if the previous team is listed in the "Teams_Playing_That_Year"
            teams_playing_that_year = row.get("Teams_Playing_That_Year", [])
            
            if current_team != previous_team:
                if previous_team in teams_playing_that_year or len(teams_playing_that_year) == 0:
                    # Decrease loyalty for team change, but not if the team was not playing
                    last_known_loyalty = max(last_known_loyalty - 10, 0)
            else:
                # Increase loyalty if staying with the same team
                last_known_loyalty = min(last_known_loyalty + 5, 100)
        
        # Store the loyalty percentage for the current year
        loyalty_dict[current_year] = last_known_loyalty

        # Update previous_team and previous_year
        previous_team = current_team
        previous_year = current_year

    # Ensure all years from the minimum to maximum year are represented
    all_years = list(range(player_df["Year"].min(), player_df["Year"].max() + 1))
    full_loyalty_list = [(year, loyalty_dict.get(year, last_known_loyalty)) for year in all_years]

    # Create a DataFrame for easier plotting
    loyalty_df = pd.DataFrame(full_loyalty_list, columns=['Year', 'Loyalty_Percentage'])
    loyalty_df['Team'] = player_df['TEAM_CODE'].iloc[0]  # Add team column

    return loyalty_df

