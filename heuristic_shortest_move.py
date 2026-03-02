def heuristic_shortest_move(target_matrix, occ_matrix):
    """
    Implements greedy shortest-move matching.

    Output:
        [[[i,j], [i',j'], ...], ...]  (paths)
    """

    D = get_dist_matrix(target_matrix, occ_matrix, metric="manhattan")

    atoms = get_atom_positions(occ_matrix)
    targets = get_target_positions(target_matrix)

    n_targets = D.shape[0]

    # Keep track of available rows and columns
    available_rows = list(range(n_targets))
    available_cols = list(range(D.shape[1]))

    assignments = []

    # Repeat until all targets assigned
    for _ in range(n_targets):

        min_value = float("inf")
        min_row = None
        min_col = None

        # Find smallest available element
        for r in available_rows:
            for c in available_cols:

                if D[r][c] < min_value:
                    min_value = D[r][c]
                    min_row = r
                    min_col = c

        # Assign atom to target
        source = atoms[min_col].tolist()
        target = targets[min_row].tolist()

        assignments.append([source, target])

        # Remove row and column
        available_rows.remove(min_row)
        available_cols.remove(min_col)

    # Convert simple assignments into full paths
    paths = stupid_paths(assignments)

    return paths
