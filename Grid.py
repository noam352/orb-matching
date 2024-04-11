from collections import Counter
import random
import pygame
import sys
import time

from Orb import Orb
from Color import Color


class Grid:
    BACKGROUND_COLOR = (30, 30, 30)

    def __init__(self, grid_rows, grid_columns) -> None:
        self.grid_rows = grid_rows
        self.grid_columns = grid_columns
        self.grid = [
            [Orb(i, j, Color.random()) for i in range(self.grid_columns)]
            for j in range(self.grid_rows)
        ]

    def find_matched_orbs(self):

        matched_set = set()

        # Horizontal
        for j in range(self.grid_columns - 2):
            for i in range(self.grid_rows):
                if not all([self.grid[i][j + c] for c in range(3)]):
                    continue
                orb1_color = self.grid[i][j].get_color().value
                orb2_color = self.grid[i][j + 1].get_color().value
                orb3_color = self.grid[i][j + 2].get_color().value

                if orb1_color == orb2_color and orb1_color == orb3_color:
                    matched_set.update([(i, j), (i, j + 1), (i, j + 2)])

        # Vertical
        for j in range(self.grid_columns):
            for i in range(self.grid_rows - 2):
                if not all([self.grid[i + c][j] for c in range(3)]):
                    continue
                orb1_color = self.grid[i][j].get_color().value
                orb2_color = self.grid[i + 1][j].get_color().value
                orb3_color = self.grid[i + 2][j].get_color().value

                if orb1_color == orb2_color and orb1_color == orb3_color:
                    matched_set.update([(i, j), (i + 1, j), (i + 2, j)])

        return list(matched_set)

    def draw_grid(self, fall=False, frame=True):
        screen.fill(Grid.BACKGROUND_COLOR)
        for row in self.grid:
            for orb in row:
                if orb is None:
                    continue
                orb_x, orb_y = orb.get_coordinates(fall=fall)
                pygame.draw.circle(
                    screen,
                    orb.get_color().value,
                    (orb_x, orb_y),
                    (Orb.ORB_SIZE + orb.temp_size) // 2,
                )
        # clock.tick(120)
        if frame:
            pygame.display.flip()

    def draw_hover_orb(self, color, event_pos):
        self.draw_grid(frame=False)
        pygame.draw.circle(screen, color, event_pos, Orb.ORB_SIZE // 2)
        # clock.tick(120)
        pygame.display.flip()


grid = Grid(5, 6)
# Initialize Pygame
pygame.init()
clock = pygame.time.Clock()
# Calculate window size
window_width = grid.grid_columns * (Orb.ORB_SIZE + Orb.ORB_MARGIN) + Orb.ORB_MARGIN
window_height = grid.grid_rows * (Orb.ORB_SIZE + Orb.ORB_MARGIN) + Orb.ORB_MARGIN
# restricted_area = pygame.Rect(0, 0, window_width, int(2 / 3 * window_height))

# Set up the display
screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Orb Matching Game")
# Game loop
running = True
selected_orb = None
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Mouse button down event
        if event.type == pygame.MOUSEBUTTONDOWN:
            for orb in [orb for row in grid.grid for orb in row if orb is not None]:
                pos = orb.get_coordinates()
                if (event.pos[0] - pos[0]) ** 2 + (event.pos[1] - pos[1]) ** 2 <= (
                    Orb.ORB_SIZE // 2
                ) ** 2:
                    selected_orb = orb
                    selected_orb.color = Color.Black
                    break

        # Mouse button up event
        if event.type == pygame.MOUSEBUTTONUP:
            if selected_orb:
                selected_orb.color = selected_orb.perma_color
                selected_orb = None

    # # Get current mouse position
    # mouse_pos = pygame.mouse.get_pos()

    # # Check if the mouse is in the restricted area
    # if restricted_area.collidepoint(mouse_pos):
    #     # Move the mouse to the default position
    #     pygame.mouse.set_pos((mouse_pos[0], int(2 / 3 * window_height)))

    if selected_orb:
        selected_orb_pos = selected_orb.get_pos()
        for orb in [orb for row in grid.grid for orb in row]:
            if orb is None:
                continue
            if selected_orb is not orb:
                coordinates = orb.get_coordinates()
                pos = orb.get_pos()
                if (pygame.mouse.get_pos()[0] - coordinates[0]) ** 2 + (
                    pygame.mouse.get_pos()[1] - coordinates[1]
                ) ** 2 <= (Orb.ORB_SIZE // 2) ** 2:
                    grid.grid[selected_orb_pos[1]][selected_orb_pos[0]] = orb
                    grid.grid[pos[1]][pos[0]] = selected_orb
                    selected_orb.set_pos(pos[0], pos[1])
                    orb.set_pos(selected_orb_pos[0], selected_orb_pos[1])
                    break
        grid.draw_hover_orb(selected_orb.perma_color.value, pygame.mouse.get_pos())
        continue

    matched = grid.find_matched_orbs()
    if not matched:
        continue

    # count how many orbs to drop per column
    column_counter = Counter()
    max_dic = {}
    for x, y in matched:
        # grid.grid[x][y].color = Color.white
        if y not in max_dic:
            max_dic[y] = [x]
        else:
            max_dic[y].append(x)
        column_counter[y] += 1

    for y in max_dic:
        max_dic[y] = list(sorted(max_dic[y]))

    grid.draw_grid()
    time.sleep(0.5)
    for x, y in matched:
        grid.grid[x][y] = None

    grid.draw_grid()
    time.sleep(0.5)

    # print()
    for col in max_dic:
        curr = grid.grid_rows - 1
        inc = 0

        while curr >= 0:
            if max_dic[col] and curr == max_dic[col][-1]:
                inc += 1
                max_dic[col].pop()
            elif grid.grid[curr][col] and inc > 0:
                p = grid.grid[curr][col]
                # print(curr, col, inc, p.get_pos())
                new_orb = Orb(p.get_pos()[0], p.get_pos()[1] + inc, p.get_color())
                new_orb.add_falling(inc)
                grid.grid[curr + inc][col] = new_orb
                # print(curr + inc, col, new_orb.get_pos())
                grid.grid[curr][col] = None
            curr -= 1

    for col in column_counter:
        while column_counter[col] > 0:
            # print(column_counter[col], col)
            grid.grid[column_counter[col] - 1][col] = Orb(
                col, column_counter[col] - 1, Color.random()
            )
            grid.grid[column_counter[col] - 1][col].add_falling(column_counter[col] + 1)
            column_counter[col] -= 1

    while any([orb.falling > 0 for row in grid.grid for orb in row if orb != None]):
        grid.draw_grid(fall=True)

    ##### Find out why some grid squares have None
    grid.draw_grid()
    # pygame.display.flip()
    # time.sleep(0.5)


pygame.quit()
sys.exit()
