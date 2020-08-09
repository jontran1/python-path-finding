import pygame
import heuristic
from queue import PriorityQueue


def build_path(parents, start, end):
    """
        Iterate backwards from end to start
        using the set parents.
    """

    while end != start:
        end.make_path()
        end = parents[end]


def a_star_path_finding(draw, grid, start, end, heuristic_func):
    """
        A* path finding algorthim.
        draw : lambda function. draw is called each iteration of the while loop.
        grid : 2D list of Nodes
        start : Node
        end : Node
        heuristic_func : The heuristic function takes in two arugments. 
        Both arugments are tuples (int, int). The function should return an integer. 

        return boolean True if path is found. False if path doesn't exist.
    """
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    previous_parent = {}

    # f(n) = g(n) + h(n)
    g_score = {node: float("inf") for row in grid for node in row}
    g_score[start] = 0

    f_score = {node: float("inf") for row in grid for node in row}
    f_score[start] = heuristic_func(
        start.get_pos(), end.get_pos()) + g_score[start]

    # Keeps track of whats in the open_set
    open_set_tracker = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        # Retreives the node with the best f_score
        current = open_set.get()[2]
        open_set_tracker.remove(current)

        if current == end:
            build_path(previous_parent, start, end)
            end.make_end()
            start.make_start()
            return True

        for neighbor in current.get_neighbors():
            current_to_neighbor_distance = g_score[current] + 1

            if current_to_neighbor_distance < g_score[neighbor]:
                previous_parent[neighbor] = current
                g_score[neighbor] = current_to_neighbor_distance
                f_score[neighbor] = g_score[neighbor] + \
                    heuristic_func(neighbor.get_pos(), end.get_pos())

                if neighbor not in open_set_tracker:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_tracker.add(neighbor)
                    neighbor.make_open()

        draw()

        if current != start:
            current.make_closed()

    return False
