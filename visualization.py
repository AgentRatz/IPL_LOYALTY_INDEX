
import pandas as pd

import plotly.graph_objects as go
import plotly.express as px
import streamlit as st

# Define the custom color palette for IPL teams with primary, secondary, and tertiary colors
color_map = {
    'CSK': {'Primary': '#F9CD05', 'Secondary': '#2A2A72', 'Tertiary': '#EA3C53'},
    'MI': {'Primary': '#004BA0', 'Secondary': '#E4B73F', 'Tertiary': '#B0B8BC'},
    'RCB': {'Primary': '#D11A2D', 'Secondary': '#212121', 'Tertiary': '#CBA92B'},
    'KKR': {'Primary': '#2E0854', 'Secondary': '#D4AF37', 'Tertiary': '#2E0854'},
    'SRH': {'Primary': '#F15A22', 'Secondary': '#000000', 'Tertiary': '#F15A22'},
    'DC': {'Primary': '#17449B', 'Secondary': '#E91326', 'Tertiary': '#17449B'},
    'RR': {'Primary': '#EA1A84', 'Secondary': '#254AA5', 'Tertiary': '#EA1A84'},
    'PBKS': {'Primary': '#D71920', 'Secondary': '#B5B5B5', 'Tertiary': '#D71920'},
    'GT': {'Primary': '#1C1C42', 'Secondary': '#FFB81C', 'Tertiary': '#1C1C42'},
    'LSG': {'Primary': '#00A0E5', 'Secondary': '#FF6000', 'Tertiary': '#00A0E5'},
    'RPS': {'Primary': '#A12559', 'Secondary': '#DA2373', 'Tertiary': '#A12559'},
    'GL': {'Primary': '#F28021', 'Secondary': '#0077B6', 'Tertiary': '#F28021'},
    'DNC': {'Primary': '#1A4380', 'Secondary': '#FFFFFF', 'Tertiary': '#1A4380'},
    'PWI': {'Primary': '#00A19C', 'Secondary': '#004261', 'Tertiary': '#00A19C'},
    'KTK': {'Primary': '#FF9933', 'Secondary': '#472A68', 'Tertiary': '#FF9933'},
    'KXIP': {'Primary': '#D71920', 'Secondary': '#B5B5B5', 'Tertiary': '#D71920'},

}
def plot_loyalty_line_chart(player_df, loyalty_df):
    fig = go.Figure()

    # Extract the team for each year from player_df
    team_per_year = player_df.set_index('Year')['TEAM_CODE']

    # Map the colors based on the team
    loyalty_df['Primary_Color'] = loyalty_df['Year'].map(team_per_year).map(lambda x: color_map.get(x, {}).get('Primary', '#6e6e6e'))
    loyalty_df['Secondary_Color'] = loyalty_df['Year'].map(team_per_year).map(lambda x: color_map.get(x, {}).get('Secondary', '#6e6e6e'))
    loyalty_df['Tertiary_Color'] = loyalty_df['Year'].map(team_per_year).map(lambda x: color_map.get(x, {}).get('Tertiary', color_map.get(x, {}).get('Primary', '#6e6e6e')))

    # Plotting the line chart with team-specific colors
    for team in loyalty_df['Year'].map(team_per_year).unique():
        team_data = loyalty_df[loyalty_df['Year'].map(team_per_year) == team].copy()

        # Sort data by year to ensure lines are drawn in order
        team_data = team_data.sort_values(by='Year')

        # Plotting team-specific data without interpolation (connect only actual points)
        fig.add_trace(go.Scatter(
            x=team_data['Year'],
            y=team_data['Loyalty_Percentage'],
            mode='lines+markers+text',
            name=team,
            line=dict(color=color_map.get(team, {}).get('Primary', '#6e6e6e'), width=4),
            marker=dict(color=color_map.get(team, {}).get('Secondary', '#6e6e6e'), size=8, line=dict(width=2, color=color_map.get(team, {}).get('Tertiary', '#6e6e6e'))),
            text=team_data['Loyalty_Percentage'],
            textposition='top center'
        ))

    fig.update_layout(
        title='Player Loyalty Over Time',
        title_font=dict(size=14, color='white'),
        xaxis_title='Year',
        yaxis_title='Loyalty Percentage',
        xaxis=dict(
            tickvals=loyalty_df['Year'].unique(),
            ticktext=[str(year) for year in loyalty_df['Year'].unique()],
            color='white'
        ),
        yaxis=dict(color='white'),
        paper_bgcolor='black',
        plot_bgcolor='black',
        font=dict(color='white'),
        margin=dict(t=50, b=50, l=50, r=50)
    )

    st.plotly_chart(fig)


def plot_team_tenure_bar_chart(player_df):
    # Count occurrences of each team in the DataFrame
    team_counts = player_df['TEAM_CODE'].value_counts()

    # Create the bar chart
    fig = go.Figure()
    
    for team in team_counts.index:
        fig.add_trace(go.Bar(
            x=[team],
            y=[team_counts[team]],
            name=team,
            marker_color=color_map.get(team, {}).get('Primary', '#6e6e6e'),
            marker_line=dict(
                color=color_map.get(team, {}).get('Secondary', '#6e6e6e'),
                width=2
            ),
            text=[team_counts[team]],
            textposition='auto'
        ))

    fig.update_layout(
        title='Number of Tenures by Team',
        title_font=dict(size=14, color='white'),
        xaxis_title='Team',
        yaxis_title='Number of Tenures',
        xaxis=dict(
            tickvals=list(team_counts.index),
            ticktext=[team for team in team_counts.index],
            color='white'
        ),
        yaxis=dict(color='white'),
        paper_bgcolor='black',
        plot_bgcolor='black',
        font=dict(color='white'),
        margin=dict(t=50, b=50, l=50, r=50)
    )

    st.plotly_chart(fig)
def consolidate_team_periods(team_years):
    """ Consolidate consecutive years for the same team into periods. """
    consolidated = {}
    for team, years in team_years.items():
        years.sort()
        periods = []
        start_year = years[0]
        end_year = years[0]

        for i in range(1, len(years)):
            if years[i] == end_year + 1:
                end_year = years[i]
            else:
                periods.append((start_year, end_year))
                start_year = years[i]
                end_year = years[i]

        periods.append((start_year, end_year))
        consolidated[team] = periods
    return consolidated

def format_labels(consolidated):
    """ Format the labels based on consolidated periods. """
    labels = []
    for team, periods in consolidated.items():
        period_strings = []
        for start_year, end_year in periods:
            if start_year == end_year:
                period_strings.append(f"{start_year}")
            else:
                period_strings.append(f"{start_year}-{end_year}")
        label = f"{team}: {', '.join(period_strings)}"
        labels.append(label)
    return labels

def plot_team_distribution_pie_chart(player_df):
    # Group by team and aggregate the years played
    team_years = player_df.groupby('TEAM_CODE')['Year'].apply(list)
    
    # Consolidate team periods
    consolidated = consolidate_team_periods(team_years)
    
    # Create labels and values
    labels = format_labels(consolidated)
    values = [sum(end - start + 1 for start, end in periods) for periods in consolidated.values()]
    colors = [color_map.get(team, {}).get('Primary', '#6e6e6e') for team in consolidated]
    outlines = [color_map.get(team, {}).get('Secondary', '#6e6e6e') for team in consolidated]

    # Create the pie chart
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hoverinfo='label+percent',
        textinfo='label+value',
        marker=dict(
            colors=colors,
            line=dict(color=outlines, width=2)  # Secondary color as the outline with a width of 2
        ),
        sort=False  # Keep segments in the order of the input data
    )])

    # Uniform text size
    fig.update_traces(textfont_size=12, textposition='inside', insidetextorientation='radial')

    # Update layout to ensure consistent size and appearance
    fig.update_layout(
        title='Player Career Distribution by Team',
        title_font=dict(size=14, color='white'),
        paper_bgcolor='black',
        font=dict(color='white'),
        margin=dict(t=50, b=50, l=50, r=50),
        uniformtext_minsize=10,
        uniformtext_mode='hide'  # Hide text if it doesn't fit well
    )

    st.plotly_chart(fig)