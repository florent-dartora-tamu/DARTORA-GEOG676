import math

i = 0

# Read data in the file
filename = '/Users/Florent/Documents/Github Repositories/MY_PROJECTS/02_GIS_Training/GIS Programming/shape.txt'
with open(filename) as file_object:
    lines = file_object.readlines()

# Define shape Class : Rectangle
class Rectangle():
    def __init__(self, l, w):
        self.l = l
        self.w = w
    def getArea(self):
        return str(self.l * self.w)
    
# Define shape Class : Circle
class Circle():
    def __init__(self, r):
        self.r = r
    def getArea(self):
        return str(math.pi * (self.r)**2)
    
# Define shape Class : Triangle
class Triangle():
    def __init__(self, b, h):
        self.b = b
        self.h = h
    def getArea(self):
        return str((self.b * self.h)/2)
   

# Loop on the lines of the file
for line in lines:
    i +=1 
    tokens = line.split(",") # We split our string on coma
    if tokens[0]=="Rectangle":
        rectangle = Rectangle(int(tokens[1]), int(tokens[2]))
        print ("Area of the shape #" + str(i) +  " is " + rectangle.getArea())
    elif tokens[0]=="Circle":
        circle = Circle(int(tokens[1]))
        print ("Area of the shape #" + str(i) +  " is " + circle.getArea())
    elif tokens[0]=="Triangle":
        triangle = Triangle(int(tokens[1]), int(tokens[2]))
        print ("Area of the shape #" + str(i) +  " is " + triangle.getArea())
    else :
        print("Unknown shape !")
