import pygame
import time, math
import tkinter as tk
from pygame.locals import *
import Stop_class, Rails_class

pygame.init()

class Train():
    def __init__(self, position, pygame_screen, color, train_num, image_path=None):
        # train parameters
        self.position = position
        self.pygame_screen = pygame_screen
        self.color = color
        self.train_num = train_num
        self.train_name = "TRAIN_"+str(train_num)
        self.stops = []
        self.rails = []
        self.stops_and_rails = []
        self.i = 0
        self.stop_cnt = 1
        self.start_time = 0
        self.set_start_time = True
        self.distance = 0
        self.occ = None
        self.path = None
        self.path_cnt = 0
        #self.image = pygame.image.load(image_path)

    def draw(self):
        train_rect = pygame.Rect(self.position[0]-8, self.position[1]-8, 16, 16)
        pygame.draw.rect(self.pygame_screen, self.color, train_rect)
        #self.pygame_screen.blit(self.image, self.position)

    def calculate_path(self, end):

        # get coordinates
        x1 = self.position[0]
        y1 = self.position[1]
        x2 = end[0]
        y2 = end[1]
        # calculate distances
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        # determine step size
        step = self.step_size(end)
        # determine which way to go
        sx = step if x1 < x2 else -step
        sy = step if y1 < y2 else -step

        x = x1
        y = y1
        points = []

        if dx > dy:
            err = dx/2.0

            while x != x2:
                points.append((x, y))
                err -= dy

                if err < 0:
                    y += sy
                    err += dx

                x += sx

        else:
            err = dy/2.0

            while y != y2:
                points.append((x, y))
                err -= dx

                if err < 0:
                    x += sx
                    err += dy

                y += sy

        points.append((x, y))

        return points

    def move_train(self):

        # check if path exists
        if self.path != None:
            # determine next position
            next_pos = self.path[self.path_cnt]
            self.path_cnt+=1 if self.path_cnt < len(self.path) else 0
            # update train position
            self.position = next_pos

        else:
            return

    def sort_list(self):
        stops = []
        rails = []

        for obj in self.stops_and_rails:
            # check if stop
            if isinstance(obj, Stop_class.Stop) == True:
                stops.append(obj)
                # put stops in a list
                self.stops.append(obj)

            # check if rails    
            elif isinstance(obj, Rails_class.Rails) == True:
                rails.append(obj)
                # put rails in a list
                self.rails.append(obj)

            else:
                pass

        self.stops_and_rails.clear()
        self.stops_and_rails = stops

        # sort
        i = 1
        for rail in rails:
            self.stops_and_rails.insert(i, rail)
            i += 2

    def step_size(self, end):
        rail = self.rails[self.stop_cnt-1] if self.stop_cnt != 0 else self.rails[len(self.rails)-1]

        if rail.text != "":
            # get path time in seconds
            time = int(rail.text)*60

            # calculate distance
            if self.distance == 0:
                self.distance = math.sqrt((end[0]-self.position[0])**2 + (end[1]-self.position[1])**2)

            # calculate velocity
            velocity = self.distance/time
            if velocity <= 0.5:
                step = 0.5

            elif velocity >= 1:
                step = 1

            else:
                step = 0.5 if velocity < 0.75 else 1
            # return velocity
            return step

        else:
            # return max possible velocity
            return 1

    def wait_at_stop(self, text):
        if text != "":
            # get delay time
            n = int(text)

            if self.set_start_time == True:
                # get start time
                self.start_time = time.time()
                self.set_start_time = False

            if time.time() >= self.start_time + n:
                # enable set start time variable
                self.set_start_time = True

                return True

            else:
                return False

        else:
            return True

    def check_if_occupied(self, stop):
        # check if stop has two lanes
        if stop.two_lane == True:
            # if does check if both lanes are occupied
            if stop.occupied_1 == True and stop.occupied_2 == True:
                return True

            else:
                return False

        elif stop.two_lane == False:
            # check if stop is occupied
            if stop.occupied_1 == True:
                return True

            else:
                return False

    def occupy(self, stop):
        # check if stop has two lanes
        if stop.two_lane == True:
            # check if train has already occupied stop
            if self.occ == None:
                # if not occupy it
                if stop.occupied_1 == False and stop.occupied_2 == False:
                    stop.occupied_1 = True
                    self.occ = 1

                elif stop.occupied_1 == True and stop.occupied_2 == False:
                    stop.occupied_2 = True
                    self.occ = 2

                elif stop.occupied_1 == False and stop.occupied_2 == True:
                    stop.occupied_1 = True
                    self.occ = 1

        elif stop.two_lane == False:
            # check if train has already occupied stop
            if self.occ == None:
                # if not occupy it
                stop.occupied_1 = True

    def unoccupy(self, stop):
        # check if stop has two lanes
        if stop.two_lane == True:
            # unoccupy the stop so other trains can come
            if stop.occupied_1 == True and stop.occupied_2 == True:
                if self.occ == 1:
                    stop.occupied_1 = False
                    self.occ = None

                elif self.occ == 2:
                    stop.occupied_2 = False
                    self.occ = None

            elif stop.occupied_1 == True and stop.occupied_2 == False:
                stop.occupied_1 = False
                self.occ = None

            elif stop.occupied_1 == False and stop.occupied_2 == True:
                stop.occupied_2 = False
                self.occ = None

        elif stop.two_lane == False:
            # unoccupy the stop so other trains can come
            stop.occupied_1 = False
            self.occ = None
