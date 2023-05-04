import pygame
import tkinter as tk
from pygame.locals import *

pygame.init()

color_inactive = pygame.Color('lightskyblue3')
color_active = pygame.Color('dodgerblue2')
FONT = pygame.font.Font(None, 23)

class Stop:
    def __init__(self, pygame_screen, stop_color, stop_width, stop_height, position, root, i, two_lane):
        # stop parameters
        self.pygame_screen = pygame_screen
        self.width = stop_width
        self.height = stop_height
        self.color = stop_color
        self.x = position[0]
        self.y = position[1]
        self.position = position
        self.root = root
        self.i = i
        self.two_lane = two_lane
        self.occupied_1 = False
        self.occupied_2 = False
        self.beginner = False
        self.rectangle = None

        # text box parameters - predefined
        self.textbox_rect = pygame.Rect(self.position[0]-25/2.2, self.position[1]+20, 25, 22)
        self.textbox_color = color_inactive
        self.text = ""
        self.text_surface = FONT.render(self.text, True, self.textbox_color)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # if the user clicked on the input_box rect
            if self.textbox_rect.collidepoint(event.pos):
                # toggle the active variable.
                self.active = True

            else:
                self.active = False

            # change the current color of the input box
            if self.active:
                self.textbox_color = color_active
                self.text_surface = FONT.render(self.text, True, self.textbox_color)

            else:
                self.textbox_color = color_inactive
                self.text_surface = FONT.render(self.text, True, self.textbox_color)

        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print(self.text)

                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]

                elif event.key >= K_0 and event.key <= K_9 and len(self.text) < 2:
                    self.text += event.unicode

                else:
                    print("ERROR: Wrong input or the maximum number of numbers has been entered!")

                # Re-render the text
                self.text_surface = FONT.render(self.text, True, self.textbox_color)

    def update(self):
        # resize the box if the text is too long
        width = max(100, self.text_surface.get_width()+10)
        self.textbox_rect.w = width

    def draw(self):
        # rectangle coordinates
        co_x = self.position[0]-self.width/2
        co_y = self.position[1]-self.height/2
        # create rectangle
        self.rectangle = pygame.Rect((co_x, co_y), (self.width, self.height))
        pygame.draw.rect(self.pygame_screen, self.color, self.rectangle)

        # label text font
        font = pygame.font.SysFont("Calibri", 13)
        # creating label text
        text = font.render("Stanica "+str(self.i), True, self.color)
        # label text rectangle
        textRect = text.get_rect()
        # label text rectangle center
        label_co_x = self.position[0]
        label_co_y = self.position[1]-self.height/1.2
        textRect.center = (label_co_x, label_co_y)
        # create label
        self.pygame_screen.blit(text, textRect)

        # blit the text
        self.pygame_screen.blit(self.text_surface, (self.textbox_rect.x+5, self.textbox_rect.y+5))
        # blit the rect
        textbox_rect = pygame.draw.rect(self.pygame_screen, self.textbox_color, self.textbox_rect, 2)
        # move stop textbox to its layer
        textbox_rect_layer = 1
        textbox_rect.move_ip(0, textbox_rect_layer)