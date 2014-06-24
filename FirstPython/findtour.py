#!/usr/bin/python
# -*- coding: utf-8 -*-

# Find Eulerian Tour
#
# Write a function that takes in a graph
# represented as a list of tuples
# and return a list of nodes that
# you would follow on an Eulerian Tour
#
# For example, if the input graph was
# [(1, 2), (2, 3), (3, 1)]
# A possible Eulerian tour would be [1, 2, 3, 1]
#
# [(0, 1), (1, 5), (1, 7), (4, 5), (4, 8), (1, 6), (3, 7), (5, 9), (2, 4), (0, 4), (2, 5), (3, 6), (8, 9)]
#
# [(1, 13), (1, 6), (6, 11), (3, 13), (8, 13), (0, 6), (8, 9),(5, 9), (2, 6), (6, 10), (7, 9), (1, 12), 
# (4, 12), (5, 14), (0, 1),  (2, 3), (4, 11), (6, 9), (7, 14), (10, 13)]
#
# [(8, 16), (8, 18), (16, 17), (18, 19), (3, 17), (13, 17), (5, 13),(3, 4), 
# (0, 18), (3, 14), (11, 14), (1, 8), (1, 9), (4, 12), (2, 19),(1, 10), (7, 9), 
# (13, 15), (6, 12), (0, 1), (2, 11), (3, 18), (5, 6), (7, 15), (8, 13), (10, 17)]

def find_edges(node, graph):
    nodes = [];
    for a, b in graph:
        if a == node:
            nodes.append(b);
        elif b == node:
            nodes.append(a);
    return nodes;

def build_edges(graph):
    nodes = to_nodes(graph);
    edges = {};
    for node in nodes:
        edges[node] = find_edges(node, graph);
    return edges;

def to_nodes(graph):
    nodes = [];
    for a, b in graph:
        if a not in nodes:
            nodes.append(a);
        if b not in nodes:
            nodes.append(b);
    return nodes;

def find_eu_path(graph, nodes, edges):
    path, visited = [], [];
    walk(edges, nodes[0], nodes[0], path, graph, visited);
    return path;

def walk(edges, start, node, path, graph, visited):
    path.append(node);
    for p in edges[node]:
        if not has_visited(node, p, visited):
            visited.append((node, p));
            walk(edges, start, p, path, graph, visited);

def has_visited(a, b, visited):
    return (a, b) in visited or (b, a) in visited;

def group_edges(edges):
    for edge in edges:
        t = edges[edge][0];
        edges[edge] = edges[edge][1:];
        edges[edge].append(t);

def find_eulerian_tour(graph):
    edges = build_edges(graph);
    nodes = to_nodes(graph);
    path = find_eu_path(graph, nodes, edges);
    index = 0;
    while (path[0] != path[-1] and index < 3):
        group_edges(edges);
        path = find_eu_path(graph, nodes, edges);
        index = index + 1;
    return path;

if __name__ == "__main__":
    graph = [(0, 1), (1, 5), (1, 7), (4, 5), (4, 8), (1, 6), (3, 7), (5, 9), (2, 4), (0, 4), (2, 5), (3, 6), (8, 9)];
    print (find_eulerian_tour(graph));
