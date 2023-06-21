import tkinter as tk
import pygame
from pygame.locals import *


#############################################  WINDOW'S FUNCTIONS  #############################################

def init_root_window():

    '''
    This function creates a root window which is an object of the tkinter class and which will later contain
    pygame and a button window. It also initializes pygame. After the values of the dimension and the title
    of the root window are set, the function returns the root variable.
    '''

    # creating root window
    root = tk.Tk()
    # set size
    root.geometry("800x650")
    # set background color
    root.configure(bg="LightBlue")
    # set title
    root.title("Simple 2D Train Simulator 1.0.0")

    return root

def create_button_windows(root):

    '''
    This function defines parameter values for button window and pygame window and then creates them.
    After that, the function embeds the mentioned windows into root window. At the end, pygame screen
    is initialized. It gets root window as an argument and it returns a list containing pygame window,
    button window, pygame screen and background color of pygame window.
    '''

    ## START Button Window ##
    # start button window parameters
    btn_width_start = 650
    btn_height_start = 500
    # creating start button window
    start_button_window = tk.Frame(root, bg="LightBlue", width = btn_width_start, height = btn_height_start)
    start_button_window.pack(side=tk.TOP)

    ## BOTTOM Button Window ##
    # bottom button window parameters
    btn_width_btm = 650
    btn_height_btm = 50
    # creating bottom button window
    bottom_button_window = tk.Frame(root, bg="LightBlue", width = btn_width_btm, height = btn_height_btm)
    bottom_button_window.pack(side=tk.BOTTOM)

    ## LEFT Button Window ##
    # button window 1 parameters
    btn_width_1 = 125
    btn_height_1 = 800
    # creating button window 1
    button_window_1 = tk.Frame(root, bg="LightBlue", width = btn_width_1, height = btn_height_1)

    ## TOP Button Window ##
    # button window 2 parameters
    btn_width_2 = 650
    btn_height_2 = 800
    # creating button window 2
    button_window_2 = tk.Frame(root, bg="LightBlue", width = btn_width_2, height = btn_height_2)

    return [start_button_window,bottom_button_window, button_window_1, button_window_2]

def create_pygame_window():

    # pygame init
    pygame.init()

    ## Pygame Window ##
    # pygame window parameters
    win_width = 700
    win_height = 700
    win_color = (255, 255, 255) # white
    win_color = "lightblue"

    # creating pygame window
    pygame_screen = pygame.display.set_mode((win_width, win_height))
    pygame_screen.fill(win_color)
    pygame.display.set_caption("Simple 2D Train Simulator 1.0.0")

    return [pygame_screen, win_color]

################################################################################################################
