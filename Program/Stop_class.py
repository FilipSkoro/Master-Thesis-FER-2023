import pygame
import tkinter as tk
from pygame.locals import *

pygame.init()

color_inactive = pygame.Color('lightskyblue3')
color_active = pygame.Color('dodgerblue2')
FONT = pygame.font.Font(None, 29)

class Stop:

    def __init__(self, pygame_screen, stop_color, stop_width, stop_height, position, root, i):
        # stop parameters
        self.pygame_screen = pygame_screen
        self.width = stop_width
        self.height = stop_height
        self.color = stop_color
        self.x = position[0]
        self.y = position[1]
        self.root = root
        self.i = i

        # text box parameters - predefined
        self.textbox_rect = pygame.Rect(self.x-25/2.2, self.y+20, 25, 22)
        self.textbox_color = color_inactive
        self.text = ""
        self.text_surface = FONT.render(self.text, True, self.textbox_color)
        self.active = False

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

    def draw(self):
        # rectangle coordinates
        co_x = self.x-self.width/2
        co_y = self.y-self.height/2
        # create rectangle
        pygame.draw.rect(self.pygame_screen, self.color, pygame.Rect((co_x, co_y), (self.width, self.height)))

        # label text font
        font = pygame.font.SysFont("Calibri", 13)
        # creating label text
        text = font.render("Stanica "+str(self.i), True, self.color)
        # label text rectangle
        textRect = text.get_rect()
        # label text rectangle center
        label_co_x = self.x
        label_co_y = self.y-self.height/1.2
        textRect.center = (label_co_x, label_co_y)
        # create label
        self.pygame_screen.blit(text, textRect)

        # blit the text
        self.pygame_screen.blit(self.text_surface, (self.textbox_rect.x, self.textbox_rect.y))
        # blit the rect
        pygame.draw.rect(self.pygame_screen, self.textbox_color, self.textbox_rect, 2)
