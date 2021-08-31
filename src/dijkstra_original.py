import networkx as nx


def get_neighbors(G, v):
    neighbors = list()
    for n in G.neighbors(v):
        weight = 1
        try:
            weight = G[v][n]['weight']
        except Exception as ex:
            print(ex, 'Hier')
        finally:
            neighbors.append((n, weight))
    return neighbors


def dijkstra_original(G, source, target, excluded_vertices=None):
    try:
        if source in excluded_vertices:
            raise nx.NetworkXNoPath(f"Source {source} can not be excluded!")
        if target in excluded_vertices:
            raise nx.NetworkXNoPath(f"Target {target} can not be excluded!")
    except Exception as e:
        raise e

    # Raise exception if source or target are excluded
    if source in excluded_vertices or target in excluded_vertices:
        raise nx.NetworkXNoPath

    # Init distances with infinite
    distances = {v: float('inf') for v in G.nodes}

    # Swap source and target so the distances are calculated from the target and not the source
    # This is important for the path building step
    swap = [source, target]
    source = swap[1]

    distances[source] = 0
    vertices = list(G.nodes)

    # Calculate the distance of each node to the target
    while len(vertices) > 0:
        v = min(vertices, key=lambda u: distances[u])
        vertices.remove(v)
        if distances[v] == float('inf'):
            break
        for neighbor, weight in get_neighbors(G, v):
            path_cost = distances[v] + weight
            if path_cost < distances[neighbor]:
                distances[neighbor] = path_cost

    #Swap source and target back
    source = swap[0]

    path = list()
    path.append(source)
    current_vertex = source
    while current_vertex != target:
        # Get the neighbors of the current vertex
        neighbors = get_neighbors(G, current_vertex)
        # Sort them based on their costs to the current vertex
        neighbors.sort(reverse=True, key=lambda tup: tup[1])
        costs_to_src = [float('inf')]
        for neighbor in neighbors:
            if neighbor[0] != source \
                    and neighbor[0] not in excluded_vertices \
                    and distances[neighbor[0]] != float('inf') \
                    and (distances[neighbor[0]] + neighbor[1]) < (min(costs_to_src)):
                # Pick the neighbor with (current) minimal cost to target
                # The next vertex is determined by its total distance to the target + edge cost from the current vertex
                # The vertex with the minimal sum is chosen
                current_vertex = neighbor[0]
                costs_to_src.append(distances[neighbor[0]] + neighbor[1])
        path.append(current_vertex)
        # If the same vertex is twice in the path then its a loop and the algorithm can terminate
        if len(path) != len(set(path)):
            break

    return path

