import pygame, math, os
from pygame.locals import *
import tkinter as tk
import Stop_class, Rails_class, Train_class


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
    root.geometry("800x650")
    root.title("Tkinter Window")

    return root

def create_windows(root):

    '''
    This function defines parameter values for button window and pygame window and then creates them.
    After that, the function embeds the mentioned windows into root window. At the end, pygame screen
    is initialized. It gets root window as an argument and it returns a list containing pygame window,
    button window, pygame screen and background color of pygame window.
    '''

    ## LEFT Button Window ##
    # button window 1 parameters
    btn_width_1 = 125
    btn_height_1 = 800
    # creating button window 1
    button_window_1 = tk.Frame(root, width = btn_width_1, height = btn_height_1)
    button_window_1.pack(side = tk.LEFT)

    ## TOP Button Window ##
    # button window 2 parameters
    btn_width_2 = 650
    btn_height_2 = 800
    # creating button window 2
    button_window_2 = tk.Frame(root, width = btn_width_2, height = btn_height_2)
    button_window_2.pack(side = tk.TOP)

    # pygame window parameters
    win_width = 700
    win_height = 700
    win_color = (255, 255, 255) # white

    '''
    # creating pygame window
    pygame_window = tk.Frame(root, width = win_width, height = win_height)
    pygame_window.pack(side = tk.BOTTOM)
    '''
    '''
    # embedding two windows
    os.environ['SDL_WINDOWID'] = str(pygame_window.winfo_id())
    os.environ['SDL_VIDEODRIVER'] = 'windib'
    # update is needed so everything is visible
    root.update()
    '''

    # pygame screen init
    pygame_screen = pygame.display.set_mode((win_width, win_height))
    pygame_screen.fill(win_color)
    pygame.display.set_caption("PyGame Window")

    return [button_window_1, button_window_2, pygame_screen, win_color]


###### BUTTON'S FUNCTIONS ######

# button's variables
enable_train = True
enable_stops = True
enable_lines = False
enable_nums = False
enable_start = False
clear_screen = False
clear_last = False

def start_btn_function():
    global enable_stops, enable_lines, enable_nums, enable_start

    enable_nums = False
    enable_lines = False
    enable_stops = False
    enable_start = True

def matrix_btn_function():
    return

def graph_btn_function():
    return

def new_route_btn_function():
    global enable_train

    # reset stops and rails coordinates
    rails_coordinates.clear()
    # enable creation of new train
    enable_train = True

def enable_stops_btn_function():
    global enable_stops, enable_lines, enable_nums, enable_start

    enable_nums = False
    enable_lines = False
    enable_stops = True
    enable_start = False

def enable_rails_btn_function():
    global enable_stops, enable_lines, enable_nums, enable_start

    enable_nums = False
    enable_lines = True
    enable_stops = False
    enable_start = False

def enable_nums_btn_function():
    global enable_stops, enable_lines, enable_nums, enable_start

    enable_nums = True
    enable_lines = False
    enable_stops = False
    enable_start = False

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

def create_buttons(button_window_1, button_window_2):

    ## LEFT Button Window ##
    # start button
    start_btn = tk.Button(button_window_1, text = "Start\nSimulation", height=3, width=12, command = start_btn_function)
    start_btn.place(x=25, y=175)
    # matrix button
    matrix_btn = tk.Button(button_window_1, text = "Get\nMatrices", height=3, width=12, command = matrix_btn_function)
    matrix_btn.place(x=25, y=250)
    # graph button
    graph_btn = tk.Button(button_window_1, text = "Get\nMax-Plus Graph", height=3, width=12, command = graph_btn_function)
    graph_btn.place(x=25, y=325)

    ## TOP Button Window ##
    # caption label
    caption = tk.Label(button_window_2, text = "Simple 2D Train Simulator", font=("Roman", 20, "bold"))
    caption.place(x=120, y=10)
    # new route button
    new_route_btn = tk.Button(button_window_2, text = "Create\nNew Route", height=3, width=12, command = new_route_btn_function)
    new_route_btn.place(x=20, y=60)
    # enable stop button
    enable_stops_btn = tk.Button(button_window_2, text = "Create\nStop", height=3, width=12, command = enable_stops_btn_function)
    enable_stops_btn.place(x=125, y=60)
    # enable rails button
    enable_rails_btn = tk.Button(button_window_2, text = "Create\nRails", height=3, width=12, command = enable_rails_btn_function)
    enable_rails_btn.place(x=230, y=60)
    # enable nums button
    enable_nums_btn = tk.Button(button_window_2, text = "Set\nTime Units", height=3, width=12, command = enable_nums_btn_function)
    enable_nums_btn.place(x=335, y=60)
    # clear screen button
    clear_btn = tk.Button(button_window_2, text = "Clear\nScreen", height=3, width=12, command = clear_btn_function)
    clear_btn.place(x=440, y=60)
    # clear last button
    clear_last_btn = tk.Button(button_window_2, text = "Clear\nLast", height=3, width=12, command = clear_last_btn_function)
    clear_last_btn.place(x=545, y=60)


###### MAIN PROGRAM'S FUNCTIONS ######

# stops and rails lists and variables
stops_coordinates = []
stops_list = []
rails_coordinates = []
rails_list = []
stops_and_rails = []
trains_list = []
stop_num = 1
color_num = 0
rail_offset_x = 1
rail_offset_y = 1
enable_sort = True

# clock
fps = 60
clock = pygame.time.Clock()

# train colors
COLOR = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (0, 255, 255), (255, 0, 255)]

def update_screen(pygame_screen, win_color):

    '''
    This function receives the variables pygame screen and its background color as arguments and updates
    the pygame screen using the displayed commands.
    '''

    pygame_screen.fill(win_color)
    #pygame.display.update()

def create_stops(pygame_screen, event, root, two_lane):
    global stop_num, color_num, enable_train

    # stop color, width and height
    stop_color = (0, 0, 0) # black
    stop_width = 60
    stop_height = 30
    # create stop object
    stop = Stop_class.Stop(pygame_screen, stop_color, stop_width, stop_height, event.pos, root, stop_num, two_lane)
    stop_num = stop_num + 1
    # put stop object in a list
    stops_list.append(stop)
    stops_and_rails.append(stop)

    # check if new route is being made
    if enable_train:
        # mark just created stop as beginner stop
        stop.beginner = True
        # create train object
        train = Train_class.Train(event.pos, pygame_screen, COLOR[color_num])
        color_num = color_num + 1
        color_num = 0 if color_num == len(COLOR) else color_num
        # put train in a list
        trains_list.append(train)
        # disable creation of a new train
        enable_train = False

    else:
        pass

    # put stop object in a train list
    train = trains_list[len(trains_list)-1]
    train.stops_and_rails.append(stop)

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
        # put rails object in a train list
        train = trains_list[len(trains_list)-1]
        train.stops_and_rails.append(rails)

    else:
        pass

def draw_rails():

    for rails in rails_list:
        rails.draw()

def draw_trains():

    for train in trains_list:
        train.draw()

def clear_screen_function():
    global clear_screen, clear_last, enable_lines, enable_nums, enable_start, enable_stops, enable_train, enable_sort
    global stop_num, color_num, rail_offset_x, rail_offset_y

    # delete all stops and rails
    stops_coordinates.clear()
    rails_coordinates.clear()
    stops_and_rails.clear()
    rails_list.clear()
    stops_list.clear()
    trains_list.clear()
    stop_num = 1
    color_num = 0
    rail_offset_x = 1
    rail_offset_y = 1

    # set variables back to default
    enable_train = True
    enable_stops = True
    enable_lines = False
    enable_nums = False
    enable_start = False
    clear_screen = False
    clear_last = False
    enable_sort = True

def clear_last_function():
    global clear_last, enable_train
    global stop_num, color_num

    last_object = 1

    try:
        # remove last drawn object
        last_object = stops_and_rails.pop()

    except IndexError:
        # catching IndexError
        print("ERROR: There's no stop or a track on display!")

    # remove last drawn object from it's list
    if last_object in stops_list:
        # check if last stop was beginner stop for some train
        if last_object.beginner == True:
            trains_list.pop()
            color_num = color_num - 1

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

    # remove last drawn object from trains list of stops and rails
    for train in trains_list:
        if last_object in train.stops_and_rails:
            train.stops_and_rails.pop()

    # set clear_last variable back to False
    clear_last = False

def handle_events(event):

    for stop in stops_list:
        stop.handle_event(event)

    for rails in rails_list:
        rails.handle_event(event)

def update_trains():

    for train in trains_list:
        # check if train has arrived at the stop, if yes make him wait then send him to next stop
        if train.position != train.stops[train.stop_cnt].position:
            # check if train has calculated path
            if train.path == None:
                train.path = train.calculate_path(train.stops[train.stop_cnt].position)
            # check if next stop is occupied
            if train.check_if_occupied(train.stops[train.stop_cnt]) == False:
                # update train position
                train.move_train()

        else:
            # make this stop occupied
            train.occupy(train.stops[train.stop_cnt])
            # make train wait for specified amount of time
            if train.wait_at_stop(train.stops[train.stop_cnt].text) == True:
                # unoccupy this stop
                train.unoccupy(train.stops[train.stop_cnt])
                # reset distance and path
                train.distance = 0
                train.path = None
                train.path_cnt = 0
                # set signal for next stop
                train.stop_cnt+=1
                # if train has arrived at the last stop send him to the first one
                if train.stop_cnt == len(train.stops):
                    train.stop_cnt = 0

def sort_lists(trains_list):

    for train in trains_list:
        train.sort_list()

def check_pos(position, stops_coordinates):
    radius = 40
    rez = None

    for cord in stops_coordinates:
        dif = math.sqrt((cord[0]-position[0])**2 + (cord[1]-position[1])**2)

        if dif <= radius:
            rez = cord
            break

        else:
            continue

    return rez

def check_stop(position, train_stops_list, stops_list):
    radius = 40

    for stop in stops_list:
        cord = (stop.x, stop.y)
        dif = math.sqrt((cord[0]-position[0])**2 + (cord[1]-position[1])**2)

        if dif <= radius:
            if stop in train_stops_list:
                return True

            else:
                return stop

        else:
            continue

def check_rails(rails_coordinates, train_rails_list, rails_list):
    radius = 40

    if len(rails_coordinates) >= 2:
        prev_pos = rails_coordinates[len(rails_coordinates)-2]
        pos = rails_coordinates[len(rails_coordinates)-1]

        for rails in rails_list:
            cord_prev = (rails.prev_position[0], rails.prev_position[1])
            cord = (rails.position[0], rails.position[1])
            dif1 = math.sqrt((cord_prev[0]-prev_pos[0])**2 + (cord_prev[1]-prev_pos[1])**2)
            dif2 = math.sqrt((cord_prev[0]-pos[0])**2 + (cord_prev[1]-pos[1])**2)
            dif3 = math.sqrt((cord[0]-prev_pos[0])**2 + (cord[1]-prev_pos[1])**2)
            dif4 = math.sqrt((cord[0]-pos[0])**2 + (cord[1]-pos[1])**2)

            if dif1 <= radius and dif2 <= radius:
                if rails not in train_rails_list:
                    return rails

            elif dif1 <= radius and dif3 <= radius:
                if rails not in train_rails_list:
                    return rails

            elif dif1 <= radius and dif4 <= radius:
                if rails not in train_rails_list:
                    return rails

            elif dif2 <= radius and dif3 <= radius:
                if rails not in train_rails_list:
                    return rails

            elif dif2 <= radius and dif4 <= radius:
                if rails not in train_rails_list:
                    return rails

            elif dif3 <= radius and dif4 <= radius:
                if rails not in train_rails_list:
                    return rails

            else:
                continue

        return False

    else:
        return False

def check_if_stop_exists(position, stops_list):
    radius = 40

    for stop in stops_list:
        cord = (stop.x, stop.y)
        dif = math.sqrt((cord[0]-position[0])**2 + (cord[1]-position[1])**2)

        if dif <= radius:
            return True

        else:
            continue

    return False


def main_program(pygame_screen, win_color, root):
    global rail_offset_x, rail_offset_y, enable_sort

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
            if enable_stops == True and enable_lines == False and enable_nums == False and enable_start == False:
                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if check_if_stop_exists(event.pos, stops_list) == False:
                            # saving coordinates on which LEFT mouse button clicked
                            stops_coordinates.append(event.pos)
                            # creating stop object
                            create_stops(pygame_screen, event, root, two_lane=False)

                        else:
                            print("ERROR: Stop already exists at this place!")

                    elif event.button == 3:
                        if check_if_stop_exists(event.pos, stops_list) == False:
                            # saving coordinates on which RIGHT mouse button clicked
                            stops_coordinates.append(event.pos)
                            # creating stop object
                            create_stops(pygame_screen, event, root, two_lane=True)

                        else:
                            print("ERROR: Stop already exists at this place!")

                    else:
                        pass

                else:
                    pass

            elif enable_stops == False and enable_lines == True and enable_nums == False and enable_start == False:
                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        # checking if stops are being connected
                        rez = check_pos(event.pos, stops_coordinates)

                        if rez != None:
                            # saving coordinates which are center of the nearest stop
                            if rez in rails_coordinates:
                                if rail_offset_y >= rail_offset_x:
                                    rez = (rez[0]-rail_offset_x, rez[1])
                                    rails_coordinates.append(rez)
                                    rail_offset_x = rail_offset_x + 1

                                else:
                                    rez = (rez[0]-rail_offset_y, rez[1])
                                    rails_coordinates.append(rez)
                                    rail_offset_y = rail_offset_y + 1

                            else:
                                rails_coordinates.append(rez)

                            # get last train object
                            train = trains_list[len(trains_list)-1]
                            # check if stop already exists
                            pos = check_stop(rez, train.stops_and_rails, stops_list)

                            if pos == True:
                                pass

                            else:
                                train.stops_and_rails.append(pos)

                            # check if stops are already connected
                            pruga = check_rails(rails_coordinates, train.stops_and_rails, rails_list)

                            if pruga != False:
                                train.stops_and_rails.append(pruga)
                            
                            elif pruga == False:
                                # creating rails object
                                create_rails(pygame_screen, rez, root)

                            else:
                                pass

                        else:
                            print("ERROR: Only stops can be connected with rails!")

                    else:
                        pass

                else:
                    pass

            elif enable_stops == False and enable_lines == False and enable_nums == True and enable_start == False:
                # handle events
                handle_events(event)

            else:
                pass

        # updating pygame screen
        update_screen(pygame_screen, win_color)

        # check if start is enabled
        if enable_start == True and enable_stops == False and enable_lines == False and enable_nums == False:
            # get trains lists ready
            if enable_sort == True:
                sort_lists(trains_list)
                enable_sort = False

            # try to update trains positions
            if len(trains_list) != 0:
                try:
                    # update trains positions
                    update_trains()

                except IndexError:
                    # catching IndexError
                    print("ERROR: Stops are not connected!!")

            else:
                print("ERROR: No stop or train has been created!!")

        else:
            pass

        # plotting stops, rails and trains
        draw_stops()
        draw_rails()
        draw_trains()

        try:
            # updating pygame and root window
            pygame.display.update()
            root.update()

        except tk.TclError:
            # catching _tkinter.TclError
            break

        # clock 60 fps
        clock.tick(fps)

###### MAIN FUNCTION ######

if __name__ == "__main__":

    '''
    This is the main function used to run the program, create class objects and call all relevant
    functions so that the simulator can run normally.
    '''

    # creating root window
    root = init_root_window()
    # creating pygame and button windows
    [button_window_1, button_window_2, pygame_screen, win_color] = create_windows(root)
    # creating buttons
    create_buttons(button_window_1, button_window_2)
    # starting main program
    main_program(pygame_screen, win_color, root)
