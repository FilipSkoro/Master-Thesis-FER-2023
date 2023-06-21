import pygame
import tkinter as tk
from pygame.locals import *


#########################################  RAILS CLASS FUNCTIONS  ##############################################

pygame.init()

color_inactive = pygame.Color('grey50')
color_active = pygame.Color('dodgerblue2')
FONT = pygame.font.Font(None, 23)

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
        # parameters
        x_pp = prev_position[0]
        y_pp = prev_position[1]
        x_p = position[0]
        y_p = position[1]
        # distance and offset
        offset = 30
        distance = 1

        # calculate middle point
        mid_point = ((x_pp+x_p)//2, (y_pp+y_p)//2)
        result = 0

        # determine the angle of the line
        angle = pygame.math.Vector2(position[0] - prev_position[0], position[1] - prev_position[1]).angle_to((1, 0))

        # calculate result
        result = (int(mid_point[0] + distance * pygame.math.Vector2(1, 0).rotate(-angle)[0]) + offset,
                  int(mid_point[1] + distance * pygame.math.Vector2(1, 0).rotate(-angle)[1]) - offset)

        return result

    def handle_event(self, event, error):
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
                    self.write_message("ERROR: Wrong input or the maximum number of numbers has been entered!!\n", error)

                # Re-render the text
                self.text_surface = FONT.render(self.text, True, self.textbox_color)

    def write_message(self, text, error):

        if "ERROR" in text:
            # make error widget normal
            error.configure(state="normal")
            # make error text red
            error.configure(fg="red")
            # write error message
            error.insert(tk.END, text)
            # disable error widget
            error.configure(state="disabled")

        else:
            pass

    def draw(self):
        # rails coordinates
        start_pos = (self.prev_position[0], self.prev_position[1])
        end_pos = (self.position[0], self.position[1])
        # create rails
        line = pygame.draw.line(self.pygame_screen, self.color, start_pos, end_pos, self.width)
        # move line to its layer
        line_layer = 0
        line.move_ip(0, line_layer)

        # blit the text
        self.pygame_screen.blit(self.text_surface, (self.textbox_rect.x+5, self.textbox_rect.y+5))
        # blit the rect
        textbox_rect = pygame.draw.rect(self.pygame_screen, self.textbox_color, self.textbox_rect, 2)
        # move line textbox to its layer
        textbox_rect_layer = 1
        textbox_rect.move_ip(0, textbox_rect_layer)

################################################################################################################
