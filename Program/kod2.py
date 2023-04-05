import pygame, os
from pygame.locals import *
import tkinter as tk
import Stop_class, Rails_class

###### WINDOW'S FUNCTIONS ######

def init_root_window():

    '''
    This function creates a root window which is an object of the tkinter class and which will later contain
    pygame and a button window. It also initializes pygame. After the values of the dimension and the title
    of the root window are set, the function returns the root variable.
    '''

    # pygame init
    pygame.init()

    # creating root window
    root = tk.Tk()
    root.geometry("750x650")
    root.title("Spawn stanice")

    return root

def create_windows(root):

    '''
    This function defines parameter values for button window and pygame window and then creates them.
    After that, the function embeds the mentioned windows into root window. At the end, pygame screen
    is initialized. It gets root window as an argument and it returns a list containing pygame window,
    button window, pygame screen and background color of pygame window.
    '''

    # button window parameters
    btn_width = 600
    btn_height = 50
    #btn_color =
    # creating button window
    button_window = tk.Frame(root, width = btn_width, height = btn_height)
    button_window.pack(side = tk.TOP)

    # pygame window parameters
    win_width = 600
    win_height = 600
    win_color = (255, 255, 255) # white
    # creating pygame window
    pygame_window = tk.Frame(root, width = win_width, height = win_height)
    pygame_window.pack(side = tk.BOTTOM)

    # embedding two windows
    os.environ['SDL_WINDOWID'] = str(pygame_window.winfo_id())
    os.environ['SDL_VIDEODRIVER'] = 'windib'
    # update is needed so everything is visible
    root.update()

    # pygame screen init
    pygame_screen = pygame.display.set_mode((win_width, win_height))
    pygame_screen.fill(win_color)

    return [pygame_window, button_window, pygame_screen, win_color]


###### BUTTON'S FUNCTIONS ######

# button's variables
enable_stops = True
enable_lines = False
enable_nums = False
clear_screen = False
clear_last = False

def enable_stops_btn_function():
    global enable_stops
    global enable_lines
    global enable_nums

    enable_nums = False
    enable_lines = False
    enable_stops = True

def enable_rails_btn_function():
    global enable_lines
    global enable_stops
    global enable_nums

    enable_nums = False
    enable_stops = False
    enable_lines = True

def enable_nums_btn_function():
    global enable_lines
    global enable_stops
    global enable_nums

    enable_stops = False
    enable_lines = False
    enable_nums = True

def clear_btn_function():

    '''
    This is a command function for the clear button that sets the value of the clear_screen variable
    to True and thus allows the user to clear all the display on the screen at the click of the button.
    '''

    global clear_screen

    clear_screen = True

def clear_last_btn_function():

    '''
    This is a command function for the clear last button that sets the value of the clear_last variable
    to True and thus allows the user to clear last shape drawn on the screen at the click of the button.
    '''

    global clear_last

    clear_last = True

def create_buttons(button_window):
 
    '''
    This function is used to create the necessary buttons. It receives a button window as an argument.
    The function defines the parameters of all buttons, creates them and places them on the button window.
    '''

    enable_stops_btn = tk.Button(button_window, text = "Stops",  command = enable_stops_btn_function)
    enable_stops_btn.pack(side=tk.LEFT)
    enable_rails_btn = tk.Button(button_window, text = "Rails",  command = enable_rails_btn_function)
    enable_rails_btn.pack(side=tk.LEFT)
    enable_nums_btn = tk.Button(button_window, text = "Nums",  command = enable_nums_btn_function)
    enable_nums_btn.pack(side=tk.LEFT)
    clear_btn = tk.Button(button_window, text = "Clear screen", command = clear_btn_function)
    clear_btn.pack(side=tk.RIGHT)
    clear_last_btn = tk.Button(button_window, text = "Clear last", command = clear_last_btn_function)
    clear_last_btn.pack(side=tk.RIGHT)


###### MAIN PROGRAM'S FUNCTIONS ######

# stops and rails lists and variables
stops_coordinates = []
stops_list = []
rails_coordinates = []
rails_list = []
stops_and_rails = []
stop_num = 1

def update_screen(pygame_screen, win_color):

    '''
    This function receives the variables pygame screen and its background color as arguments and updates
    the pygame screen using the displayed commands.
    '''

    pygame_screen.fill(win_color)
    pygame.display.update()

def create_stops(pygame_screen, position, root):
    global stop_num

    # stop color, width and height
    stop_color = (0, 0, 0) # black
    stop_width = 60
    stop_height = 30
    # create stop object
    stop = Stop_class.Stop(pygame_screen, stop_color, stop_width, stop_height, position, root, stop_num)
    stop_num = stop_num + 1
    # put stop object in a list
    stops_list.append(stop)
    stops_and_rails.append(stop)

def draw_stops():

    for stop in stops_list:
        stop.draw()

def create_rails(pygame_screen, position, root):

    if len(rails_coordinates) >= 2:
        # rails color and width
        rails_color = (0, 0, 0) # black
        rails_width = 3
        # determine next position
        prev_position = rails_coordinates[rails_coordinates.index(position)-1]
        # create rails object
        rails = Rails_class.Rails(pygame_screen, rails_color, rails_width, prev_position, position, root)
        # put rails object in a list
        rails_list.append(rails)
        stops_and_rails.append(rails)

    else:
        pass

def draw_rails():

    for rails in rails_list:
        rails.draw()

def clear_screen_function():
    global clear_screen
    global stop_num

    # delete all stops and rails
    stops_coordinates.clear()
    rails_coordinates.clear()
    stops_and_rails.clear()
    rails_list.clear()
    stops_list.clear()
    stop_num = 1
    # set clear_screen variable back to False
    clear_screen = False

def clear_last_function():
    global clear_last
    global stop_num

    last_object = 1

    try:
        # remove last drawn object
        last_object = stops_and_rails.pop()

    except IndexError:
        # catching IndexError
        print("ERROR: There's no stop or a track on display!")

    # remove last drawn object from it's list
    if last_object in stops_list:
        stops_list.remove(last_object)
        stops_coordinates.pop()
        stop_num = stop_num-1

    elif last_object in rails_list:
        # check if only two rails are left
        if len(rails_list) == 1:
            rails_coordinates.clear()
            rails_list.clear()

        else:
            rails_list.remove(last_object)
            rails_coordinates.pop()

    else:
        pass

    # set clear_last variable back to False
    clear_last = False

def handle_events(event):

    for stop in stops_list:
        stop.handle_event(event)

    for rails in rails_list:
        rails.handle_event(event)

def main_program(pygame_screen, win_color, root):

    run = True

    while run:

        if clear_screen == True:
            # clear screen
            clear_screen_function()
            # update screen
            update_screen(pygame_screen, win_color)

        else:
            pass

        if clear_last == True:
            # clear last object
            clear_last_function()
            # update screen
            update_screen(pygame_screen, win_color)

        else:
            pass

        for event in pygame.event.get():
            # iterating over all the events received from pygame.event.get()
            if event.type == pygame.QUIT:
                run = False

            # checking what is enabled
            if enable_stops == True and enable_lines == False and enable_nums == False:
                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        # saving coordinates on which LEFT mouse button clicked
                        stops_coordinates.append(event.pos)
                        # creating stop object
                        create_stops(pygame_screen, event.pos, root)

                    else:
                        pass

                else:
                    pass

            elif enable_stops == False and enable_lines == True and enable_nums == False:
                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        # saving coordinates on which LEFT mouse button clicked
                        rails_coordinates.append(event.pos)
                        # creating rails object
                        create_rails(pygame_screen, event.pos, root)

                    else:
                        pass

                else:
                    pass

            elif enable_stops == False and enable_lines == False and enable_nums == True:
                # handle events
                handle_events(event)

            else:
                pass

            if not event.type == MOUSEMOTION and not event.type == MOUSEBUTTONDOWN and not event.type == MOUSEWHEEL:
                # updating pygame window
                update_screen(pygame_screen, win_color)

            else:
                pass

        # plotting stops and rails
        draw_stops()
        draw_rails()

        try:
            # updating pygame and root window
            pygame.display.update()
            root.update()

        except tk.TclError:
            # catching _tkinter.TclError
            break


###### MAIN FUNCTION ######

if __name__ == "__main__":

    '''
    This is the main function used to run the program, create class objects and call all relevant
    functions so that the simulator can run normally.
    '''

    # creating root window
    root = init_root_window()
    # creating pygame and button window
    [pygame_window, button_window, pygame_screen, win_color] = create_windows(root)
    # creating all buttons
    create_buttons(button_window)
    # starting main program
    main_program(pygame_screen, win_color, root)
