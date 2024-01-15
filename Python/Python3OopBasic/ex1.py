import math

class Point:
    def __init__(self, x=0.0, y=0.0):
        if isinstance(x,(int, float)) and isinstance(y,(int, float)):
            self.x = x
            self.y = y
        else:
            print("Error: points must be numbers")

    def distance_from_origin(self):
        return math.sqrt(self.x**2 + self.y**2)

my_points = Point(1.2, 5.5)
print(my_points.distance_from_origin())