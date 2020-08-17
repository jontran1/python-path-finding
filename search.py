import pygame


def breadth_first_search(draw, start, end):
    """
        draw: lambda function. This function is called each while loop iteration. 
        This will update the grid for the user.
        start (Node): A starting node.
        end (Node): A ending node.
    """
    queue = []
    visited = []
    queue.append(start)

    while len(queue) > 0:
        current = queue.pop(0)

        if current == end:
            start.make_start()
            end.make_end()
            return True

        for neighbor in current.get_neighbors():
            if not neighbor in visited:
                queue.append(neighbor)
                visited.append(neighbor)
                neighbor.make_open()

        if current != end:
            current.make_closed()

        draw()

    return False


def depth_first_search(draw, start, end):
    """
        draw: lambda function. This function is called each while loop iteration. 
        This will update the grid for the user.
        start (Node): A starting node.
        end (Node): A ending node.
    """
    visited = []
    stack = []
    stack.append(start)

    while len(stack) > 0:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = stack.pop()

        if current == end:
            start.make_start()
            end.make_end()
            return True

        for neighbor in current.get_neighbors():
            if not neighbor in visited:
                stack.append(neighbor)
                visited.append(neighbor)
                neighbor.make_open()

        if current != end:
            current.make_closed()

        draw()

    return False
