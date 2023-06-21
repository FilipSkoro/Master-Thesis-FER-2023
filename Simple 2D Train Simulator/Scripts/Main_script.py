import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame, math
from pygame.locals import *
from tkinter import font, ttk
import tkinter as tk
import Stop_class, Rails_class, Train_class
from Matrices_functions import *
from Windows_functions import *
from MaxPlus_functions import *


#############################################  BUTTON'S FUNCTIONS  #############################################

# button's variables
enable_train = True
enable_stops = True
enable_lines = False
enable_nums = False
enable_start = False
clear_screen = False
clear_last = False
start_btn = False
exit_btn = False

# text, error and scale widgets
text = None
error = None
scale = None
fs_write = True
max_plus_write = True

def start_btn_function():
    global start_btn

    start_btn = True

def exit_btn_function():
    global exit_btn

    exit_btn = True

def start_sim_btn_function():
    global enable_stops, enable_lines, enable_nums, enable_start

    enable_nums = False
    enable_lines = False
    enable_stops = False
    enable_start = True

def fs_matrix_btn_function():
    global text, fs_write

    if enable_start == True and fs_write == True:
        # get dictionary
        data = get_Trains_Dictionary(trains_list)
        # get segments between stops
        segments = get_Segments(data, [*data])
        # get trains on segments
        trains_on_segments = get_Trains_On_Segments(data, [*data])

        # get matrix F
        [F, Fu, Fv, Fr, Fy] = get_Matrix_F(data, [*data], segments, trains_on_segments)
        # get matrix S
        [S, Su, Sv, Sr, Sy] = get_Matrix_S(data, [*data], segments, trains_on_segments)
        # get matrix W
        W = get_Matrix_W(F, S)

        # make text widget normal
        text.configure(state="normal")

        ###  Matrix F  ###
        # write caption F
        text.insert(tk.END, "===================================\n")
        text.insert(tk.END, "             Matrix F")
        text.insert(tk.END, "\n===================================\n")
        text.insert(tk.END, "\n")

        # print Fu
        text.insert(tk.END, "Fu = \n")
        print_matrix(Fu)

        # print Fv
        text.insert(tk.END, "Fv = \n")
        print_matrix(Fv)

        # print Fr
        text.insert(tk.END, "Fr = \n")
        print_matrix(Fr)

        # print Fy
        text.insert(tk.END, "Fy = \n")
        print_matrix(Fy)

        # print matrix F
        text.insert(tk.END, "F = [Fu Fv Fr Fy] = \n")
        print_matrix(F)

        ###  Matrix S  ###
        # write caption F
        text.insert(tk.END, "===================================\n")
        text.insert(tk.END, "             Matrix S")
        text.insert(tk.END, "\n===================================\n")
        text.insert(tk.END, "\n")

        # print Su
        text.insert(tk.END, "Su = \n")
        print_matrix(Su)

        # print Sv
        text.insert(tk.END, "Sv = \n")
        print_matrix(Sv)

        # print Sr
        text.insert(tk.END, "Sr = \n")
        print_matrix(Sr)

        # print Sy
        text.insert(tk.END, "Sy = \n")
        print_matrix(Sy)

        # print matrix S
        text.insert(tk.END, "S = [Su; Sv; Sr; Sy] = \n")
        print_matrix(S)

        ###  Matrix W  ###
        # write caption F
        text.insert(tk.END, "===================================\n")
        text.insert(tk.END, "             Matrix W")
        text.insert(tk.END, "\n===================================\n")
        text.insert(tk.END, "\n")

        # print matrix W
        text.insert(tk.END, "W = \n")
        print_matrix(W)

        # make text widget read-only
        text.configure(state="disabled")

        # disable fs_write
        fs_write = False

    elif enable_start == True and fs_write == False:
        # write warning message
        write_message("WARNING: F and S matrices already calculated!!\n")

    else:
        # write error message
        write_message("ERROR: Cannot calculate matrices - simulation has not begun yet!!\n")

def graph_btn_function():
    global text, max_plus_write

    if enable_start == True and max_plus_write == True:

        # get weights and squares
        [weights, squares] = get_weights(state_dict, trains_list)

        # make text widget normal
        text.configure(state="normal")

        # get graph and print equations and matrices
        draw_max_plus_graph(weights, text, squares)

        # make text widget read-only
        text.configure(state="disabled")

        # disable max_plus_write
        max_plus_write = False

    elif enable_start == True and max_plus_write == False:
        # write warning message
        write_message("WARNING: Max-Plus graph and equations already created!!\n")

    else:
        # write error message
        write_message("ERROR: Cannot make Max-Plus graph - simulation has not begun yet!!\n")

def new_route_btn_function():
    global enable_train, enable_stops, enable_lines, enable_nums

    if enable_start == False:
        if color_num < len(COLOR):
            # sort train lists and write routes
            sort_lists(trains_list)
            write_routes()

            # reset stops and rails coordinates
            rails_coordinates.clear()
            # enable creation of new train
            enable_train = True
            enable_stops = True
            enable_nums = False
            enable_lines = False

        else:
            # sort train lists and write routes
            sort_lists(trains_list)
            write_routes()
            # write error message
            write_message("ERROR: Maximum number of trains have been created!!\n")

    else:
        # write error message
        write_message("ERROR: Cannot add new elements to scheme after simulation has begun!!\n")

def enable_stops_btn_function():
    global enable_stops, enable_lines, enable_nums

    if enable_start == False:
        enable_nums = False
        enable_lines = False
        enable_stops = True

    else:
        # write error message
        write_message("ERROR: Cannot add new elements to scheme after simulation has begun!!\n")

def enable_rails_btn_function():
    global enable_stops, enable_lines, enable_nums

    if enable_start == False:
        enable_nums = False
        enable_lines = True
        enable_stops = False

    else:
        # write error message
        write_message("ERROR: Cannot add new elements to scheme after simulation has begun!!\n")

def enable_nums_btn_function():
    global enable_stops, enable_lines, enable_nums, enable_start

    if enable_start == False:
        enable_nums = True
        enable_lines = False
        enable_stops = False

    else:
        # write error message
        write_message("ERROR: Cannot change time units after simulation has begun!!\n")

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

    if enable_start == False:
        clear_last = True

    else:
        # write error message
        write_message("ERROR: Cannot delete elements from scheme after simulation has begun!!\n")

def scaler_function():
    global fps

    fpss = fps.get()

def create_start_buttons(start_button_window, bottom_button_window):

    # set button font
    btn_font = font.Font(family="Arial", size=13, weight="bold")

    ## START Button Window ##
    # start caption label
    start_caption = tk.Label(start_button_window, bg="LightBlue", text = "WELCOME\nTO SIMPLE\n2D TRAIN SIMULATOR", font=("Roman", 40, "bold"))
    start_caption.place(x=100, y=10)
    # start button
    start_btn = tk.Button(start_button_window, fg="White", bg="DarkBlue", text = "START\nSIMULATOR", font=btn_font, height=4, width=18, command = start_btn_function)
    start_btn.place(x=230, y=250)
    # exit button
    exit_btn = tk.Button(start_button_window, fg="White", bg="DarkBlue", text = "EXIT\nSIMULATOR", font=btn_font, height=4, width=18, command = exit_btn_function)
    exit_btn.place(x=230, y=375)
    # bottom caption label
    bottom_caption = tk.Label(bottom_button_window, bg="LightBlue", text = "Simple 2D Train Simulator 1.0.0", font=("Arial", 10))
    bottom_caption.pack()

def create_simulator_buttons(button_window_1, button_window_2):
    global text, error, scale
    global fps

    # set button font
    btn_font = font.Font(family="Arial", size=9, weight="bold")

    ## LEFT Button Window ##
    # start simulation button
    start_sim_btn = tk.Button(button_window_1, fg="White", bg="DarkBlue", text = "Start\nSimulation", font=btn_font, height=3, width=12, command = start_sim_btn_function)
    start_sim_btn.place(x=25, y=200)
    # F and S matrix button
    fs_matrix_btn = tk.Button(button_window_1, fg="White", bg="DarkBlue", text = "Get\nF and S\nMatrices", font=btn_font, height=3, width=12, command = fs_matrix_btn_function)
    fs_matrix_btn.place(x=25, y=275)
    # graph button
    graph_btn = tk.Button(button_window_1, fg="White", bg="DarkBlue", text = "Get\nMax-Plus\nGraph", font=btn_font, height=3, width=12, command = graph_btn_function)
    graph_btn.place(x=25, y=350)
    # scale widget
    scale = tk.Scale(button_window_1, variable=fps, font=btn_font, bg="DarkBlue", fg="White", orient="horizontal", label="     Adjust fps", from_=30, to=180, command=scaler_function()) 
    scale.place(x=20, y=425)

    ## TOP Button Window ##
    # caption label
    caption = tk.Label(button_window_2, bg="LightBlue", text = "Simple 2D Train Simulator", font=("Roman", 23, "bold"))
    caption.place(x=100, y=10)
    # new route button
    new_route_btn = tk.Button(button_window_2, fg="White", bg="DarkBlue", text = "Create\nNew Route", font=btn_font, height=3, width=12, command = new_route_btn_function)
    new_route_btn.place(x=20, y=60)
    # enable stop button
    enable_stops_btn = tk.Button(button_window_2, fg="White", bg="DarkBlue", text = "Create\nStop", font=btn_font, height=3, width=12, command = enable_stops_btn_function)
    enable_stops_btn.place(x=125, y=60)
    # enable rails button
    enable_rails_btn = tk.Button(button_window_2, fg="White", bg="DarkBlue", text = "Create\nRails", font=btn_font, height=3, width=12, command = enable_rails_btn_function)
    enable_rails_btn.place(x=230, y=60)
    # enable nums button
    enable_nums_btn = tk.Button(button_window_2, fg="White", bg="DarkBlue", text = "Set\nTime Units", font=btn_font, height=3, width=12, command = enable_nums_btn_function)
    enable_nums_btn.place(x=335, y=60)
    # clear last button
    clear_last_btn = tk.Button(button_window_2, fg="White", bg="DarkBlue", text = "Clear\nLast", font=btn_font, height=3, width=12, command = clear_last_btn_function)
    clear_last_btn.place(x=440, y=60)
    # clear screen button
    clear_btn = tk.Button(button_window_2, fg="White", bg="DarkBlue", text = "Clear\nScreen", font=btn_font, height=3, width=12, command = clear_btn_function)
    clear_btn.place(x=545, y=60)

    # determine scrollbars style
    style=ttk.Style()
    style.theme_use('classic')
    # determine scrollbars color
    style.configure("Vertical.TScrollbar", background="DarkBlue", arrowcolor="LightBlue")
    style.configure("Horizontal.TScrollbar", background="DarkBlue", arrowcolor="LightBlue")

    # text widget
    text = tk.Text(button_window_2, height=20, width=70, wrap="none")
    text.place(x=50, y=150)
    text.tag_add("start", "end")
    text.tag_config("start", background="black", foreground="red")
    # make text widget read-only
    text.configure(state="disabled")
    # create a right scrollbar widget and set its command to the text widget
    scrollbar_vertical_1 = ttk.Scrollbar(button_window_2, orient="vertical", command=text.yview)
    scrollbar_vertical_1.place(x=613, y=150, height=324)
    # communicate back to the right scrollbar
    text["yscrollcommand"] = scrollbar_vertical_1.set
    # create a bottom scrollbar widget and set its command to the text widget
    scrollbar_horizontal = ttk.Scrollbar(button_window_2, orient="horizontal", command=text.xview)
    scrollbar_horizontal.place(x=51, y=474, width=563)
    # communicate back to the bottom scrollbar
    text["xscrollcommand"] = scrollbar_horizontal.set

    # error widget
    error = tk.Text(button_window_2, height=6, width=70, wrap="none")
    error.place(x=50, y=510)
    # make error widget read-only
    error.configure(state="disabled")
    # create a right scrollbar for error widget and set its command to the error widget
    scrollbar_error = ttk.Scrollbar(button_window_2, orient="vertical", command=error.yview)
    scrollbar_error.place(x=613, y=510, height=100)
    # communicate back to the right error scrollbar
    error["yscrollcommand"] = scrollbar_error.set

def print_matrix(matrix):

    text.insert(tk.END, "\n")
    for i in range(len(matrix)):
        text.insert(tk.END, "    ")
        text.insert(tk.END, matrix[i])
        text.insert(tk.END, "\n")

    text.insert(tk.END, "\n")

################################################################################################################


##########################################  MAIN PROGRAM'S FUNCTIONS  ##########################################

# stops and rails lists and variables
stops_coordinates = []
stops_list = []
rails_coordinates = []
rails_list = []
stops_and_rails = []
trains_list = []
state_dict = {}
stop_num = 1
color_num = 0
rail_offset_x = 1
rail_offset_y = 1
msg_color = 1
enable_sort = True

# clock
clock = pygame.time.Clock()

# train colors
COLOR = ['Red', 'Green', 'Blue', 'Gold', 'Cyan', 'Orange', 'Purple', 'Gray', 'Violet', 'Yellow']

def update_screen(pygame_screen, win_color):

    '''
    This function receives the variables pygame screen and its background color as arguments and updates
    the pygame screen using the displayed commands.
    '''

    pygame_screen.fill(win_color)

def create_stops(pygame_screen, position, root, check, two_lane):
    global stop_num, color_num, enable_train

    if check == False:
        # stop width and height
        stop_width = 60
        stop_height = 30
        # create stop object
        stop = Stop_class.Stop(pygame_screen, stop_width, stop_height, position, root, stop_num, two_lane)
        stop_num = stop_num + 1
        # put stop object in a list
        stops_list.append(stop)
        stops_and_rails.append(stop)

    # check if new route is being made
    if enable_train:
        if check == False:
            # mark just created stop as beginner stop
            stop.beginner = True
            # create train object
            train = Train_class.Train(position, pygame_screen, COLOR[color_num], color_num+1)
            color_num = color_num + 1
            ##color_num = 0 if color_num == len(COLOR) else color_num
            # put train in a list
            trains_list.append(train)
            # disable creation of a new train
            enable_train = False

        else:
            # check if no train is already having this stop as beginner stop
            if check.beginner == False:
                # mark stop that already exists as beginner stop
                check.beginner = True
                # create train object
                train = Train_class.Train(position, pygame_screen, COLOR[color_num], color_num+1)
                color_num = color_num + 1
                ##color_num = 0 if color_num == len(COLOR) else color_num
                # put train in a list
                trains_list.append(train)
                # disable creation of a new train
                enable_train = False

            else:
                # write error message
                write_message("ERROR: Other train is already starting it's route from this stop!!\n")

    else:
        pass

    train = trains_list[len(trains_list)-1]
    # put stop object in a train list
    if check == False:
        train.stops_and_rails.append(stop)
    else:
        train.stops_and_rails.append(check)

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
    global fs_write, max_plus_write, msg_color

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

    # delete text from widgets
    text.configure(state="normal")
    text.delete("1.0", "end")
    text.configure(state="disabled")
    error.configure(state="normal")
    error.delete("1.0", "end")
    error.configure(state="disabled")

    # enable scale widget
    scale.configure(state="normal")

    # set variables back to default
    enable_train = True
    enable_stops = True
    enable_lines = False
    enable_nums = False
    enable_start = False
    clear_screen = False
    clear_last = False
    enable_sort = True
    fs_write = True
    max_plus_write = True
    msg_color = 1

def clear_last_function():
    global clear_last, enable_train
    global stop_num, color_num

    last_object = 1

    try:
        # remove last drawn object
        last_object = stops_and_rails.pop()

    except IndexError:
        # catching IndexError
        write_message("ERROR: There's no stop or a track on display!!\n")

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
        stop.handle_event(event, error)

    for rails in rails_list:
        rails.handle_event(event, error)

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
                # check if collision has happend
                check_if_collision(train)

        else:
            # make this stop occupied
            train.occupy(train.stops[train.stop_cnt])
            # check if stop has two lanes
            if train.stops[train.stop_cnt].two_lane == False:
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

            else:
                # recognize two lane stop
                train.at_two_lane = True
                # check if other train has arrived
                for train2 in trains_list:
                    if train2 != train:
                        if train2.at_two_lane == True:
                            if train.position == train2.position:
                                if train.started_time_cnt == False:
                                    train.started_time_cnt = True

                if train.started_time_cnt == True:
                    # make train wait for specified amount of time
                    if train.wait_at_stop(train.stops[train.stop_cnt].text) == True:
                        # unoccupy this stop
                        train.unoccupy(train.stops[train.stop_cnt])
                        # reset distance and path
                        train.distance = 0
                        train.path = None
                        train.path_cnt = 0
                        train.at_two_lane = False
                        train.started_time_cnt = False
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
    radius = 100

    for stop in stops_list:
        cord = (stop.x, stop.y)
        dif = math.sqrt((cord[0]-position[0])**2 + (cord[1]-position[1])**2)

        if dif <= radius:
            return stop

        else:
            continue

    return False

def check_if_rails_are_too_close(position, rails_coordinates):

    if len(rails_coordinates) != 0:
        last_cord = rails_coordinates[len(rails_coordinates)-1] 

        if math.dist(position, last_cord) <= 5:
            return True
        else:
            return False
    else:
        return False

def check_if_collision(train):
    global enable_start

    for other_train in trains_list:
        if train != other_train:
            if other_train.position not in stops_coordinates:
                if train.position == other_train.position:
                    # stop simulation
                    enable_start = False
                    # write message
                    write_message("FATAL ERROR: COLLISION HAS HAPPENED!!\n")
                    write_message("ERROR: Program has crashed!!\n")

        else:
            continue

def get_states(trains_list):
    global state_dict

    # clear dictionary
    state_dict.clear()
    # define strting state number
    state_num = 1

    for train in trains_list:
        for stop in train.stops:
            # define first state for stop
            state = "x"+str(state_num)
            state_dict[state] = train.train_name+" is waiting at "+stop.stop_name
            # define second state for stop
            state = "x"+str(state_num+1)
            state_dict[state] = train.train_name+" leaves "+stop.stop_name
            # update state number
            state_num+=2

def write_message(text):
    global error, msg_color

    if "ERROR" in text:
        # make error widget normal
        error.configure(state="normal")

        # write error message
        error.insert(tk.INSERT, text)

        # create tag
        tag = "tag_"+str(msg_color)
        # highlight text
        error.tag_add(tag, str(msg_color)+".0", str(msg_color)+".100")
        error.tag_config(tag, background="white", foreground='Red')

        # disable error widget
        error.configure(state="disabled")
        # add 1 to msg color
        msg_color+=1

    elif "WARNING" in text:
        # make error widget normal
        error.configure(state="normal")

        # write error message
        error.insert(tk.INSERT, text)

        # create tag
        tag = "tag_"+str(msg_color)
        # highlight text
        error.tag_add(tag, str(msg_color)+".0", str(msg_color)+".100")
        error.tag_config(tag, background="white", foreground='Orange')

        # disable error widget
        error.configure(state="disabled")
        # add 1 to msg color
        msg_color+=1

    else:
        pass

def write_routes():
    global text, trains_list

    # make text widget normal
    text.configure(state="normal")
    # clear text widget
    text.delete("1.0", "end")

    text.insert(tk.INSERT, "===================================\n")
    text.insert(tk.INSERT, "           TRAIN ROUTES\n")
    text.insert(tk.INSERT, "===================================\n")

    # row index
    row = 4

    for train in trains_list:
        text.insert(tk.INSERT, train.train_name)
        text.insert(tk.INSERT, ": ")

        for stop in train.stops:    
            text.insert(tk.INSERT, stop.stop_name)
            text.insert(tk.INSERT, " -> ")

        text.insert(tk.INSERT, train.stops[0].stop_name)

        # create tag
        tag = "tag_"+str(row)
        # highlight text
        text.tag_add(tag, str(row)+".0", str(row)+"."+str(10+9*(len(train.stops)+1)))
        text.tag_config(tag, background="white", foreground=train.color)
        text.insert(tk.INSERT, "\n")
        # move row index
        row+=1

    text.insert(tk.INSERT, "===================================\n")
    text.insert(tk.INSERT, "\n")

    # make text widget disabled
    text.configure(state="disabled")

def write_states():
    global text

    # make text widget normal
    text.configure(state="normal")

    text.insert(tk.INSERT, "===================================\n")
    text.insert(tk.INSERT, "              STATES\n")
    text.insert(tk.INSERT, "===================================\n")

    # num variable
    num = 3 + len(trains_list) + 2 + 4

    for state in state_dict.keys():
        text.insert(tk.INSERT, state)
        text.insert(tk.INSERT, " -> ")
        text.insert(tk.INSERT, state_dict.get(state))
        text.insert(tk.INSERT, "\n")

        # get train index
        train_index = int(state_dict.get(state).split(" ")[0][-1])

        # create tag
        tag = "tag_"+str(num)
        # highlight text
        text.tag_add(tag, str(num)+".6", str(num)+".14")
        text.tag_config(tag, background="white", foreground=COLOR[train_index-1])
        # move num index
        num+=1

    text.insert(tk.INSERT, "===================================\n")
    text.insert(tk.INSERT, "\n")

    # make text widget disabled
    text.configure(state="disabled")

def main_program(root):
    global fps

    while start_btn == False and exit_btn == False:
        try:    
            # update root window
            root.update()

        except tk.TclError:
            # catching _tkinter.tclError
            break

    if start_btn == True and exit_btn == False:
        # destroy start button window
        start_button_window.destroy()
        # pack other button windows
        button_window_1.pack(side = tk.LEFT)
        button_window_2.pack(side = tk.TOP)
        # create scale variable
        fps = tk.IntVar()
        # create simulator buttons
        create_simulator_buttons(button_window_1, button_window_2)
        # create pygame window
        [pygame_screen, win_color] = create_pygame_window()
        # call main loop
        main_loop(pygame_screen, win_color, root)

    else:
        # exit program
        return

def main_loop(pygame_screen, win_color, root):
    global rail_offset_x, rail_offset_y, enable_sort
    global enable_stops, enable_start
    global fps

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

            # STOPS
            if enable_stops == True and enable_lines == False and enable_nums == False and enable_start == False:
                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        # check if stop exists
                        check = check_if_stop_exists(event.pos, stops_list)
                        if check == False:
                            # saving coordinates on which LEFT mouse button clicked
                            stops_coordinates.append(event.pos)
                            # creating stop object
                            create_stops(pygame_screen, event.pos, root, check, two_lane=False)

                        elif check != False and enable_train == True:
                            # saving coordinates on which LEFT mouse button clicked
                            stops_coordinates.append(check.position)
                            # creating stop object
                            create_stops(pygame_screen, check.position, root, check, two_lane=False)

                        else:
                            # write message
                            write_message("ERROR: Stop already exists at this place!!\n")

                    elif event.button == 3:
                        # check if stop exists
                        check = check_if_stop_exists(event.pos, stops_list)
                        if check == False:
                            # saving coordinates on which RIGHT mouse button clicked
                            stops_coordinates.append(event.pos)
                            # creating stop object
                            create_stops(pygame_screen, event.pos, root, check, two_lane=True)

                        elif check != False and enable_train == True:
                            # saving coordinates on which RIGHT mouse button clicked
                            stops_coordinates.append(check.position)
                            # creating stop object
                            create_stops(pygame_screen, check.position, root, check, two_lane=True)

                        else:
                            # write message
                            write_message("ERROR: Stop already exists at this place!!\n")

                    else:
                        pass

                else:
                    pass

            # RAILS
            elif enable_stops == False and enable_lines == True and enable_nums == False and enable_start == False:
                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        # checking if stops are being connected
                        rez = check_pos(event.pos, stops_coordinates)

                        if rez != None:
                            # check if user is trying to connect the stop to itself
                            if check_if_rails_are_too_close(rez, rails_coordinates) == False:
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
                                # write error message
                                write_message("ERROR: Cannot connect the stop to itself!!\n")

                        else:
                            # write message
                            write_message("ERROR: Only stops can be connected with rails!!\n")

                    else:
                        pass

                else:
                    pass

            # TIME UNITS
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
                # sort trains lists
                sort_lists(trains_list)
                # get states
                get_states(trains_list)
                # write trains routes
                write_routes()
                # write states
                write_states()
                # disable scale
                scale.configure(state="disabled")
                enable_sort = False

            # try to update trains positions
            if len(trains_list) != 0:
                try:
                    # update trains positions
                    update_trains()

                except IndexError:
                    # catching IndexError
                    enable_start = False
                    enable_stops = True
                    enable_sort = True
                    # enable scale
                    scale.configure(state="normal")
                    # write message
                    write_message("ERROR: Stops are not connected!!\n")

            else:
                enable_start = False
                enable_stops = True
                enable_sort = True
                # enable scale
                scale.configure(state="normal")
                # write message
                write_message("ERROR: No stop or train has been created!!\n")

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

        # clock fps
        clock.tick(fps.get())

################################################################################################################


###############################################  MAIN FUNCTION  ################################################

if __name__ == "__main__":

    '''
    This is the main function used to run the program, create class objects and call all relevant
    functions so that the simulator can run normally.
    '''

    # creating root window
    root = init_root_window()
    # creating pygame and button windows
    [start_button_window, bottom_button_window, button_window_1, button_window_2] = create_button_windows(root)
    # creating start buttons
    create_start_buttons(start_button_window, bottom_button_window)
    # starting main program
    main_program(root)

################################################################################################################
