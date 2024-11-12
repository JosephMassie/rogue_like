from __future__ import annotations

import math

type Coords = tuple[int, int]

class Int_Vector():
    def __init__(self, x: int, y: int) -> None:
        self._coords = (x, y)
    
    def __repr__(self) -> str:
        x, y = self._coords
        return f"int_vec [{x},{y}]"
    
    def setCoords(self, coords: Coords) -> None:
        self._coords = coords
    
    def getCoords(self) -> Coords:
        return self._coords
    
    def __eq__(self, value: Int_Vector) -> bool:
        x, y = self._coords
        xx, yy = value._coords
        return x == xx and y == yy
    
    def __add__(self, value: Int_Vector) -> Int_Vector:
        x, y = self._coords
        xx, yy = value._coords
        return Int_Vector(x + xx, y + yy)

    def __sub__(self, value: Int_Vector) -> Int_Vector:
        x, y = self._coords
        xx, yy = value._coords
        return Int_Vector(x - xx, y - yy)
    
    def __mul__(self, scalar: int):
        x, y = self._coords
        return Int_Vector(x * scalar, y * scalar)
    
    def __truediv__(self, scalar: float):
        x, y = self._coords
        xx = round(x / scalar)
        yy = round(y / scalar)
        return Int_Vector(xx, yy)
    
    def getNormalized(self) -> Int_Vector:
        return self / self.magnitude()
    
    def magnitude(self) -> float:
        x, y = self._coords
        return math.sqrt(x ** 2 + y ** 2)
    
    def plot_difference(self, end: Int_Vector) -> list[Int_Vector]:
        plots: list[Int_Vector] = list()

        start_x, start_y = self._coords
        end_x, end_y = end.getCoords()

        # absolute value of the delta between start and end Xs
        x_diff = end_x - start_x
        if x_diff < 0:
            x_diff *= -1

        # amount to increment x each iteration
        move_x = 0
        if start_x < end_x:
            move_x = 1
        else:
            move_x = -1
        
        # negative absolute value of the delta between start and end Ys
        y_diff = end_y - start_y
        if y_diff > 0:
            y_diff *= -1
        
        # amount to increment y each iteration
        move_y = 0
        if start_y < end_y:
            move_y = 1
        else:
            move_y = -1
        grid_deviation = x_diff + y_diff

        x = start_x
        y = start_y
        while True:
            plots.append(Int_Vector(x, y))
            if x == end_x and y == end_y:
                break
            e2 = grid_deviation * 2
            if e2 >= y_diff:
                if x == end_x:
                    break
                grid_deviation += y_diff
                x += move_x
            if e2 <= x_diff:
                if y == end_y:
                    break;
                grid_deviation += x_diff
                y += move_y
        return plots
