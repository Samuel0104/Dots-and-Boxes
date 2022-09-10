from pygame import Rect
import colors as c

class Side(Rect):
    def __init__(self, x, y, width, height, color=c.light):
        Rect.__init__(self, x, y, width, height)
        self.color = color

class Box(Rect):
    def __init__(self, x=0, y=0, side=0, color=c.lightSquare):
        Rect.__init__(self, x, y, side, side)
        self.color = color

        self.sides = []
        for i in (-6, side):
            self.sides.append(Side(x + i, y, 6, side))
            self.sides.append(Side(x, y + i, side, 6))

        self.count = 0 # Number of selected sides

    def adjust(self, m, size, index, color): # Color and relative position/size
        Rect.__init__(self, m*(index//size) + 25, m*(index%size) + 25, m - 6, m - 6)
        self.color = color
        colors = [s.color for s in self.sides]
        self.sides.clear()
        for i, n in enumerate([-6, m - 6]):
            self.sides.append(Side(self.x + n, self.y, 6, m - 6, colors[2*i]))
            self.sides.append(Side(self.x, self.y + n, m - 6, 6, colors[2*i + 1]))
