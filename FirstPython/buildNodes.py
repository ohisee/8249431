#!/usr/bin/python

def create_tour(nodes):
    visited = [];
    tour = [];
    degree_count = 2;
    for i in range(len(nodes)):
        degree = 0;
        current = i;
        while degree < degree_count and (current + 1) < len(nodes):
            if nodes[current + 1] not in visited:
                tour.append((nodes[i], nodes[current + 1]));
                visited.append(nodes[current + 1]);
            degree += 1;
            current += 1;
    tour.append((nodes[-2], nodes[-1]));
    return tour;

def create_tour_comp(nodes):
    # connect the first node with the second node, and second with third ..., and last with the first node
    tour = [];
    for i in range(len(nodes)):
        tour.append((nodes[i], nodes[(i + 1) % len(nodes)]));
    return tour;


if __name__ == "__main__":
    print (create_tour([1, 2, 3, 4, 5, 6]));
    print (create_tour_comp([1, 2, 3, 4, 5, 6]));
