import streamlit as st
from shared import calculate_loyalty
from visualization import plot_loyalty_line_chart, plot_team_tenure_bar_chart, plot_team_distribution_pie_chart
from advanced_viz import plot_team_distribution_map
import geopandas as gpd

shapefile_path = gpd.read_file('india_states.shp')

def display_player_profile(player_df, loyalty_df):
    if not player_df.empty:
        # Extract the profile link and images of the selected player
        player_profile_link = player_df['Profile_Link'].iloc[0]

        # Generate the HTML with the dynamic profile link and images
        dynamic_html = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Player Profile</title>
            <style>
                body {{
                    margin: 0;
                    padding: 0;
                    background-color: black;
                }}
                .container {{
                    width: 100%;
                    height: 30vh; /* Fixed height for the iframe container */
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    overflow: hidden;
                }}
                .iframe-wrapper {{
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    overflow: hidden;
                    margin-left: -250px;
                    margin-bottom: -200px;
                    width: 2010px; /* Fixed width for the iframe wrapper */
                    height: 580px; /* Fixed height for the iframe wrapper */
                }}
                iframe {{
                    border: none;
                    width: 100%;  /* Ensure iframe width matches wrapper */
                    height: 100%;  /* Ensure iframe height matches wrapper */
                    transform: scale(1);  /* Prevent scaling */
                    transform-origin: 0 0; /* Ensure scaling is fixed to the top-left corner */
                    pointer-events: none;  /* Disable interactions */
                }}
                .grid-container {{
                    display: grid;
                    grid-template-columns: repeat(6, 1fr);
                    grid-gap: 10px;
                    margin-top: 20px;
                }}
                .grid-item {{
                    background-color: #000000;
                    border: 1px solid #000000;
                    padding: 10px;
                    text-align: center;
                    color: white;
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                }}
                .player-details {{
                    font-size: 14px;
                    margin-bottom: 10px;
                }}
                .player-face {{
                    width: 100px;
                    height: auto;
                }}
                .player-jersey {{
                    width: 100px;
                    height: auto;
                    margin-top: -25px;
                }}
                /* Disable right-click context menu */
                body, iframe {{
                    -webkit-touch-callout: none; /* Disable callout, for iOS */
                    -webkit-user-select: none;   /* Disable text selection, for Safari */
                    -khtml-user-select: none;    /* Disable text selection, for Konqueror */
                    -moz-user-select: none;      /* Disable text selection, for Firefox */
                    -ms-user-select: none;       /* Disable text selection, for Internet Explorer/Edge */
                    user-select: none;           /* Non-prefixed version, currently supported by Chrome, Edge, Opera and Firefox */
                    -webkit-user-drag: none;     /* Disable dragging */
                    -webkit-user-modify: none;   /* Disable text field editing */
                    pointer-events: none;        /* Disable mouse interactions */
                    -webkit-tap-highlight-color: transparent; /* Remove tap highlight */
                }}
                body {{
                    pointer-events: auto; /* Allow pointer events on body */
                }}
            </style>
            <script>
                document.addEventListener('contextmenu', event => event.preventDefault());  /* Disable right-click */
            </script>
        </head>
        <body>
            <div class="container" id="container">
                <div class="iframe-wrapper">
                    <iframe id="myIframe" scrolling="no" src="{player_profile_link}"></iframe>
                </div>
            </div>
            <div class="grid-container">
                {generate_grid_items(player_df)}
            </div>
        </body>
        </html>
        """
        # Display the HTML and iframe in Streamlit
        st.write(dynamic_html, unsafe_allow_html=True)

        # Merge the player_df with loyalty_df based on the year
        player_df_with_loyalty = player_df.merge(loyalty_df, on='Year', how='left')

        # Display the table below the iframe
        st.subheader("Player Details:")
        st.table(player_df_with_loyalty[["Player_Name_short", "TEAM_CODE", "Year", "Loyalty_Percentage"]].reset_index(drop=True))

        # Display loyalty percentage
        st.subheader(f"Loyalty Percentage: {loyalty_df['Loyalty_Percentage'].iloc[-1]}%")

        # Add visualizations below the loyalty percentage
        st.header("Player Loyalty Visualization")
        
        # Plot the loyalty line chart
        plot_loyalty_line_chart(player_df, loyalty_df)

        # Plot the team tenure bar chart
        plot_team_tenure_bar_chart(player_df)

        plot_team_distribution_pie_chart(player_df)

        # Plot team distribution map
        plot_team_distribution_map(player_df)
    else:
        st.write("No matching players found.")

def generate_grid_items(player_df):
    grid_items = ""
    for _, row in player_df.iterrows():
        grid_items += f"""
        <div class="grid-item">
            <div class="player-details">
                {row['Year']} : {row['TEAM_CODE']}
            </div>
            <img src="{row['Player_Face']}" alt="Player Face" class="player-face">
            <img src="{row['Player_Jersey']}" alt="Player Jersey" class="player-jersey">
        </div>
        """
    return grid_items
