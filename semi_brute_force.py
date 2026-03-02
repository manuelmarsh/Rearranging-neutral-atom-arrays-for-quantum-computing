def semi_brute_force(target_matrix, occ_matrix, extra_atoms=2):
    """
    Semi-brute-force assignment.
    Searches all permutations within a dynamically limited atom pool.
    """

    atoms = get_atom_positions(occ_matrix).tolist()
    targets = get_target_positions(target_matrix).tolist()

    n_targets = len(targets)

    if len(atoms) < n_targets:
        raise ValueError("Not enough atoms.")

    # Compute center of target region
    center_r = sum(t[0] for t in targets) / n_targets
    center_c = sum(t[1] for t in targets) / n_targets

    # Sort atoms by proximity to center
    atoms.sort(key=lambda a: abs(a[0] - center_r) + abs(a[1] - center_c))

    # Dynamic pool size
    pool_size = min(len(atoms), n_targets + extra_atoms)
    atom_pool = atoms[:pool_size]

    best_dist = float('inf')
    best_assignment = None

    for atom_subset in itertools.combinations(atom_pool, n_targets):
        for perm in itertools.permutations(atom_subset):

            current_dist = 0
            for i in range(n_targets):
                current_dist += abs(targets[i][0] - perm[i][0]) + \
                                abs(targets[i][1] - perm[i][1])

            if current_dist < best_dist:
                best_dist = current_dist
                best_assignment = [[perm[i], targets[i]] for i in range(n_targets)]

    best_assignment.sort(
        key=lambda x: abs(x[0][0]-x[1][0]) + abs(x[0][1]-x[1][1])
    )

    return stupid_paths(best_assignment)
