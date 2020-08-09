import pygame
import path_finding as pf
import heuristic

WIDTH = 800
WINDOW = pygame.display.set_mode([WIDTH, WIDTH])
pygame.display.set_caption("Path Finding Visualizer")

RED = (255, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)


class Node:

    # Constructor
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows

    def get_pos(self):
        return self.row, self.col

    def is_closed(self):
        return self.color == RED

    def is_open(self):
        return self.color == GREEN

    def is_barrier(self):
        return self.color == BLACK

    def is_start(self):
        return self.color == ORANGE

    def is_end(self):
        return self.color == PURPLE

    def reset(self):
        self.color = WHITE

    def make_start(self):
        self.color = ORANGE

    def make_closed(self):
        self.color = RED

    def make_open(self):
        self.color = GREEN

    def make_barrier(self):
        self.color = BLACK

    def make_end(self):
        self.color = TURQUOISE

    def make_path(self):
        self.color = PURPLE

    # Draws a rectangle at the node's x and y position with a
    # length and width equals to the node's width.
    def draw(self):
        pygame.draw.rect(WINDOW, self.color, (self.x,
                                              self.y, self.width, self.width))

    def update_neighbors(self, grid):
        self.neighbors = []

        # Each if statement checks if the neigbor is within the bounds
        # and checks if the neigbor is not a barrier.

        # DOWN
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row + 1][self.col])

        # UP
        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row - 1][self.col])

        # RIGHT
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col + 1])

        # LEFT
        if self.col > 0 and not grid[self.row][self.col-1].is_barrier():
            self.neighbors.append(grid[self.row][self.col-1])

    def get_neighbors(self):
        return self.neighbors


def get_clicked_pos(pos, rows, width):

    node_width = width // rows
    y, x = pos

    row = y // node_width
    col = x // node_width

    return row, col


def make_grid(rows, width):
    grid = []
    node_width = width // rows

    for row in range(rows):
        grid.append([])
        for col in range(rows):
            node = Node(row, col, node_width, rows)
            grid[row].append(node)

    return grid


def draw_grid(window, rows, width):

    node_width = width // rows

    # Horizontal lines.
    for i in range(rows):
        pygame.draw.line(window, GREY, (0, i * node_width),
                         (width, i * node_width))

    # Vertical lines.
    for i in range(rows):
        pygame.draw.line(window, GREY, (i * node_width, 0),
                         (i * node_width, width))


def update_nodes_neighbors(grid):
    """
        Every single node will have a list of thier neighbors.
        This list will contain the current state of each node
        to insure that the grid is accurate.
    """
    for row in grid:
        for node in row:
            node.update_neighbors(grid)


def draw(window, grid, rows, width):
    """
        Draws the entire gird. 
        Can be used to redraw the grid.
    """
    window.fill(WHITE)

    for row in grid:
        for node in row:
            node.draw()

    draw_grid(window, rows, width)
    pygame.display.update()


def main(window, width):
    ROWS = 50

    grid = make_grid(ROWS, width)

    start = None
    end = None

    run = True

    while run:

        draw(window, grid, ROWS, width)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                run = False
            if pygame.mouse.get_pressed()[0]:  # LEFT MOUSE CLICK

                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                node = grid[row][col]

                if not start and node != end:
                    start = node
                    node.make_start()

                elif not end and node != start:
                    end = node
                    node.make_end()

                elif node != end and node != start:
                    node.make_barrier()

            elif pygame.mouse.get_pressed()[2]:  # RIGHT MOUSE CLICK

                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                node = grid[row][col]
                node.reset()

                if node == start:
                    start = None
                if node == end:
                    end = None

            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_SPACE and start and end:
                    update_nodes_neighbors(grid)

                    pf.a_star_path_finding(lambda: draw(window, grid,
                                                        ROWS, width), grid, start, end, heuristic.manhattan_distance)
    pygame.quit()


main(WINDOW, WIDTH)
