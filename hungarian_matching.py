def hungarian_matching(target_matrix, occ_matrix, alpha=2.0):
    """Rigorous assignment using the Hungarian algorithm and alpha scaling."""
    D = get_dist_matrix(target_matrix, occ_matrix, metric="manhattan")
    atoms = get_atom_positions(occ_matrix)
    targets = get_target_positions(target_matrix)

    # Apply alpha scaling to penalize trespassing and force relaying
    cost_matrix = D ** alpha
    row_ind, col_ind = linear_sum_assignment(cost_matrix)

    assignments = []
    for r, c in zip(row_ind, col_ind):
        assignments.append({'source': atoms[c].tolist(), 'target': targets[r].tolist(), 'dist': D[r][c]})

    # Sort by shortest distance first to help clear local traffic
    assignments.sort(key=lambda x: x['dist'])
    ordered_assignments = [[a['source'], a['target']] for a in assignments]

    return stupid_paths(ordered_assignments)
