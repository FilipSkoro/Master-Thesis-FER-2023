import pygame
import tkinter as tk
from pygame.locals import *


##########################################  STOP CLASS FUNCTIONS  ##############################################

pygame.init()

color_inactive = pygame.Color('grey50')
color_active = pygame.Color('dodgerblue2')
FONT = pygame.font.Font(None, 23)

class Stop:
    def __init__(self, pygame_screen, stop_width, stop_height, position, root, i, two_lane):
        # stop parameters
        self.pygame_screen = pygame_screen
        self.width = stop_width
        self.height = stop_height
        self.color = (0, 0, 0) # black
        self.x = position[0]
        self.y = position[1]
        self.position = position
        self.root = root
        self.i = i
        self.two_lane = two_lane
        self.occupied_1 = False
        self.occupied_2 = False
        self.beginner = False

        # define stop image path
        img_path = "D:\FER_2023\Diplomski rad\Simple 2D Train Simulator - Original\Images\Custom Stop\Train_Stop.png"
        # create stop image and rectangle
        self.stop_image = pygame.image.load(img_path).convert_alpha()
        self.stop_rect = self.stop_image.get_rect(center=(self.position[0], self.position[1]))

        # text box parameters
        self.textbox_rect = pygame.Rect(self.position[0]-25/2.2, self.position[1]+20, 25, 22)
        self.textbox_color = color_inactive
        self.text = ""
        self.text_surface = FONT.render(self.text, True, self.textbox_color)
        self.active = False

        # label text font
        font = pygame.font.SysFont("Calibri", 13)
        # creating label text
        self.stop_name = "STOP_"+str(self.i)
        self.text2 = font.render(self.stop_name, True, self.color) if self.two_lane == False else font.render(self.stop_name+"_TL", True, self.color)
        # label text rectangle
        self.textRect = self.text2.get_rect()
        # label text rectangle center
        label_co_x = self.position[0]
        label_co_y = self.position[1]-self.height/1.2
        self.textRect.center = (label_co_x, label_co_y)

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
        # blit stop image
        self.pygame_screen.blit(self.stop_image, self.stop_rect)
        # blit label
        self.pygame_screen.blit(self.text2, self.textRect)
        # blit the text
        self.pygame_screen.blit(self.text_surface, (self.textbox_rect.x+5, self.textbox_rect.y+5))
        # draw textbox rect
        textbox_rect = pygame.draw.rect(self.pygame_screen, self.textbox_color, self.textbox_rect, 2)
        # move stop textbox to its layer
        textbox_rect_layer = 1
        textbox_rect.move_ip(0, textbox_rect_layer)

################################################################################################################
