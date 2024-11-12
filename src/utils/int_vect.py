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
    
    def magnitude(self) -> float:
        x, y = self._coords
        return math.sqrt(x ** 2 + y ** 2)
