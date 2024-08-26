import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import streamlit as st

# IPL team color mapping
color_map = {
    'CSK': '#F9CD05',
    'MI': '#004BA0',
    'RCB': '#D11A2D',
    'KKR': '#2E0854',
    'SRH': '#F15A22',
    'DC': '#17449B',
    'RR': '#EA1A84',
    'PBKS': '#D71920',
    'GT': '#1C1C42',
    'LSG': '#00A0E5',
    'RPS': '#A12559',
    'KXIP': '#E43843',
    'PWI': '#6C1D5F',
    'GL': '#F57F17',
    'DNC': '#0033A0',
    'KTK': '#FF9933',
    'Other': '#6e6e6e'
}

# Define team to state mapping (Update as needed)
team_to_state = {
    'CSK': 'Tamil Nadu',
    'MI': 'Maharashtra',
    'RCB': 'Karnataka',
    'KKR': 'West Bengal',
    'SRH': 'Telangana',
    'DC': 'NCT of Delhi',
    'RR': 'Rajasthan',
    'PBKS': 'Punjab',
    'GT': 'Gujarat',
    'LSG': 'Uttar Pradesh',
    'RPS': 'Maharashtra',  # Historical team
    'KXIP': 'Punjab',     # Historical team
    'PWI': 'Maharashtra', # Historical team
    'GL': 'Gujarat',      # Historical team
    'DNC': 'Telangana',   # Historical team
    'KTK': 'Kerala'
}

def interpolate_color(color1, color2, t):
    """Interpolate between two colors."""
    c1 = np.array([int(color1[i:i+2], 16) for i in (1, 3, 5)])
    c2 = np.array([int(color2[i:i+2], 16) for i in (1, 3, 5)])
    c = (1 - t) * c1 + t * c2
    return '#%02x%02x%02x' % (int(c[0]), int(c[1]), int(c[2]))

def plot_team_distribution_map(player_df):
    # Load the shapefile
    shapefile_path = 'india_states.shp'
    india_map = gpd.read_file(shapefile_path)
    
    # Map teams to states
    player_df['State'] = player_df['TEAM_CODE'].map(team_to_state)
    
    # Create a state-to-team mapping with colors
    state_color_map = {}
    state_team_map = {}
    for state in india_map['ST_NM']:
        teams_in_state = player_df[player_df['State'] == state]['TEAM_CODE'].unique()
        if len(teams_in_state) > 1:
            # Interpolate colors if more than one team is present
            color1 = color_map.get(teams_in_state[0], '#6e6e6e')
            color2 = color_map.get(teams_in_state[1], '#6e6e6e')
            state_color_map[state] = interpolate_color(color1, color2, 0.5)  # Use a midpoint for simplicity
            state_team_map[state] = (teams_in_state[0], teams_in_state[1])
        elif len(teams_in_state) == 1:
            # Use the single team's color
            state_color_map[state] = color_map.get(teams_in_state[0], '#6e6e6e')
            state_team_map[state] = (teams_in_state[0],)
        else:
            # Handle cases with no teams
            state_color_map[state] = '#6e6e6e'  # Default color for states with no teams
            state_team_map[state] = ()

    # Map state names to colors
    india_map['Color'] = india_map['ST_NM'].map(state_color_map).fillna('gray')  # Default to gray for unmapped states

    # Plot the map
    fig, ax = plt.subplots(figsize=(12, 12))
    india_map.plot(ax=ax, color=india_map['Color'], edgecolor='black')

    # Prepare the legend handles and labels
    unique_colors = list(set(india_map['Color']))
    legend_handles = []
    legend_labels = []

    for color in unique_colors:
        teams = [team for state, color_val in state_color_map.items() if color_val == color for team in state_team_map[state]]
        unique_teams = list(set(teams))
        if len(unique_teams) > 1:
            # For gradient colors, use both teams in the legend
            legend_labels.append(f"{unique_teams[0]} & {unique_teams[1]}")
        else:
            # For single colors, use the team in the legend
            legend_labels.append(unique_teams[0] if unique_teams else "Others")


        legend_handles.append(plt.Line2D([0], [0], color=color, lw=4))
    
    # Add the legend
    plt.legend(legend_handles, legend_labels, title='IPL Teams', bbox_to_anchor=(1.05, 1), loc='upper left', title_fontsize='13', fontsize='10')

    # Customize the plot
    plt.title('IPL Teams Distribution by State', fontsize=14, color='white')
    plt.axis('off')  # Hide the axes
    st.pyplot(fig)  # Use Streamlit's pyplot function to display the plot
