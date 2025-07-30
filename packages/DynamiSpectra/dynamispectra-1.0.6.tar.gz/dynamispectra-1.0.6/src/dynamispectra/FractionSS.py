# analysis.py
import pandas as pd
import matplotlib.pyplot as plt

# State mapping
STATE_MAPPING = {
    'H': 1,  # α-Helix
    'E': 2,  # β-Sheet
    'C': 0,  # Loop/Coil
    'T': 3,  # Turn
    'S': 4,  # Bend
    'G': 5,  # 3-Helix
    '~': -1, # Undefined structure
    'B': -1, # Treat as undefined structure
}

def load_data(file_path):
    """Loads the data file."""
    try:
        df = pd.read_csv(file_path, header=None)
        print("First few rows of the file:")
        print(df.head())
        return df
    except Exception as e:
        print(f"Error loading the file: {e}")
        return None

def calculate_fractions(df):
    """Calculates the fractions of each conformation over time."""
    time = []
    helix_fraction = []
    sheet_fraction = []
    coil_fraction = []
    turn_fraction = []
    bend_fraction = []
    three_helix_fraction = []

    for index, row in df.iterrows():
        sequence = row[0]
        total_residues = len(sequence)

        helix_count = sequence.count("H")
        sheet_count = sequence.count("E")
        coil_count = sequence.count("C")
        turn_count = sequence.count("T")
        bend_count = sequence.count("S")
        three_helix_count = sequence.count("G")

        helix_fraction.append(helix_count / total_residues)
        sheet_fraction.append(sheet_count / total_residues)
        coil_fraction.append(coil_count / total_residues)
        turn_fraction.append(turn_count / total_residues)
        bend_fraction.append(bend_count / total_residues)
        three_helix_fraction.append(three_helix_count / total_residues)

        time.append(index)

    results_df = pd.DataFrame({
        "Time": time,
        "Helix Fraction": helix_fraction,
        "Sheet Fraction": sheet_fraction,
        "Coil Fraction": coil_fraction,
        "Turn Fraction": turn_fraction,
        "Bend Fraction": bend_fraction,
        "3-Helix Fraction": three_helix_fraction
    })

    print("First few rows of the results:")
    print(results_df.head())
    return results_df

def plot_results(results_df, title, output_png, output_tiff):
    """Plots the results and saves the graphs."""
    plt.figure(figsize=(7, 6))

    plt.plot(results_df["Time"], results_df["Helix Fraction"], label="α-Helix", color="#6A9EDA", linewidth=2)
    plt.plot(results_df["Time"], results_df["Sheet Fraction"], label="β-Sheet", color="#f2444d", linewidth=2)
    plt.plot(results_df["Time"], results_df["Coil Fraction"], label="Loop/Coil", color="#4bab44", linewidth=2)
    plt.plot(results_df["Time"], results_df["Turn Fraction"], label="Turn", color="#fc9e19", linewidth=2)
    plt.plot(results_df["Time"], results_df["Bend Fraction"], label="Bend", color="#54b36a", linewidth=2)
    plt.plot(results_df["Time"], results_df["3-Helix Fraction"], label="3-Helix", color="#c9824f", linewidth=2)

    plt.xlabel("Frames")
    plt.ylabel("Fraction of Residues")
    plt.title(title)
    plt.legend(loc="lower center", bbox_to_anchor=(0.5, -0.2), ncol=6, frameon=False, markerscale=2, handlelength=2, handleheight=2)
    plt.grid(False)
    plt.xlim(0, 10000)
    plt.ylim(0, 0.85)

    plt.savefig(output_png, dpi=300, bbox_inches='tight')
    plt.savefig(output_tiff, dpi=300, bbox_inches='tight')
    plt.show()

def fractions_ss_analysis(file_path, output_png, output_tiff, title):
    """Main function for secondary structure analysis."""
    df = load_data(file_path)
    if df is not None:
        results_df = calculate_fractions(df)
        plot_results(results_df, title, output_png, output_tiff)