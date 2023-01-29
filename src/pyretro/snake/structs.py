from dataclasses import dataclass


@dataclass
class Point:
    x: int
    y: int

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __radd__(self, other):
        return Point(other.x + self.x, other.y + self.y)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def __rsub__(self, other):
        return Point(other.x - self.x, other.y - self.y)

    def to_tuple(self):
        return self.x, self.y


@dataclass(frozen=True)
class Size:
    width: int
    height: int

    def __iter__(self):
        yield self.width
        yield self.height

    def __mul__(self, other):
        return type(self)(self.width * other.width, self.height * other.height)  # noqa

    def __floordiv__(self, other):
        return type(self)(self.width / other.width, self.height / other.height)  # noqa

    def to_tuple(self):
        return self.width, self.height


@dataclass(frozen=True)
class RectColors:
    fill: str = "green"
    border: str = "black"