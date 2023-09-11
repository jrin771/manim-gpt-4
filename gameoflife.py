from manim import *
import numpy as np

class GameOfLife(Scene):
    def construct(self):
        rows, cols = 20, 20
        cell_size = 0.3
        grid = np.random.choice([0, 1], size=(rows, cols), p=[0.8, 0.2])

        squares = [[
            Rectangle(height=cell_size, width=cell_size, fill_opacity=0.8 if grid[i, j] else 0.0, fill_color=GREEN)
            for j in range(cols)]
            for i in range(rows)
        ]

        for i in range(rows):
            for j in range(cols):
                squares[i][j].next_to(ORIGIN, RIGHT, buff=0)
                squares[i][j].shift(j * RIGHT * cell_size + LEFT * 3)  # Shifted to the left
                squares[i][j].shift(i * UP * cell_size + DOWN * rows * cell_size / 2)

        grid_group = VGroup(*[squares[i][j] for i in range(rows) for j in range(cols)])
        self.add(grid_group)

        for _ in range(50):
            new_grid = np.zeros((rows, cols))
            for i in range(rows):
                for j in range(cols):
                    state = grid[i, j]
                    neighbors = np.sum(grid[max(i-1, 0):min(i+2, rows), max(j-1, 0):min(j+2, cols)]) - state
                    if state and (neighbors < 2 or neighbors > 3):
                        new_grid[i, j] = 0
                    elif not state and neighbors == 3:
                        new_grid[i, j] = 1
                    else:
                        new_grid[i, j] = state

                    if new_grid[i, j]:
                        squares[i][j].set_fill(GREEN, opacity=0.8)
                    else:
                        squares[i][j].set_fill(opacity=0.0)

            grid = np.copy(new_grid)
            self.wait(0.2)
