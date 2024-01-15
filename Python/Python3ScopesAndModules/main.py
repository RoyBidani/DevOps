# ex1:
def is_defined_global(name):
    return name in globals()


name = "Roy"
print(is_defined_global("name"))
print(is_defined_global("Last_name"))


# ex2:
import areas

radius = 10
height = 8
width = 4
print("Circle area:", areas.circle_area(radius))
print("Triangle area:", areas.triangle_area(height,width))
print("Rectangle area:", areas.rectangle_area(height,width))


# ex3:
import os

print("Operating system name:", os.name)
print("Logged user:", os.getlogin())
print("Current working directory:", os.getcwd())



