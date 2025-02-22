from Cell import Cell
import time
import random


class Maze:
    def __init__(
        self, x1, y1, num_rows, num_cols, cell_size_x, cell_size_y, win=None, seed=None
    ):
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._cells = []
        self._win = win

        self._seed = seed
        if self._seed:
            random.seed(self._seed)

        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r(0, 0)
        self._reset_cells_visited()

    def _create_cells(self):
        self._cells = [
            [Cell(self._win) for _ in range(self._num_rows)]
            for _ in range(self._num_cols)
        ]

        for i in range(self._num_cols):
            for j in range(self._num_rows):
                self._draw_cell(i, j)

    def _draw_cell(self, i, j):
        if self._win is None:
            return
        x1 = self._x1 + i * self._cell_size_x
        y1 = self._y1 + j * self._cell_size_y
        x2 = x1 + self._cell_size_x
        y2 = y1 + self._cell_size_y
        self._cells[i][j].draw(x1, y1, x2, y2)
        self._animate()

    def _animate(self):
        if self._win is None:
            return
        self._win.redraw()

    def _break_entrance_and_exit(self):
        self._cells[0][0].has_top_wall = False
        self._draw_cell(0, 0)
        self._cells[self._num_cols - 1][self._num_rows - 1].has_bottom_wall = False
        self._draw_cell(self._num_cols - 1, self._num_rows - 1)

    def _break_walls_r(self, i, j):
        self._cells[i][j].visited = True
        while True:
            new_list = [
                (i - 1, j),
                (i + 1, j),
                (i, j - 1),
                (i, j + 1),
            ]
            not_visited = []
            for q in new_list:
                if (
                    q[0] >= 0
                    and q[1] >= 0
                    and q[0] < self._num_cols
                    and q[1] < self._num_rows
                ):
                    if not self._cells[q[0]][q[1]].visited:
                        not_visited.append([q[0], q[1]])

            if len(not_visited) == 0:
                self._draw_cell(i, j)
                return
            else:
                random_dir = random.choice(not_visited)
                if random_dir[0] == i + 1 and random_dir[1] == j:
                    self._cells[i][j].has_right_wall = False
                    self._cells[random_dir[0]][random_dir[1]].has_left_wall = False
                elif random_dir[0] == i - 1 and random_dir[1] == j:
                    self._cells[i][j].has_left_wall = False
                    self._cells[random_dir[0]][random_dir[1]].has_right_wall = False
                elif random_dir[0] == i and random_dir[1] == j + 1:
                    self._cells[i][j].has_bottom_wall = False
                    self._cells[random_dir[0]][random_dir[1]].has_top_wall = False
                elif random_dir[0] == i and random_dir[1] == j - 1:
                    self._cells[i][j].has_top_wall = False
                    self._cells[random_dir[0]][random_dir[1]].has_bottom_wall = False

            self._break_walls_r(random_dir[0], random_dir[1])

    def _reset_cells_visited(self):
        for i in self._cells:
            for j in i:
                j.visited = False

    def solve(self):
        return self._solve_r(0, 0)

    def _solve_r(self, i, j):
        self._animate()
        self._cells[i][j].visited = True
        if self._cells[i][j] == self._cells[self._num_cols - 1][self._num_rows - 1]:
            return True

        new_list = [
            (i - 1, j),
            (i + 1, j),
            (i, j - 1),
            (i, j + 1),
        ]
        for q in new_list:
            if (
                q[0] >= 0
                and q[1] >= 0
                and q[0] < self._num_cols
                and q[1] < self._num_rows
            ):
                if not self._cells[q[0]][q[1]].visited and not self._wall_between(
                    i, j, q
                ):
                    self._cells[i][j]._draw_move(self._cells[q[0]][q[1]])
                    if self._solve_r(q[0], q[1]):
                        return True
                    else:
                        self._cells[i][j]._draw_move(self._cells[q[0]][q[1]], True)

        return False

    def _wall_between(self, i, j, random_dir):
        if random_dir[0] == i + 1 and random_dir[1] == j:
            return self._cells[i][j].has_right_wall
        elif random_dir[0] == i - 1 and random_dir[1] == j:
            return self._cells[i][j].has_left_wall
        elif random_dir[0] == i and random_dir[1] == j + 1:
            return self._cells[i][j].has_bottom_wall
        elif random_dir[0] == i and random_dir[1] == j - 1:
            return self._cells[i][j].has_top_wall
