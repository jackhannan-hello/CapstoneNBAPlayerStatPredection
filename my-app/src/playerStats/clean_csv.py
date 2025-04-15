import pandas as pd

file_path = r"c:\Users\Jack Hannan\source\repos\CapstoneNBAPlayerStatPredection\my-app\src\playerStats\jaysontatumFullStats.csv"
output_path = r"c:\Users\Jack Hannan\source\repos\CapstoneNBAPlayerStatPredection\my-app\src\playerStats\jaysontatumFullStats_cleaned.csv"

# Load the CSV while ignoring problematic rows
try:
    df = pd.read_csv(file_path, on_bad_lines="skip")
    print("CSV loaded successfully!")
    
    # Save the cleaned CSV
    df.to_csv(output_path, index=False)
    print(f"Cleaned CSV saved to {output_path}")
except Exception as e:
    print(f"Error loading CSV: {e}")