# USEFUL FUNCTIONS (not algorithms)

import numpy as np
import matplotlib.pyplot as plt

# Only use SQUARE (NXN) Occ-Matrices are considered

def create_rectangular_target_matrix(size=7, m=3, n=3, top_left_position=(2, 2)):
    """
    Input:
        size: the size of the lattice.
        m: the number of rows in the target region.
        n: the number of columns in the target region.
        top_left_position: tuple (i,j), the top left corner of the target region.
    Output:
        np.array: a size x size binary lattice with ones in the target positions.
    """
    target_matrix = np.zeros((size, size), dtype=int)
    i_start = top_left_position[0]
    j_start = top_left_position[1]

    for i in range(i_start, i_start + m):
        for j in range(j_start, j_start + n):
            target_matrix[i][j] = 1

    return target_matrix

def create_occ_matrix(n_atoms=21, size=7, seed=None):
    """
    Create a size x size binary lattice with exactly n_atoms ones in random positions.
    Input:
        n_atoms: the number of atoms to place in the lattice.
        size: the size of the lattice.
    Output:
        np.array: a size x size binary lattice with n_atoms ones in random positions.
    """
    if seed is not None:
        np.random.seed(seed)

    if n_atoms > size * size:
        raise ValueError("Number of atoms cannot exceed total lattice sites.")

    # Create flat array with exact number of ones
    flat = np.zeros(size * size, dtype=int)
    flat[:n_atoms] = 1
    np.random.shuffle(flat)

    # Reshape into 2D lattice
    occ_matrix = flat.reshape((size, size))

    return occ_matrix

def get_atom_positions(occ_matrix):
    """
    Returns array of shape (n_atoms, 2)
    Each row = (x, y) coordinate of an atom.
    """
    return np.argwhere(occ_matrix == 1)

def get_target_positions(target_matrix):
    """
    Returns target coordinates (9 positions).
    """
    return np.argwhere(target_matrix == 1)

def get_dist_matrix(target_matrix, occ_matrix, metric="manhattan"):
    """
    Returns a (n_targets x n_atoms) distance matrix.

    metric:
        "euclidean"  -> sqrt((dx)^2 + (dy)^2)
        "manhattan"  -> |dx| + |dy|
    """

    atoms = get_atom_positions(occ_matrix)      # list of atom coordinates
    targets = get_target_positions(target_matrix)  # list of target coordinates

    n_targets = len(targets)
    n_atoms = len(atoms)

    D = np.zeros((n_targets, n_atoms))

    for i in range(n_targets):
        for j in range(n_atoms):

            dx = targets[i][0] - atoms[j][0]
            dy = targets[i][1] - atoms[j][1]

            if metric == "euclidean":
                distance = np.sqrt(dx**2 + dy**2)

            elif metric == "manhattan":
                distance = abs(dx) + abs(dy)

            else:
                raise ValueError("metric must be 'euclidean' or 'manhattan'")

            D[i][j] = distance

def plot_grid(occ_matrix):
    """
    Visualize the 7x7 grid.
    Red dots  -> atoms
    Green dots -> empty traps
    Blue square -> central 3x3 target region
    """

    grid_size = occ_matrix.shape[0]

    # --------------------------------------------------
    # 1. Get atom positions
    # --------------------------------------------------
    atoms = get_atom_positions(occ_matrix)

    # --------------------------------------------------
    # 2. Generate all possible grid positions
    # --------------------------------------------------
    all_positions = [(x, y) for x in range(grid_size)
                              for y in range(grid_size)]

    # --------------------------------------------------
    # 3. Empty positions = positions that are NOT atoms
    # --------------------------------------------------
    empties = [pos for pos in all_positions if pos not in atoms]

    # --------------------------------------------------
    # 4. Separate x and y coordinates for plotting
    # --------------------------------------------------
    atom_x = [pos[0] for pos in atoms]
    atom_y = [pos[1] for pos in atoms]

    empty_x = [pos[0] for pos in empties]
    empty_y = [pos[1] for pos in empties]

    # --------------------------------------------------
    # 5. Create figure
    # --------------------------------------------------
    fig, ax = plt.subplots(figsize=(7, 7))

    # Plot atoms (red)
    ax.scatter(atom_x, atom_y,
              color='red',
              s=150,
              label='Loaded Atom')

    # --------------------------------------------------
    # 6. Draw grid lines
    # --------------------------------------------------
    ax.set_xticks(np.arange(-0.5, grid_size, 1))
    ax.set_yticks(np.arange(-0.5, grid_size, 1))
    ax.grid(True)

    # Remove numbers on axes
    ax.set_xticklabels([])
    ax.set_yticklabels([])

    # --------------------------------------------------
    # 7. Draw central 3x3 target square
    # In a 7x7 grid, center is from 2 to 4
    # --------------------------------------------------
    rect = plt.Rectangle((1.5, 1.5), 3, 3,
                        linewidth=3,
                        edgecolor='blue',
                        facecolor='none',
                        linestyle=':',
                        label='Target 3x3')

    ax.add_patch(rect)

    # --------------------------------------------------
    # 8. Adjust plot limits
    # --------------------------------------------------
    ax.set_xlim(-0.5, grid_size - 0.5)
    ax.set_ylim(-0.5, grid_size - 0.5)

    # Title and legend
    plt.title(f"7x7 Grid with {len(atoms)} Atoms")
    plt.legend()

    # Show plot
    plt.show()


    return D


