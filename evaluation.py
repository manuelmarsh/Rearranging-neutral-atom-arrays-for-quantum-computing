import time
def evaluation(target_matrix, occ_matrix):
    """
    This does 5 things: calculate

    1) time taken,
    2) total distance,
    3) number of collisions
    4) paths
    5) all_collisions
    """

    # Computational time
    start = time.perf_counter()
    paths = algo(target_matrix, occ_matrix)

    end = time.perf_counter()

    delta_time = end - start


    # Distances for each path
    distances = []
    for path in paths:
        total_distance = 0
        current_position = path[0] # [i,j]
        for position in path[1:]:
            delta_i = abs(current_position[0] - position[0])
            delta_j = abs(current_position[1] - position[1])
            total_distance += delta_i + delta_j
            current_position = position
        distances.append(total_distance)

    total_distance = sum(distances)


    # Collision detection
    current_occ = occ_matrix.copy()

    all_collisions = []

    for path in paths:
        current_position = path[0]
        path_collisions = []

        for other_position in path[1:]: # other positions where there is a direction change

            i_now = current_position[0]
            j_now = current_position[1]

            i_next = other_position[0]
            j_next = other_position[1]

            if i_now == i_next: # horizontal move
                if j_now > j_next: # left move
                    for j in range(j_now, j_next, -1):
                        if current_occ[i_now, j] == 1:
                            path_collisions.append([i_now, j])
                else: # right move
                    for j in range(j_now, j_next, +1):
                        if current_occ[i_now, j] == 1:
                            path_collisions.append([i_now, j])

            if j_now == j_next: # vertical move
                if i_now > i_next: # up move
                    for i in range(i_now, i_next, -1):
                        if current_occ[i, j_now] == 1:
                            path_collisions.append([i, j_now])
                else: # down move
                    for i in range(i_now, i_next, +1):
                        if current_occ[i, j_now] == 1:
                            path_collisions.append([i, j_now])

            # Update occupancy matrix
            current_occ[i_now, j_now] = 0
            current_occ[i_next, j_next] = 1

            # Update current position
            current_position = other_position

        all_collisions.append(path_collisions)


        # Count total number of collisions
        n_collisions = 0
        for path_collisions in all_collisions:
            n_collisions += len(path_collisions)

    return delta_time, total_distance, n_collisions, paths, all_collisions
