from Point import Point
from Line import Line


class Cell:
    def __init__(self, win=None):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self._x1 = None
        self._y1 = None
        self._x2 = None
        self._y2 = None

        self.visited = False

        self._win = win

    def draw(self, tx, ty, bx, by):
        if self._win is None:
            return
        self._x1 = tx
        self._x2 = bx
        self._y1 = ty
        self._y2 = by
        if self.has_left_wall:
            point1 = Point(tx, ty)
            point2 = Point(tx, by)
            line = Line(point1, point2)
            self._win.draw_line(line, "black")
        else:
            point1 = Point(tx, ty)
            point2 = Point(tx, by)
            line = Line(point1, point2)
            self._win.draw_line(line, "white")
        if self.has_right_wall:
            point1 = Point(bx, ty)
            point2 = Point(bx, by)
            line = Line(point1, point2)
            self._win.draw_line(line, "black")
        else:
            point1 = Point(bx, ty)
            point2 = Point(bx, by)
            line = Line(point1, point2)
            self._win.draw_line(line, "white")
        if self.has_top_wall:
            point1 = Point(tx, ty)
            point2 = Point(bx, ty)
            line = Line(point1, point2)
            self._win.draw_line(line, "black")
        else:
            point1 = Point(tx, ty)
            point2 = Point(bx, ty)
            line = Line(point1, point2)
            self._win.draw_line(line, "white")
        if self.has_bottom_wall:
            point1 = Point(tx, by)
            point2 = Point(bx, by)
            line = Line(point1, point2)
            self._win.draw_line(line, "black")
        else:
            point1 = Point(tx, by)
            point2 = Point(bx, by)
            line = Line(point1, point2)
            self._win.draw_line(line, "white")

    def _draw_move(self, to_cell, undo=False):
        if self._win is None:
            return
        fill_color = "gray"
        if not undo:
            fill_color = "red"

        point1 = Point((self._x1 + self._x2) // 2, (self._y1 + self._y2) // 2)
        point2 = Point(
            (to_cell._x1 + to_cell._x2) // 2, (to_cell._y1 + to_cell._y2) // 2
        )

        line = Line(point1, point2)
        self._win.draw_line(line, fill_color)
