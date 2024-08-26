import pandas as pd

# Load the original DataFrame from the Excel file
file_path = "/Users/csrbharadwaj/Desktop/Projects/IPL_LOYALITY_METER/data1.xlsx"
df = pd.read_excel(file_path)

# Correct entries
correct_entries = [
    {"Player_Name_Full": "Amit Mishra", "Year": 2016, "TEAM_CODE": "DC"},
    {"Player_Name_Full": "Suresh Raina", "Year": 2014, "TEAM_CODE": "CSK"},
    {"Player_Name_Full": "Amit Mishra", "Year": 2014, "TEAM_CODE": "SRH"},
    {"Player_Name_Full": "Bharath Chipli", "Year": 2013, "TEAM_CODE": "DC"},
    {"Player_Name_Full": "Harmeet Singh", "Year": 2013, "TEAM_CODE": "KXIP"},
    {"Player_Name_Full": "Aakash Chopra", "Year": 2009, "TEAM_CODE": "KKR"},
    {"Player_Name_Full": "Rajat Bhatia", "Year": 2009, "TEAM_CODE": "DC"},
    {"Player_Name_Full": "Shreevats Goswami", "Year": 2008, "TEAM_CODE": "RCB"},
    {"Player_Name_Full": "Albie Morkel", "Year": 2008, "TEAM_CODE": "CSK"},
    {"Player_Name_Full": "Muttiah Muralitharan", "Year": 2008, "TEAM_CODE": "CSK"}
]

# Convert correct entries to a DataFrame
correct_df = pd.DataFrame(correct_entries)

# Save the correct entries to a new Excel file
new_file_path = "/Users/csrbharadwaj/Desktop/Projects/IPL_LOYALITY_METER/updated_correct_data.xlsx"
correct_df.to_excel(new_file_path, index=False)

print(f"Updated data with correct entries saved to {new_file_path}")
