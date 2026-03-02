# Convert Assignment Data to Paths Data

def stupid_paths(assignments):
    """
    Input:
        assignments = [
            [[si, sj], [ti, tj]],
            ...
        ]

    Output:
        paths = [
          [[si, sj], ..., [ti, tj]],   # full path for atom 1
          ...
        ]
    """

    all_paths = []

    for pair in assignments:

        start = pair[0]
        target = pair[1]

        si, sj = start
        ti, tj = target

        path = [[si, sj]]

        # --- Move horizontally first ---
        current_i, current_j = si, sj

        while current_j != tj:
            if tj > current_j:
                current_j += 1
            else:
                current_j -= 1
        path.append([current_i, current_j])

        # --- Then move vertically ---
        while current_i != ti:
            if ti > current_i:
                current_i += 1
            else:
                current_i -= 1
        path.append([current_i, current_j])

        all_paths.append(path)

    return all_paths
