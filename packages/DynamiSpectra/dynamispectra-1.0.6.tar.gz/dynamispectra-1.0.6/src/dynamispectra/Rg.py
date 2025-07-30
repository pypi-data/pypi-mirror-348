import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde
import os

def read_rg(file):
    """
    Reads Rg data from a .xvg file.

    Parameters:
    -----------
    file : str
        Path to the .xvg file.

    Returns:
    --------
    times : numpy.ndarray
        Array of simulation times.
    rg_values : numpy.ndarray
        Array of Rg values.
    """
    try:
        print(f"Reading file: {file}")
        
        # Open the file and process line by line
        times = []
        rg_values = []
        
        with open(file, 'r') as f:
            for line in f:
                # Skip comment lines and empty lines
                if line.startswith(('#', '@', ';')) or line.strip() == '':
                    continue
                
                # Try to extract the first two numeric values from the line
                try:
                    line_values = line.split()
                    time = float(line_values[0])  # Time
                    rg_total = float(line_values[1])  # Rg value
                    times.append(time / 1000)  # Convert time to nanoseconds
                    rg_values.append(rg_total)
                except ValueError:
                    # Skip lines that cannot be converted to numbers
                    print(f"Error processing line: {line.strip()}")
                    continue
        
        # Check if the data is valid
        if len(times) == 0 or len(rg_values) == 0:
            raise ValueError(f"File {file} does not contain valid data.")
        
        # Convert lists to numpy arrays
        times = np.array(times)
        rg_values = np.array(rg_values)
        
        return times, rg_values
    
    except Exception as e:
        print(f"Error reading file {file}: {e}")
        return None, None

def check_simulation_times(*time_arrays):
    r"""
    Checks if simulation times are consistent across files.

    Parameters:
    -----------
    \*time_arrays : list of numpy.ndarray
        Arrays of times to compare.
    """
    for i in range(1, len(time_arrays)):
        if not np.allclose(time_arrays[0], time_arrays[i]):
            raise ValueError(f"Simulation times do not match between file 1 and file {i+1}")

def plot_rg(time_simulation1, mean_simulation1, std_simulation1,
            time_simulation2, mean_simulation2, std_simulation2,
            time_simulation3, mean_simulation3, std_simulation3,
            output_folder):
    """
    Generates the Rg plot with mean and standard deviation for the groups provided.
    """
    # Create figure for the Rg plot
    plt.figure(figsize=(7, 6))
    plt.plot()

    # Plot for simulation1 (if provided)
    if time_simulation1 is not None:
        plt.plot(time_simulation1, mean_simulation1, label='Simulation 1', color='#333333', linewidth=2)
        plt.fill_between(time_simulation1, mean_simulation1 - std_simulation1, mean_simulation1 + std_simulation1, color='#333333', alpha=0.2)

    # Plot for simulation2 (if provided)
    if time_simulation2 is not None:
        plt.plot(time_simulation2, mean_simulation2, label='Simulation 2', color='#6A9EDA', linewidth=2)
        plt.fill_between(time_simulation2, mean_simulation2 - std_simulation2, mean_simulation2 + std_simulation2, color='#6A9EDA', alpha=0.2)

    # Plot for simulation3 (if provided)
    if time_simulation3 is not None:
        plt.plot(time_simulation3, mean_simulation3, label='Simulation 3', color='#54b36a', linewidth=2)
        plt.fill_between(time_simulation3, mean_simulation3 - std_simulation3, mean_simulation3 + std_simulation3, color='#54b36a', alpha=0.2)

    # Configure the Rg plot
    plt.xlabel('Time (ns)', fontsize=12)
    plt.ylabel('Rg (nm)', fontsize=12)
    plt.title('', fontsize=14)
    plt.legend(frameon=False, loc='upper right', fontsize=10)
    plt.tick_params(axis='both', which='major', labelsize=10)
    plt.grid(False)

    # Adjust x-axis limits to start at 0
    plt.xlim(left=0)  # Set the minimum x-axis limit to 0
    plt.xlim(right=100)
    
    # Adjust layout
    plt.tight_layout()

    # Save the Rg plot in TIFF and PNG formats
    os.makedirs(output_folder, exist_ok=True)  # Create the folder if it doesn't exist

    # Save as TIFF
    plt.savefig(os.path.join(output_folder, 'rg_plot.tiff'), format='tiff', dpi=300)
    # Save as PNG
    plt.savefig(os.path.join(output_folder, 'rg_plot.png'), format='png', dpi=300)

    # Show the Rg plot
    plt.show()

def plot_density(mean_simulation1, mean_simulation2, mean_simulation3, output_folder):
    """
    Generates the density plot for the groups provided.
    """
    # Create figure for the density plot
    plt.figure(figsize=(6, 6))
    plt.plot()

    # Add KDE (Kernel Density Estimation) for each dataset (if provided)
    if mean_simulation1 is not None:
        kde_simulation1 = gaussian_kde(mean_simulation1)
        x_vals = np.linspace(0, max(mean_simulation1), 1000)
        plt.fill_between(x_vals, kde_simulation1(x_vals), color='#333333', alpha=0.5, label='Simulation 1')

    if mean_simulation2 is not None:
        kde_simulation2 = gaussian_kde(mean_simulation2)
        x_vals = np.linspace(0, max(mean_simulation2), 1000)
        plt.fill_between(x_vals, kde_simulation2(x_vals), color='#6A9EDA', alpha=0.6, label='Simulation 2')

    if mean_simulation3 is not None:
        kde_simulation3 = gaussian_kde(mean_simulation3)
        x_vals = np.linspace(0, max(mean_simulation3), 1000)
        plt.fill_between(x_vals, kde_simulation3(x_vals), color='#54b36a', alpha=0.5, label='Simulation 3')

    # Configure the density plot
    plt.xlabel('Rg (nm)', fontsize=12)
    plt.ylabel('Density', fontsize=12)
    plt.title('', fontsize=14)
    plt.legend(frameon=False, loc='upper left', fontsize=10)
    plt.tick_params(axis='both', which='major', labelsize=10)
    plt.grid(False)
    plt.tight_layout()

    # Save the density plot in TIFF and PNG formats
    # Save as TIFF
    plt.savefig(os.path.join(output_folder, 'density_plot.tiff'), format='tiff', dpi=300)
    # Save as PNG
    plt.savefig(os.path.join(output_folder, 'density_plot.png'), format='png', dpi=300)

    # Show the density plot
    plt.show()

def rg_analysis(output_folder, *simulation_files_groups):
    r"""
    Main function to generate Rg analysis and plots.

    Parameters:
    -----------
    output_folder : str
        Output folder to save the plots.
    \*simulation_files_groups : list of str
        List of paths to .xvg files for each simulation group.
        You can pass 1, 2, or 3 groups.
    """
    # Helper function to process a group of files
    def process_group(file_paths):
        times = []
        rg_values = []
        for file in file_paths:
            time, rg = read_rg(file)
            times.append(time)
            rg_values.append(rg)
        check_simulation_times(*times)  # Check if times are consistent
        mean_rg = np.mean(rg_values, axis=0)  # Calculate mean
        std_rg = np.std(rg_values, axis=0)  # Calculate standard deviation
        return times[0], mean_rg, std_rg
    
    # Process each group of files
    results = []
    for group in simulation_files_groups:
        if group:  # Check if the list is not empty
            time, mean, std = process_group(group)
            results.append((time, mean, std))

    # Generate plots based on the number of groups
    if len(results) == 1:
        # Plot for 1 group
        plot_rg(results[0][0], results[0][1], results[0][2], None, None, None, None, None, None, output_folder)
        plot_density(results[0][1], None, None, output_folder)
    elif len(results) == 2:
        # Plot for 2 groups
        plot_rg(results[0][0], results[0][1], results[0][2],
                results[1][0], results[1][1], results[1][2],
                None, None, None, output_folder)
        plot_density(results[0][1], results[1][1], None, output_folder)
    elif len(results) == 3:
        # Plot for 3 groups
        plot_rg(results[0][0], results[0][1], results[0][2],
                results[1][0], results[1][1], results[1][2],
                results[2][0], results[2][1], results[2][2], output_folder)
        plot_density(results[0][1], results[1][1], results[2][1], output_folder)
    else:
        raise ValueError("You must provide at least one group of simulation files.")