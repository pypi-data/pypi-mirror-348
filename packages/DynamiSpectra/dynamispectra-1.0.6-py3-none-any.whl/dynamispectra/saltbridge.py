import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde
import os

def read_saltbridge(file):
    """
    Reads salt-bridge distance data from a .xvg file.

    Parameters:
    -----------
    file : str
        Path to the .xvg file.

    Returns:
    --------
    times : numpy.ndarray
        Time values from simulation.
    distances : numpy.ndarray
        Salt-bridge distances.
    """
    try:
        print(f"Reading file: {file}")
        times, distances = [], []

        with open(file, 'r') as f:
            for line in f:
                if line.startswith(('#', '@', ';')) or line.strip() == '':
                    continue
                try:
                    values = line.split()
                    if len(values) >= 2:
                        time, distance = map(float, values[:2])
                        times.append(time / 1000.0)  # Convert ps to ns
                        distances.append(distance)
                except ValueError:
                    print(f"Error processing line: {line.strip()}")
                    continue

        if len(times) == 0 or len(distances) == 0:
            raise ValueError(f"File {file} does not contain valid data.")

        return np.array(times), np.array(distances)

    except Exception as e:
        print(f"Error reading file {file}: {e}")
        return None, None

def check_simulation_times(*time_arrays):
    for i in range(1, len(time_arrays)):
        if not np.allclose(time_arrays[0], time_arrays[i]):
            raise ValueError(f"Simulation times do not match between file 1 and file {i+1}")

def plot_saltbridge(time1, mean1, std1,
                    time2, mean2, std2,
                    time3, mean3, std3,
                    output_folder):
    """
    Generates the salt-bridge distance plot with mean and standard deviation.
    """
    plt.figure(figsize=(7, 6))

    if time1 is not None:
        plt.plot(time1, mean1, label='Simulation 1', color='#333333', linewidth=2)
        plt.fill_between(time1, mean1 - std1, mean1 + std1, color='#333333', alpha=0.2)

    if time2 is not None:
        plt.plot(time2, mean2, label='Simulation 2', color='#6A9EDA', linewidth=2)
        plt.fill_between(time2, mean2 - std2, mean2 + std2, color='#6A9EDA', alpha=0.2)

    if time3 is not None:
        plt.plot(time3, mean3, label='Simulation 3', color='#54b36a', linewidth=2)
        plt.fill_between(time3, mean3 - std3, mean3 + std3, color='#54b36a', alpha=0.2)

    plt.xlabel('Time (ns)', fontsize=12)
    plt.ylabel('Salt-Bridge Distance (nm)', fontsize=12)
    plt.legend(frameon=False, loc='upper right', fontsize=10)
    plt.tick_params(axis='both', which='major', labelsize=10)
    plt.grid(False)

    # Ajuste do limite do eixo x para o último tempo dos dados
    max_time = max(
        max(time1) if time1 is not None else 0,
        max(time2) if time2 is not None else 0,
        max(time3) if time3 is not None else 0,
    )
    plt.xlim(0, max_time)

    plt.tight_layout()

    os.makedirs(output_folder, exist_ok=True)
    plt.savefig(os.path.join(output_folder, 'saltbridge_plot.tiff'), format='tiff', dpi=300)
    plt.savefig(os.path.join(output_folder, 'saltbridge_plot.png'), format='png', dpi=300)
    plt.show()

def plot_density(mean1, mean2, mean3, output_folder):
    """
    Generates the density plot for salt-bridge mean values.
    """
    plt.figure(figsize=(6, 6))

    if mean1 is not None:
        kde1 = gaussian_kde(mean1)
        x_vals = np.linspace(0, max(mean1), 1000)
        plt.fill_between(x_vals, kde1(x_vals), color='#333333', alpha=0.5, label='Simulation 1')

    if mean2 is not None:
        kde2 = gaussian_kde(mean2)
        x_vals = np.linspace(0, max(mean2), 1000)
        plt.fill_between(x_vals, kde2(x_vals), color='#6A9EDA', alpha=0.5, label='Simulation 2')

    if mean3 is not None:
        kde3 = gaussian_kde(mean3)
        x_vals = np.linspace(0, max(mean3), 1000)
        plt.fill_between(x_vals, kde3(x_vals), color='#54b36a', alpha=0.5, label='Simulation 3')

    plt.xlabel('Salt-Bridge Distance (nm)', fontsize=12)
    plt.ylabel('Density', fontsize=12)
    plt.legend(frameon=False, loc='upper right', fontsize=10)
    plt.tick_params(axis='both', which='major', labelsize=10)
    plt.grid(False)
    plt.tight_layout()

    plt.savefig(os.path.join(output_folder, 'saltbridge_density.tiff'), format='tiff', dpi=300)
    plt.savefig(os.path.join(output_folder, 'saltbridge_density.png'), format='png', dpi=300)
    plt.show()

def saltbridge_analysis(output_folder, *simulation_files_groups):
    """
    Main function to generate salt-bridge analysis and plots.

    Parameters:
    -----------
    output_folder : str
        Output folder to save plots.
    *simulation_files_groups : list of str
        List of .xvg files for each simulation group.
    """
    def process_group(file_paths):
        times, distances = [], []
        for file in file_paths:
            time, dist = read_saltbridge(file)
            times.append(time)
            distances.append(dist)
        check_simulation_times(*times)
        mean_dist = np.mean(distances, axis=0)
        std_dist = np.std(distances, axis=0)
        return times[0], mean_dist, std_dist

    results = []
    for group in simulation_files_groups:
        if group:
            time, mean, std = process_group(group)
            results.append((time, mean, std))

    if len(results) == 1:
        plot_saltbridge(results[0][0], results[0][1], results[0][2],
                        None, None, None, None, None, None, output_folder)
        plot_density(results[0][1], None, None, output_folder)
    elif len(results) == 2:
        plot_saltbridge(results[0][0], results[0][1], results[0][2],
                        results[1][0], results[1][1], results[1][2],
                        None, None, None, output_folder)
        plot_density(results[0][1], results[1][1], None, output_folder)
    elif len(results) == 3:
        plot_saltbridge(results[0][0], results[0][1], results[0][2],
                        results[1][0], results[1][1], results[1][2],
                        results[2][0], results[2][1], results[2][2], output_folder)
        plot_density(results[0][1], results[1][1], results[2][1], output_folder)
    else:
        raise ValueError("You must provide at least one group of simulation files.")
