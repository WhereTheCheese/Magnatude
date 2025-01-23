import pandas as pd
from astropy.cosmology import FlatLambdaCDM
import numpy as np

def analyze_sdss_data(csv_file):
    """Analyzes SDSS data from a CSV file to calculate absolute magnitudes and distances."""

    try:
        df = pd.read_csv(csv_file)
    except FileNotFoundError:
        print(f"Error: CSV file '{csv_file}' not found.")
        return
    except pd.errors.EmptyDataError:
        print(f"Error: CSV file '{csv_file}' is empty.")
        return
    except pd.errors.ParserError:
        print(f"Error: Could not parse CSV file '{csv_file}'. Check the format.")
        return

    if df.empty:
        print("No data to process.")
        return
    
    required_columns = ['objID', 'ra', 'dec', 'u', 'dered_u', 'z']
    if not all(col in df.columns for col in required_columns):
        print(f"Error: CSV file must contain the following columns: {required_columns}")
        return

    cosmo = FlatLambdaCDM(H0=70, Om0=0.3)

    df['Distance (Mpc)'] = cosmo.luminosity_distance(df['z']).value
    df['Absolute u'] = df['u'] - 5 * np.log10(df['Distance (Mpc)'] * 1e6) + 5

    print(df[['objID', 'ra', 'dec', 'u', 'dered_u', 'z', 'Distance (Mpc)', 'Absolute u']].to_string())

# Example usage:
if __name__ == "__main__":
    print("What is the name of the CSV file?")
    csv_filename = input() 
    analyze_sdss_data(csv_filename)
