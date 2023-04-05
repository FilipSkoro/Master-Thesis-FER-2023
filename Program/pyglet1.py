import pyglet
from pyglet.gl import glClearColor
from pyglet import shapes

## window parameters
title = "Proba 1"
window = pyglet.window.Window(600, 600, title)
# background color
glClearColor(255, 255, 255, 1.0) # red, green, blue, and alpha(transparency)
batch = pyglet.graphics.Batch()

## rectangle lists
rectangles = []

## line lists
lines = []
line_x = []
line_y = []

@window.event
def on_mouse_press(x, y, button, modifiers):
    if button == pyglet.window.mouse.LEFT:
        ## creating a rectangle
        # rectangle width, height and color
        rect_width = 60
        rect_height = 30
        rect_color = (0, 0, 0) # black
        # rectangle coordinates
        co_x = x - rect_width/2
        co_y = y - rect_height/2
        # creating a rectangle object
        rect = shapes.Rectangle(co_x, co_y, rect_width, rect_height, color = rect_color, batch = batch)
        # opacity is visibility (0 = invisible, 255 means visible)
        rect.opacity = 255

        # saving the rectangle in the list
        rectangles.append(rect)

    elif button == pyglet.window.mouse.RIGHT:
        # saving coordinates that are clicked with the right mouse
        line_x.append(x)
        line_y.append(y)

        if len(line_x) >= 2 and len(line_y) >= 2:
            ## creating a line
            # line width and color
            line_width = 3
            line_color = (0, 0, 0) # black
            # line coordinates
            co_x1 = line_x[len(line_x)-2]
            co_y1 = line_y[len(line_y)-2]
            co_x2 = line_x[len(line_x)-1]
            co_y2 = line_y[len(line_y)-1]
            # creating a line object
            line = shapes.Line(co_x1, co_y1, co_x2, co_y2, line_width, color = line_color, batch = batch)
            # opacity is visibility (0 = invisible, 255 means visible)
            line.opacity = 255

            # saving the line in the list
            lines.append(line)
        else:
            pass

@window.event
def on_draw():
	window.clear()
	batch.draw()

pyglet.app.run()