
import streamlit as st
from utils import filter_and_display_players

# Set page configuration to wide layout
st.set_page_config(layout="wide")

# File paths
background_image_url = "https://wallpapercave.com/wp/wp8994043.jpg"
file_path = "data1.xlsx"

# Apply background image and transparency styles for Home page
page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] {{
    background-image: url("{background_image_url}");
    background-size: cover;
    background-position: center;
}}

[data-testid="stHeader"] {{
    background-color: rgba(0, 0, 0, 0);
}}

[data-testid="stSidebar"] {{
    display: none;
}}

[data-testid="stSidebarContent"] {{
    display: none;
}}

.footer {{
    position: fixed;
    bottom: 0;
    left: 0;
    width: 100%;
    text-align: center;
    background-color: rgba(0, 0, 0, 0.2);
    color: rgba(255, 255, 255, 0.7);
    padding: 10px 0;
    font-size: 12px;
}}
</style>
"""

# Set default page if not selected
if 'page' not in st.session_state:
    st.session_state.page = "Home"

# Page content
st.title("Welcome to the IPL Loyalty Meter")
st.write("Explore the Journey of Your Player Across Teams")

# Page selection buttons side by side
col1, col2 = st.columns([1, 12])
with col1:
    if st.button("Home"):
        st.session_state.page = "Home"
with col2:
    if st.button("Player Search"):
        st.session_state.page = "Player Search"

# Apply background image for Home page
if st.session_state.page == "Home":
    st.markdown(page_bg_img, unsafe_allow_html=True)
elif st.session_state.page == "Player Search":
    # Apply solid black background for Player Search page
    page_bg_black = """
    <style>
    [data-testid="stAppViewContainer"] {{
        background-color: black;
    }}
    </style>
    """
    st.markdown(page_bg_black, unsafe_allow_html=True)
    filter_and_display_players(file_path)

# Footer
st.markdown("""
<div class="footer">
    Developed by Rahul Bharadwaj, IPL LOYALTY METER Version 1.0
</div>
""", unsafe_allow_html=True)
