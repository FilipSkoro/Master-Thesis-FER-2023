import pygame
import math
import tkinter as tk
from pygame.locals import *

pygame.init()

color_inactive = pygame.Color('lightskyblue3')
color_active = pygame.Color('dodgerblue2')
FONT = pygame.font.Font(None, 29)

class Rails:

    def __init__(self, pygame_screen, rails_color, rails_width, prev_position, position, root):
        # rails parameters
        self.pygame_screen = pygame_screen
        self.color = rails_color
        self.width = rails_width
        self.prev_position = prev_position
        self.position = position
        self.root = root

        # text box parameters - predefined
        self.textbox_pos = self.determine_textbox_position(self.prev_position, self.position)
        self.textbox_rect = pygame.Rect(self.textbox_pos[0], self.textbox_pos[1], 25, 22)
        self.textbox_color = color_inactive
        self.text = ""
        self.text_surface = FONT.render(self.text, True, self.textbox_color)
        self.active = False

    def determine_textbox_position(self, prev_position, position):
        x_pp = prev_position[0]
        y_pp = prev_position[1]
        x_p = position[0]
        y_p = position[1]
        offset = 45

        mid_point = ((x_pp+x_p)/2, (y_pp+y_p)/2)
        result = 0

        if y_p == y_pp:
            result = (mid_point[0], mid_point[1]-offset)

        elif x_p == x_pp:
            result = (mid_point[0]+offset, mid_point[1])

        elif x_pp > x_p and y_pp < y_p or x_pp < x_p and y_pp > y_p:
            result = (mid_point[0]-offset, mid_point[1])

        elif x_pp < x_p and y_pp < y_p or x_pp > x_p and y_pp > y_p:
            result = (mid_point[0]+offset, mid_point[1])

        return result

    def numbers_function(self, event):
        # check which key is pressed
        if event.keycode == 8:
            self.text = self.text[0:len(self.text)-1]

        elif event.keycode >= 48 and event.keycode <= 57:
            # check if user still can write numbers
            if len(self.text) < 2:
                self.text += str(event.char)

            else:
                print("ERROR: The maximum number of numbers has been entered!")

        else:
            print("ERROR: Wrong input!")

        # Re-render the text
        self.text_surface = FONT.render(self.text, True, self.textbox_color)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # check if the user clicked on the input_box rect
            if self.textbox_rect.collidepoint(event.pos):
                # toggle the active variable
                self.active = True

            else:
                self.active = False

        else:
            pass

        # check if active
        if self.active:
            # change the current color of the input box
            self.textbox_color = color_active

            try:
                # enable key listening
                self.root.bind("<KeyPress>", self.numbers_function)

            except tk.TclError:
                # catching _tkinter.TclError
                pass

            # refresh text box
            self.text_surface = FONT.render(self.text, True, self.textbox_color)

        else:
            # change the current color of the input box
            self.textbox_color = color_inactive

            try:
                # disable key listening
                self.root.unbind("<KeyPress>")

            except tk.TclError:
                # catching _tkinter.TclError
                pass

            # refresh text box
            self.text_surface = FONT.render(self.text, True, self.textbox_color)

    def update(self):
        # resize the box if the text is too long
        width = max(100, self.text_surface.get_width()+10)
        self.textbox_rect.w = width

    def rails_length(self, prev_position, position):

        return math.sqrt(math.pow(position[0] - prev_position[0], 2) + math.pow(position[1] - prev_position[1], 2))

    def draw(self):
        # rails coordinates
        start_pos = (self.prev_position[0], self.prev_position[1])
        end_pos = (self.position[0], self.position[1])
        # create rails
        pygame.draw.line(self.pygame_screen, self.color, start_pos, end_pos, self.width)

        # blit the text
        self.pygame_screen.blit(self.text_surface, (self.textbox_rect.x, self.textbox_rect.y))
        # blit the rect
        pygame.draw.rect(self.pygame_screen, self.textbox_color, self.textbox_rect, 2)