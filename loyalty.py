import pandas as pd
import re
import streamlit as st
import ast
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

def calculate_loyalty(player_df):
    
    # Sort the DataFrame by year
    player_df = player_df.sort_values(by="Year")

    # Initialize variables
    loyalty = 100
    previous_team = None
    previous_year = None
    loyalty_list = []

    # Convert Teams_Playing_That_Year from string to list
    def convert_to_list(teams_str):
        try:
            return ast.literal_eval(teams_str)
        except (ValueError, SyntaxError):
            return []

    player_df["Teams_Playing_That_Year"] = player_df["Teams_Playing_That_Year"].apply(convert_to_list)

    # Calculate loyalty for each year
    for i, row in player_df.iterrows():
        current_team = row["TEAM_CODE"]
        current_year = row["Year"]

        if previous_team is not None:
            if current_team != previous_team:
                if previous_team in row["Teams_Playing_That_Year"]:
                    loyalty -= 10

                if (current_year - previous_year) > 1:
                    loyalty -= 10

        previous_team = current_team
        previous_year = current_year

        loyalty_list.append((current_year, loyalty))

    # Create a DataFrame for easier plotting
    loyalty_df = pd.DataFrame(loyalty_list, columns=['Year', 'Loyalty_Percentage'])
    
    return loyalty_df
