#!/usr/bin/python

def create_tour(nodes):
    tour = [];
    for i in range(len(nodes)):
        a = nodes[i];
        for n in nodes[i + 1:]:
            tour.append((a, n));
    return tour;

if __name__ == "__main__":
    print (create_tour([1, 2, 3, 4, 5, 6, 7, 8, 9]));
