import numpy as np
import matplotlib.pyplot as plt
import os

def read_xpm(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()

    lines = [l.strip() for l in lines if l.strip().startswith('"')]
    header_line = lines[0].strip().strip('",')
    width, height, ncolors, chars_per_pixel = map(int, header_line.split())

    color_map = {}
    for i in range(1, ncolors + 1):
        line = lines[i].strip().strip('",')
        symbol = line[:chars_per_pixel]
        color_map[symbol] = i - 1

    matrix = []
    for line in lines[ncolors + 1:]:
        line = line.strip().strip('",')
        row = [color_map[line[i:i+chars_per_pixel]] for i in range(0, len(line), chars_per_pixel)]
        matrix.append(row)

    return np.array(matrix)

def plot_density(matrix, cmap='inferno', xlabel='X', ylabel='Y', title='', 
                 colorbar_label='Relative density', save_path=None):
    """
    Plots the density matrix and optionally saves it as .png and .tiff in 300 dpi.
    """
    plt.figure()
    plt.imshow(matrix, cmap=cmap, origin='lower', aspect='auto')
    plt.colorbar(label=colorbar_label)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.tight_layout()

    if save_path:
        base, _ = os.path.splitext(save_path)
        plt.savefig(f"{base}.png", dpi=300)
        plt.savefig(f"{base}.tiff", dpi=300)
        print(f"Gráficos salvos como {base}.png e {base}.tiff")

    plt.show()

def ligand_density_analysis(xpm_file_path, plot=True, save_path=None):
    """
    Reads an XPM file, plots the ligand density, and optionally saves the figure.
    """
    matrix = read_xpm(xpm_file_path)
    if plot:
        plot_density(matrix, save_path=save_path)
    return matrix
