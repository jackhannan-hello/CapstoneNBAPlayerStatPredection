import pandas as pd

# Load the CSV file
file_path = r"c:\Users\Jack Hannan\source\repos\CapstoneNBAPlayerStatPredection\my-app\src\playerStats\nikolajokicFullStats.csv"
df = pd.read_csv(file_path)

# Mapping of team abbreviations to zip codes
team_zip_mapping = {
    "BOS": "02114", "CLE": "44115", "MIL": "53203", "PHI": "19148", "NYK": "10001",
    "MIA": "33132", "SAS": "78219", "SAC": "95814", "OKC": "73102", "ORL": "32801",
    "ATL": "30313", "BRK": "11217", "GSW": "94607", "LAL": "90015", "LAC": "90015",
    "UTA": "84101", "DEN": "80204", "DET": "48226", "IND": "46225", "CHO": "28202",
    "TOR": "51300", "WAS": "20004", "HOU": "77002", "MEM": "38103", "NOP": "70112",
    "POR": "97227", "PHO": "85004", "DAL": "75219", "MIN": "55403", "CHI": "60612"
}

#"TOR": "M5V1J3"

# Replace team abbreviations with zip codes
df["Team"] = df["Team"].map(team_zip_mapping)
df["AWAY"] = df["AWAY"].replace({None: "0", "@": "1"})
df["Opp"] = df["Opp"].map(team_zip_mapping)

#df = df.drop(df.columns[0], axis=1) # Drop the first column (index column)
# Replace `,,` with `0` and `@` with `1` in the Opp column


# Save the updated CSV file
output_path = r"c:\Users\Jack Hannan\source\repos\CapstoneNBAPlayerStatPredection\my-app\src\playerStats\nikolajokicFullStats.csv"
df.to_csv(output_path, index=False)

print(f"Updated CSV saved to {output_path}")