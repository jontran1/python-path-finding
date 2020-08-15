import pygame
import heuristic
from queue import PriorityQueue


def build_path(parents, start, end):
    """
        Iterate backwards from end to start
        using the set parents.
    """

    while end != start:
        if not end:
            break
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


def dijkstra_shortest_path(draw, grid, start, end):
    """
        draw: lambda function that is run each iteration to upgrade grid.
        grid: 2D array containing Node objects.
        start: Node object
        end: Node object
    """

    count = 0
    open_set = PriorityQueue()

    # Set distance for all nodes to infinity but start node.
    distance_set = {node: float("inf") for row in grid for node in row}
    distance_set[start] = 0

    # Parent set for building path.
    previous_parent = {}

    # Start open set by placing start node in side.
    # PriorityQueue by distance.
    open_set.put((distance_set[start], count, start))

    # Tracks whats in the open set.
    open_set_tracker = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]
        open_set_tracker.remove(current)

        if current == end:
            build_path(previous_parent, start, end)
            end.make_end()
            start.make_start()
            return True

        for neighbor in current.get_neighbors():

            current_to_neighbor = distance_set[current] + 1

            if current_to_neighbor < distance_set[neighbor]:
                distance_set[neighbor] = current_to_neighbor
                previous_parent[neighbor] = current

                if neighbor not in open_set_tracker:
                    count += 1
                    open_set.put((distance_set[neighbor], count, neighbor))
                    open_set_tracker.add(neighbor)
                    neighbor.make_open()

        draw()

        if current != start:
            current.make_closed()

    return False


class BFS_DATA:

    """
        Holds the necessary data structures for Bi-Directional BFS.
    """

    # Constructor
    def __init__(self, grid, start):
        self.count = 0
        self.open_set = PriorityQueue()

        self.distance_set = {node: float("inf")
                             for row in grid for node in row}

        self.distance_set[start] = 0

        self.open_set.put((self.distance_set[start], self.count, start))
        self.open_set_tracker = {start}

        self.previous_parent = {}

    def get_open_set(self):
        return self.open_set

    def get_open_set_tracker(self):
        return self.open_set_tracker

    def get_distance_set(self):
        return self.distance_set

    def get_previous_parent(self):
        return self.previous_parent

    def get_count(self):
        return self.count

    def increment_count(self):
        self.count = self.count + 1


def bi_directional_search(draw, grid, start, end):
    """
        draw: lambda function that draws and updates the grid.
        grid: 2D list of Nodes
        start: Node
        end: Node
    """

    bfs_start = BFS_DATA(grid, start)
    bfs_end = BFS_DATA(grid, end)

    while not bfs_start.get_open_set().empty() and not bfs_end.get_open_set().empty():

        previous, collision = bi_directional_search_helper(
            start, bfs_start, bfs_end)

        if collision:
            # build path.
            build_bi_directional_path(
                bfs_start, bfs_end, previous, start, collision, end)
            start.make_start()
            end.make_end()
            return True

        previous, collision = bi_directional_search_helper(
            end, bfs_end, bfs_start)

        if collision:
            build_bi_directional_path(
                bfs_end, bfs_start, previous, end, collision, start)
            start.make_start()
            end.make_end()
            return True

        draw()

    return False


def build_bi_directional_path(bfs_start, bfs_end, previous, start, collision, end):
    """
        Builds the bi-directional path using start, collision, and end.
    """
    build_path(bfs_end.get_previous_parent(), end, collision)
    previous_parent = bfs_start.get_previous_parent()
    previous_parent[previous] = collision
    build_path(previous_parent, start, collision)


def bi_directional_search_helper(start, bfs_source, bfs_data):
    """
        start: Node
        bfs_source: BFS_DATA
        bfs_data: BFS_DATA
        Does one interation of a Bi-Directional BFS. 
        If it BFS visits a node in bfs_node. It found a collision. 
    """

    open_set_source = bfs_source.get_open_set()
    open_set_tracker_source = bfs_source.get_open_set_tracker()
    distance_set_source = bfs_source.get_distance_set()
    previous_parent_source = bfs_source.get_previous_parent()

    current = open_set_source.get()[2]
    open_set_tracker_source.remove(current)

    if current in bfs_data.get_open_set_tracker():
        return None, current

    for neighbor in current.get_neighbors():

        current_to_neighbor = distance_set_source[current] + 1

        if current_to_neighbor < distance_set_source[neighbor]:
            distance_set_source[neighbor] = current_to_neighbor
            previous_parent_source[neighbor] = current

            if neighbor not in open_set_tracker_source:
                bfs_source.increment_count()
                open_set_source.put(
                    (distance_set_source[neighbor], bfs_source.get_count(), neighbor))
                open_set_tracker_source.add(neighbor)
                neighbor.make_open()

    if current != start:
        current.make_closed()

    return current, None
