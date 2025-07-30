import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch  # Para criar elementos de legenda personalizados
import os

# Mapeamento dos estados secundários para números
state_mapping = {
    'H': 1,  # Hélice-α
    'E': 2,  # Folha-β
    'C': 0,  # Loop/Coil
    'T': 3,  # Turn
    'S': 4,  # Bend
    'G': 5,  # 3-Helix
    '~': -1, # Sem estrutura definida
    'B': -1, # Tratar como sem estrutura
}

# Nomes das estruturas secundárias
state_names = {
    0: 'Loop/Coil',
    1: 'α-Helix',
    2: 'β-Sheet',
    3: 'Turn',
    4: 'Bend',
    5: '3-Helix',
}

def read_ss(file):
    """
    Reads secondary structure data from a .dat file.

    Parameters:
    -----------
    file : str
        Path to the .dat file.

    Returns:
    --------
    ss_data : numpy.ndarray
        Array of secondary structure data.
    """
    try:
        print(f"Reading file: {file}")
        
        # Open the file and process line by line
        ss_data = []
        
        with open(file, 'r') as f:
            for line in f:
                # Skip comment lines and empty lines
                if line.startswith(('#', '@', ';')) or line.strip() == '':
                    continue
                
                # Try to extract the secondary structure data
                try:
                    ss_line = [state_mapping.get(char, -1) for char in line.strip()]
                    ss_data.append(ss_line)
                except ValueError:
                    # Skip lines that cannot be converted to numbers
                    print(f"Error processing line: {line.strip()}")
                    continue
        
        # Check if the data is valid
        if len(ss_data) == 0:
            raise ValueError(f"File {file} does not contain valid data.")
        
        # Convert lists to numpy arrays
        ss_data = np.array(ss_data)
        
        return ss_data
    
    except Exception as e:
        print(f"Error reading file {file}: {e}")
        return None

def calculate_probabilities(ss_data):
    """
    Calculates the probability of each secondary structure.

    Parameters:
    -----------
    ss_data : numpy.ndarray
        Array of secondary structure data.

    Returns:
    --------
    probabilities : dict
        Dictionary with probabilities for each secondary structure.
    """
    probabilities = {state: [] for state in state_names.values()}
    total_frames = ss_data.shape[0]  # Total de frames

    for estado, nome in state_names.items():
        probabilities[nome] = np.sum(ss_data == estado, axis=1) / ss_data.shape[1]  # Probabilidade por frame

    return probabilities

def plot_ss_boxplot(probabilities_list, labels, colors, output_folder):
    """
    Generates a boxplot for secondary structure probabilities.

    Parameters:
    -----------
    probabilities_list : list of dict
        List of dictionaries with probabilities for each simulation.
    labels : list of str
        Labels for each simulation.
    colors : list of str
        Colors for each simulation.
    output_folder : str
        Output folder to save the plots.
    """
    # Preparar dados para o boxplot
    x_labels = list(state_names.values())  # Estruturas secundárias
    x = np.arange(len(x_labels))  # Posições no eixo X

    # Criar figura para o boxplot
    plt.figure(figsize=(7, 6))
    plt.plot()

    # Função para plotar boxplots
    def plot_boxplot(data, positions, color, label):
        box = plt.boxplot(data, positions=positions, widths=0.4, patch_artist=True, labels=[label] * len(positions), showfliers=False)  # Remover outliers
        for boxplot in box['boxes']:
            boxplot.set_facecolor(color)
            boxplot.set_alpha(0.7)
        for median in box['medians']:
            median.set_color('black')
        return box

    # Plotar boxplots para cada simulação
    for i, (probabilities, label, color) in enumerate(zip(probabilities_list, labels, colors)):
        data = [probabilities[name] * 100 for name in x_labels]
        plot_boxplot(data, x - 0.25 + i * 0.25, color, label)

    # Configuração do gráfico
    plt.xlabel('', fontsize=12)
    plt.ylabel('Probability (%)', fontsize=12)  # Eixo y em percentual
    plt.title('', fontsize=14, fontweight='bold')
    plt.xticks(x, x_labels, rotation=45, fontsize=10)
    plt.yticks(fontsize=10)
    plt.grid(False)  # Remover a grade

    # Cores e rótulos para a legenda
    legend_elements = [
        Patch(facecolor=color, edgecolor='black', linewidth=1.2, alpha=0.7, label=label)
        for label, color in zip(labels, colors)
    ]

    # Posicionar a legenda
    plt.legend(handles=legend_elements, frameon=False, fontsize=10, loc='upper right', edgecolor='black')  # Borda ao redor da legenda

    # Ajustar layout para evitar cortes
    plt.tight_layout()

    # Salvar o gráfico em 300 dpi (PNG e TIFF)
    os.makedirs(output_folder, exist_ok=True)  # Create the folder if it doesn't exist

    # Salvar como PNG
    plt.savefig(os.path.join(output_folder, 'secondary_structure_boxplot.png'), dpi=300, format='png', bbox_inches='tight')

    # Salvar como TIFF
    plt.savefig(os.path.join(output_folder, 'secondary_structure_boxplot.tiff'), dpi=300, format='tiff', bbox_inches='tight')

    # Mostrar gráfico
    plt.show()

def ss_analysis(output_folder, *simulation_files_groups):
    r"""
    Main function to generate secondary structure analysis and plots.

    Parameters:
    -----------
    output_folder : str
        Output folder to save the plots.
    \*simulation_files_groups : list of str
        List of paths to .dat files for each simulation group.
        You can pass 1, 2, or 3 groups.
    """
    # Helper function to process a group of files
    def process_group(file_paths):
        ss_data = []
        for file in file_paths:
            data = read_ss(file)
            ss_data.append(data)
        return ss_data
    
    # Process each group of files
    probabilities_list = []
    labels = []
    colors = ['#333333', '#6A9EDA', '#54b36a']  # Cores para cada simulação

    for i, group in enumerate(simulation_files_groups):
        if group:  # Check if the list is not empty
            ss_data = process_group(group)
            probabilities = calculate_probabilities(ss_data[0])  # Assume only one file per group
            probabilities_list.append(probabilities)
            labels.append(f'Simulation {i + 1}')

    # Generate plots
    plot_ss_boxplot(probabilities_list, labels, colors[:len(probabilities_list)], output_folder)