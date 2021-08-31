import networkx as nx
import matplotlib.pyplot as plt
import dijkstra_original as do
import re
import random


def nodeConnectivity(G, layout):
    graphs = list()
    figures = list()
    graphData, bridges, articulationPoints = list(), list(), list()
    sortedNodes = sorted(dict(G.nodes), key=lambda g: g[0])

    graphData.append('')
    graphData.append(nx.is_connected(G))
    if nx.has_bridges(G):
        graphData.append(nx.has_bridges(G))
        bridges.extend(nx.bridges(G))
        graphData.append(bridges)
        articulationPoints.extend(nx.articulation_points(G))
        graphData.append(articulationPoints)
    else:
        graphData.append(nx.has_bridges(G))
    graphs.append(graphData)

    nodeColor = list()
    for n in sortedNodes:
        if n in list(articulationPoints):
            nodeColor.append("green")
        else:
            nodeColor.append("#1f78b4")

    edgeColor = list()
    for e in dict(G.edges):
        if e in list(bridges):
            edgeColor.append("#ff8000")
        else:
            edgeColor.append("black")

    figures.append(createFigure(G, layout=layout, sortedNodes=sortedNodes, articulationPoints=articulationPoints,
                                bridges=bridges, nodeColor=nodeColor, edgeColor=edgeColor))

    for node in sortedNodes:
        graphData, bridges, articulationPoints = list(), list(), list()
        newG = G.copy()
        newG.remove_node(node)
        graphData.append(node)
        graphData.append(nx.is_connected(newG))
        if nx.has_bridges(newG):
            graphData.append(nx.has_bridges(newG))
            bridges.extend(nx.bridges(newG))
            graphData.append(bridges)
            articulationPoints.extend(nx.articulation_points(newG))
            graphData.append(articulationPoints)
        else:
            graphData.append(nx.has_bridges(newG))
        graphs.append(graphData)

        nodeColor = list()
        for n in sortedNodes:
            if n is node:
                nodeColor.append("red")
            elif n in list(articulationPoints):
                nodeColor.append("green")
            else:
                nodeColor.append("#1f78b4")

        edgeColor = list()
        for e in dict(G.edges):
            if e in list(bridges):
                edgeColor.append("#ff8000")
            else:
                edgeColor.append("black")

        figures.append(createFigure(G, layout=layout, sortedNodes=sortedNodes, removedNode=node, articulationPoints=articulationPoints,
                                    bridges=bridges, nodeColor=nodeColor, edgeColor=edgeColor))

    return graphs, figures


def edgeConnectivity(G, layout):
    graphs = list()
    figures = list()
    graphData, bridges, articulationPoints = list(), list(), list()
    sortedEdges = sorted(dict(G.edges), key=lambda g: g[0])

    graphData.append('')
    graphData.append(nx.is_connected(G))
    if nx.has_bridges(G):
        graphData.append(nx.has_bridges(G))
        bridges.extend(nx.bridges(G))
        graphData.append(bridges)
        articulationPoints.extend(nx.articulation_points(G))
        graphData.append(articulationPoints)
    else:
        graphData.append(nx.has_bridges(G))
    graphs.append(graphData)

    sortedNodes = sorted(dict(G.nodes), key=lambda g: g[0])
    nodeColor = list()
    for n in sortedNodes:
        if n in list(articulationPoints):
            nodeColor.append("green")
        else:
            nodeColor.append("#1f78b4")

    edgeColor = list()
    for e in dict(G.edges):
        if e in list(bridges):
            edgeColor.append("#ff8000")
        else:
            edgeColor.append("black")

    figures.append(createFigure(G, layout=layout, sortedNodes=sortedNodes, articulationPoints=articulationPoints,
                                bridges=bridges, nodeColor=nodeColor, edgeColor=edgeColor))

    for edge in sortedEdges:
        graphData, bridges, articulationPoints = list(), list(), list()
        newG = G.copy()
        newG.remove_edge(edge[0], edge[1])
        graphData.append(edge)
        graphData.append(nx.is_connected(newG))
        if nx.has_bridges(newG):
            graphData.append(nx.has_bridges(newG))
            bridges.extend(nx.bridges(newG))
            graphData.append(bridges)
            articulationPoints.extend(nx.articulation_points(newG))
            graphData.append(articulationPoints)
        else:
            graphData.append(nx.has_bridges(newG))
        graphs.append(graphData)

        sortedNodes = sorted(dict(G.nodes), key=lambda g: g[0])
        nodeColor = list()
        for n in sortedNodes:
            if n in list(articulationPoints):
                nodeColor.append("green")
            else:
                nodeColor.append("#1f78b4")

        edgeColor = list()
        for e in dict(G.edges):
            if e == edge:
                edgeColor.append("red")
            elif e in list(bridges):
                edgeColor.append("#ff8000")
            else:
                edgeColor.append("black")

        figures.append(createFigure(G, layout=layout, sortedNodes=sortedNodes, removedEdge=edge, articulationPoints=articulationPoints,
                                    bridges=bridges, nodeColor=nodeColor, edgeColor=edgeColor))

    return graphs, figures


def edgeAugementation(G, k, layout):
    graphs, figures, kAugmentedEdges = list(), list(), list()
    for i in range(1, k+1):
        try:
            newEdges = sorted(nx.k_edge_augmentation(G, k=i))
            kAugmentedEdges.append(newEdges)
            newG = G.copy()
            newG.add_edges_from(newEdges)
            graphs.append(newG)
            edgeColor = list()
            for e in dict(newG.edges):
                if e in list(newEdges):
                    edgeColor.append("green")
                else:
                    edgeColor.append("black")
            figures.append(createFigure(newG, layout=layout, edgeColor=edgeColor, kAugmentedEdges=newEdges))
        except Exception as e:
            print(e)

    return graphs, figures, kAugmentedEdges


def kNodeAlgorithm(G, layout):
    # For k=3
    newG = G.copy()
    articulationPoints = list()
    newEndpoints = set()
    graphs, figures, nodes = list(), list(), list()
    figures.append(createFigure(G, layout=layout,))
    graphs.append(G)
    nodes.append([])
    if nx.has_bridges(newG):
        articulationPoints.extend(nx.articulation_points(G))
        for point in nx.articulation_points(G):
            edges = newG.edges(point)
            for edge in edges:
                newEndpoints.add(edge[0] + "'")
                if edge[1] not in newEndpoints:
                    newG.add_edge(edge[0] + "'", edge[1])

            # for point in articulationPoints:
            #     newG.add_edge(point, point + 10)

    sortedNodes = sorted(dict(newG.nodes), key=lambda g: g[0])
    nodeColor = list()
    for n in sortedNodes:
        if n in newEndpoints:
            nodeColor.append("lightblue")
        elif n in articulationPoints:
            nodeColor.append("green")
        else:
            nodeColor.append("#1f78b4")

    graphs.append(newG.copy())
    nodes.append(list(newEndpoints))
    figures.append(createFigure(newG, layout=layout, sortedNodes=sortedNodes,
                                articulationPoints=articulationPoints,
                                nodeColor=nodeColor, kAugmentedNodes=newEndpoints))

    """K=3"""
    criticalNodes = list()
    for node1 in dict(newG.nodes):
        loopG = newG.copy()
        loopG.remove_node(node1)
        for node2 in dict(loopG.nodes):
            loopG2 = loopG.copy()
            loopG2.remove_node(node2)
            if not nx.is_connected(loopG2):
                criticalNodes.append((node1, node2))
            newG.add_node(node2)
        newG.add_node(node1)

    loopG3 = newG.copy()
    usedNodes = set()
    for critNode in criticalNodes:
        edges1 = loopG3.edges(critNode[0])
        edges2 = loopG3.edges(critNode[1])
        edgeSet = set()
        for edge in edges1:
            edgeSet.add(edge)
        for edge in edges2:
            edgeSet.add(edge)
        for edge in edgeSet:
            if critNode[1] + critNode[0] not in usedNodes:
                newG.add_edge(critNode[0] + critNode[1], edge[1])
                usedNodes.add(critNode[0] + critNode[1])
    createFigure(newG, layout=layout)

    sortedNodes = sorted(dict(newG.nodes), key=lambda g: g[0])
    nodeColor = list()
    for n in sortedNodes:
        if n in usedNodes:
            nodeColor.append("lightblue")
        else:
            nodeColor.append("#1f78b4")

    edgeColor = list()
    usedEdges = list()
    for e in newG.edges:
        if e[1] in usedNodes:
            edgeColor.append("green")
            usedEdges.append(e)
        else:
            edgeColor.append("black")


    graphs.append(newG)
    nodes.append(list(usedNodes))
    figures.append(createFigure(newG, layout=layout, sortedNodes=sortedNodes,
                                nodeColor=nodeColor, edgeColor=edgeColor, kAugmentedNodes=usedNodes,
                                kAugmentedEdges=usedEdges))
    print(graphs, figures)
    return graphs, figures, nodes


def addNode(G, nodeID):
    G.add_node(nodeID)


def removeNode(G, nodeID):
    G.remove_node(nodeID)


def addEdge(G, node1, node2, weight=None):
    if weight is None:
        G.add_edge(node1, node2)
    else:
        G.add_edge(node1, node2, weight=weight)


def removeEdge(G, nodeID1, nodeID2):
    G.remove_edge(nodeID1, nodeID2)


def createLayout(G, layout=None):
    pos = nx.spring_layout(G, seed=36)
    if layout == 'Planar' and nx.check_planarity(G)[0]:
        print(nx.check_planarity(G))
        pos = nx.planar_layout(G)
    elif layout == 'Circular':
        pos = nx.circular_layout(G)
    elif layout == 'Kamada-Kawai':
        pos = nx.kamada_kawai_layout(G)
    elif layout == 'Random':
        pos = nx.random_layout(G)
    elif layout == 'Spectral':
        pos = nx.spectral_layout(G)
    elif layout == 'Spiral':
        pos = nx.spiral_layout(G, resolution=1.0)

    return pos


def createFigure(G, layout='Spring', text=None, sortedNodes=None, nodeColor=None, edgeColor=None, removedNode=None, removedEdge=None,
                 articulationPoints=None, bridges=None, kAugmentedEdges=None, kAugmentedNodes=None):

    pos = createLayout(G, layout)

    # Closes all figures before creating new ones (without this old figures remain in the ram)
    plt.close('all')
    fig, axes = plt.subplots(dpi=60)
    fig.suptitle(text, fontsize=20, fontweight='bold', verticalalignment='top')
    plt.axis('off')

    if removedNode is not None:
        nx.draw_networkx_nodes(G, pos=pos, node_size=600, nodelist=[removedNode],
                               node_color='red', label='Removed node')

    if articulationPoints is not None:
        nx.draw_networkx_nodes(G, pos=pos, node_size=600, nodelist=articulationPoints,
                               node_color='green', label='Articulation points')
    if kAugmentedNodes is not None:
        nx.draw_networkx_nodes(G, pos=pos, node_size=600, nodelist=kAugmentedNodes,
                               node_color='lightblue', label='New nodes')
    if removedEdge is not None:
        nx.draw_networkx_edges(G, pos=pos, edgelist=[removedEdge], width=4.0, edge_color='red',
                               label='Removed edge')
    if bridges is not None:
        nx.draw_networkx_edges(G, pos=pos, edgelist=bridges, width=4.0, edge_color='#ff8000', label='Bridges')
    if kAugmentedEdges is not None:
        nx.draw_networkx_edges(G, pos=pos, edgelist=kAugmentedEdges, width=4.0, edge_color='green', label='New edges')

    if sortedNodes is not None:
        nx.draw_networkx(G, pos, ax=axes, nodelist=sortedNodes, node_size=500, width=2.0, font_weight="bold",
                         node_color=nodeColor, edge_color=edgeColor)
    else:
        nx.draw_networkx(G, pos, ax=axes, node_size=500, width=2.0, font_weight="bold",
                         node_color=nodeColor, edge_color=edgeColor)
    plt.legend(scatterpoints=1, prop={'size': 15})
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
    # plt.show()
    return fig


def Reverse(tuples):
    new_tup = tuples[::-1]
    return new_tup


def create_figures_for_routing(G, source, target, path, excludedNodes=None, layout=None):

    # TODO Coloring in dijkstra_original seems of when loop is created
    # TODO Color source and target

    if excludedNodes is None:
        excludedNodes = []
    pos = createLayout(G, layout)

    excludedEdges = list()
    for node in excludedNodes:
        edges = G.edges(node)
        excludedEdges.extend(edges)

    pathEdges = list()
    for index in range(len(path)):
        if index == len(path)-1:
            break
        else:
            pathEdges.append((path[index], path[index+1]))

    loop_edge = None
    if len(path) != len(set(path)):
        loop_edge = (path[-2], path[-1])

    edgeColor = list()
    for edge in G.edges:
        if edge in pathEdges or Reverse(edge) in pathEdges:
            edgeColor.append("green")
        elif edge in excludedEdges or Reverse(edge) in excludedEdges:
            edgeColor.append("red")
        else:
            edgeColor.append("black")

    sortedNodes = sorted(dict(G.nodes), key=lambda g: g[0])

    figures = list()
    for activeNode in path:

        path_arrows = 'Path: '
        for index in range(len(path)):
            if index == len(path)-1:
                path_arrows += path[index]
            else:
                path_arrows += path[index] + ' \u2192 '

        plt.close('all')
        fig, axes = plt.subplots(dpi=60)
        plt.axis('off')
        text = 'Source: ' + source + ', Target: ' + target + '\n' + path_arrows
        fig.suptitle(text, fontsize=20, fontweight='bold', verticalalignment='top')

        nodeColor = list()
        for node in sortedNodes:
            if node in path or node == source or node == target:
                if node == source or node == target:
                    if node == activeNode:
                        nodeColor.append('yellow')
                    else:
                        nodeColor.append('purple')
                elif node == activeNode:
                    nodeColor.append('yellow')
                else:
                    nodeColor.append('green')
            elif node in excludedNodes:
                nodeColor.append('red')
            else:
                nodeColor.append('#1f78b4')

        nx.draw_networkx(G, pos, ax=axes, nodelist=sortedNodes, node_color=nodeColor, edge_color=edgeColor,
                         node_size=500, width=2.0, font_weight="bold")

        nx.draw_networkx_nodes(G, pos=pos, node_size=600, nodelist=[source, target],
                               node_color='purple', label='Source & Target')
        nx.draw_networkx_nodes(G, pos=pos, node_size=600, nodelist=[activeNode],
                               node_color='yellow', label='Current Node')
        nx.draw_networkx_nodes(G, pos=pos, node_size=600, nodelist=excludedNodes,
                               node_color='red', label='Excluded Nodes')

        nx.draw_networkx_edges(G, pos=pos, width=4, edgelist=excludedEdges, edge_color='red', label='Excluded Edges')
        nx.draw_networkx_edges(G, pos=pos, width=4, edgelist=pathEdges, edge_color='green', label='Path')

        if len(path) != len(set(path)):
            nx.draw_networkx_edges(G, pos=pos, width=4, edgelist=[loop_edge], edge_color='orange',
                                   label='Loop')

        plt.legend(scatterpoints=1, prop={'size': 15})
        labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
        # plt.show()
        figures.append(fig)

    return figures


def convertWeightsToFloat(G):
    for n in G.nodes:
        for v in G.neighbors(n):
            try:
                weight = G[n][v]['weight']
                G[n][v]['weight'] = float(weight)
                print('Here')
            except Exception as ex:
                print(ex)
    return G

def importGraph(filename):
    fh = open(filename, "rb")
    G = nx.read_edgelist(fh)
    fh.close()
    return nx.relabel_nodes(G, lambda x: str(x))


def importGraphGraphml(filename):
    fh = open(filename, "rb")
    G = nx.read_graphml(fh)
    fh.close()
    G = convertWeightsToFloat(G)
    return nx.relabel_nodes(G, lambda x: str(x))


def importGraphGml(filename):
    fh = open(filename, "rb")
    G = nx.read_gml(fh)
    fh.close()
    # G = convertWeightsToFloat(G)
    return nx.relabel_nodes(G, lambda x: str(x))


def exportGraphTxt(G, filename):
    nx.write_edgelist(G, filename)


def exportGraphGraphml(G, filename):
    print(G.nodes)
    nx.write_graphml_xml(G, filename, infer_numeric_types=True)


def exportGraphGml(G, filename):
    print(G.nodes)
    nx.write_gml(G, filename)


def saveGraphAsImage(filename, figure):
    figure.set_size_inches(16, 14)
    figure.savefig(filename, bbox_inches='tight', dpi=100)


def shortest_path_dijkstra(G, source, target, excludedNodes):
    newG = G.copy()
    for node in excludedNodes:
        newG.remove_node(node)

    return nx.dijkstra_path(newG, source, target, weight='weight')


def dijkstra_original(G, source, target, excludedNodes):
    return do.dijkstra_original(G, source, target, excludedNodes)


def nodes_connected(G, u, v):
    return u in G.neighbors(v)


def build_path(G, source, target, excluded_nodes, file_path):
    try:
        with open(file_path) as f:
            lines = f.read().splitlines()

        node_priorities = dict()
        for line in lines:
            match = re.fullmatch(r"(([A-Za-z0-9_@./#&+-])+{(([A-Za-z0-9_@./#&+-])+\b,*\b)+})", line)

            if match:
                sp1 = (match.string.split('{'))
                node = sp1[0]
                sp2 = (sp1[1].split('}'))
                priorities = (sp2[0].split(','))

                if not G.has_node(node):
                    raise nx.NetworkXNoPath(f"Node {node} not in graph")

                for priority in priorities:
                    if not nodes_connected(G, priority, node):
                        raise nx.NetworkXNoPath(f"Node {priority} not neighbor of {node}")
                    if priority in excluded_nodes:
                        priorities.remove(priority)

                if node not in excluded_nodes:
                    node_priorities[node] = priorities

            else:
                raise ImportError('Import error: Wrong syntax!')

        path = list()
        if source in node_priorities:
            path.append(source)
            priorities = node_priorities[source]
            path.append(priorities[0])
        else:
            raise nx.NetworkXNoPath(f"Source {source} not in the priority list")

        while True:
            if path[-1] == target:
                break
            if path[-1] in node_priorities:
                node = path[-1]
                nodes = node_priorities[node]
                path.append(nodes[0])
            else:
                break

            if len(path) != len(set(path)):
                break

        return path

    except Exception as e:
        raise e


def createRandomGraph():
    G = nx.fast_gnp_random_graph(random.randint(5,10), random.randint(1,5)*0.1)
    return nx.relabel_nodes(G, lambda x: str(x))

