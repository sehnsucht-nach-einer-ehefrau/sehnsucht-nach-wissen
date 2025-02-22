class Line:
    def __init__(self, point1, point2):
        self._point1, self._point2 = point1, point2

    def draw(self, canvas, fill_color):
        canvas.create_line(
            self._point1.x,
            self._point1.y,
            self._point2.x,
            self._point2.y,
            fill=fill_color,
            width=2,
        )
