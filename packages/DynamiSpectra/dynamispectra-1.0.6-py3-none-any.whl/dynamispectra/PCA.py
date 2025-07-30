import numpy as np
import matplotlib.pyplot as plt
import os

def read_xvg(file_path):
    """
    Reads data from a .xvg file.

    Parameters:
    -----------
    file_path : str
        Path to the .xvg file.

    Returns:
    --------
    data : numpy.ndarray
        Array of numerical data from the .xvg file.
    """
    data = []
    with open(file_path, "r") as file:
        for line in file:
            if not line.startswith(("#", "@")):  # Ignore headers and metadata
                values = line.split()
                data.append([float(values[0]), float(values[1])])  # PC1 and PC2
    return np.array(data)

def read_eigenvalues(eigenval_path):
    """
    Reads eigenvalues from a .xvg file.

    Parameters:
    -----------
    eigenval_path : str
        Path to the .xvg file containing eigenvalues.

    Returns:
    --------
    eigenvalues : numpy.ndarray
        Array of eigenvalues.
    """
    eigenvalues = []
    with open(eigenval_path, "r") as file:
        for line in file:
            if not line.startswith(("#", "@")):
                # Extract the second column (eigenvalues)
                value = line.split()[1]
                eigenvalues.append(float(value))
    return np.array(eigenvalues)

def plot_pca(pca_data, eigenvalues, output_folder, title="PCA"):
    """
    Generates the PCA plot.

    Parameters:
    -----------
    pca_data : numpy.ndarray
        Array of PCA data (PC1 and PC2).
    eigenvalues : numpy.ndarray
        Array of eigenvalues.
    output_folder : str
        Output folder to save the plot.
    title : str, optional
        Title of the plot.
    """
    # Calculate the explained variance in percentage
    total_variance = np.sum(eigenvalues)
    pc1_variance = (eigenvalues[0] / total_variance) * 100
    pc2_variance = (eigenvalues[1] / total_variance) * 100

    # Create the scatter plot (PC1 vs PC2)
    plt.figure(figsize=(7, 6))
    scatter = plt.scatter(
        pca_data[:, 0], pca_data[:, 1], 
        c=np.linspace(0, 1, len(pca_data)),  # Gradient of colors for points
        cmap="viridis",  # Colormap to differentiate points
        alpha=0.8, edgecolors='k', linewidths=0.8
    )

    # Update axis labels with explained variance
    plt.xlabel(f"PC1 ({pc1_variance:.2f}%)")
    plt.ylabel(f"PC2 ({pc2_variance:.2f}%)")
    plt.title(title)

    # Add color bar
    plt.colorbar(scatter, label="Simulation times")
    plt.grid(False)

    # Save the plot as PNG with 300 DPI
    os.makedirs(output_folder, exist_ok=True)  # Create the folder if it doesn't exist
    output_path = os.path.join(output_folder, 'pca_plot.png')
    plt.savefig(output_path, dpi=300)

    # Show the plot
    plt.show()

def pca_analysis(pca_file_path, eigenval_path, output_folder, title="PCA"):
    """
    Main function to generate PCA analysis and plot.

    Parameters:
    -----------
    pca_file_path : str
        Path to the .xvg file containing PCA data.
    eigenval_path : str
        Path to the .xvg file containing eigenvalues.
    output_folder : str
        Output folder to save the plot.
    title : str, optional
        Title of the plot.
    """
    # Read PCA data
    pca_data = read_xvg(pca_file_path)

    # Read eigenvalues
    eigenvalues = read_eigenvalues(eigenval_path)

    # Generate the PCA plot
    plot_pca(pca_data, eigenvalues, output_folder, title)