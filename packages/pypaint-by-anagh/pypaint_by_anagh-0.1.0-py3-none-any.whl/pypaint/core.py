import turtle
import math

def draw_square(size=100, color="black"):
    turtle.fillcolor(color)
    turtle.begin_fill()
    turtle.pendown()
    for _ in range(4):
        turtle.forward(size)
        turtle.right(90)
    turtle.end_fill()
    turtle.penup()

def draw_rectangle(width=150, height=80, color="black"):
    turtle.fillcolor(color)
    turtle.begin_fill()
    turtle.pendown()
    for _ in range(2):
        turtle.forward(width)
        turtle.right(90)
        turtle.forward(height)
        turtle.right(90)
    turtle.end_fill()
    turtle.penup()

def draw_circle(radius=50, color="black"):
    turtle.fillcolor(color)
    turtle.begin_fill()
    turtle.pendown()
    turtle.circle(radius)
    turtle.end_fill()
    turtle.penup()

def draw_line(length=100, color="black"):
    turtle.pencolor(color)
    turtle.pendown()
    turtle.forward(length)
    turtle.penup()

def draw_triangle(a=100, b=100, c=100, color="black"):
    turtle.fillcolor(color)
    turtle.begin_fill()
    turtle.pendown()
    
    turtle.forward(a)
    angle_b = math.degrees(math.acos((a**2 + c**2 - b**2) / (2 * a * c)))
    turtle.left(180 - angle_b)
    turtle.forward(b)
    angle_c = math.degrees(math.acos((a**2 + b**2 - c**2) / (2 * a * b)))
    turtle.left(180 - angle_c)
    turtle.forward(c)
    
    turtle.end_fill()
    turtle.penup()

def draw_pentagon(size=100, color="black"):
    turtle.fillcolor(color)
    turtle.begin_fill()
    turtle.pendown()
    for _ in range(5):
        turtle.forward(size)
        turtle.right(72)
    turtle.end_fill()
    turtle.penup()

def finish():
    turtle.done()
