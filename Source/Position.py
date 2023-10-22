from __future__ import annotations
from random import randint

class Position:

    def __init__(self : Position, x : int = None, y : int = None):
        if x == None:
            x = randint(3,6)
        if y == None:
            y = randint(3,6)
        self.__x : int = x
        self.__y : int = y

    def __str__(self : Position) -> str:
        return f"Position :  (X = {self.x} Y = {self.y})"
    
    def __repr__(self) -> str:
        return f"x = {self.x} y = {self.y}"
    
    def __eq__(self, cell: Position) -> bool:
        return self.y == cell.y and self.x == cell.x
    
    @property
    def x(self : Position) -> int:
        return self.__x

    @property
    def y(self : Position) -> int:
        return self.__y
    
    @property
    def id(self: Position) -> str:
        return self.__id
    
    @x.setter
    def x(self : Position, x : int) -> None:
        self.__x = x

    @y.setter
    def y(self : Position, y : int) -> None:
        self.__y = y

    def __eq__(self, position : Position) -> bool:
        return (self.x == position.x and self.y == position.y)
    
    def add_x(self: Position, delta: int):
        self.__x += delta

    def add_y(self: Position, delta: int):
        self.__y += delta