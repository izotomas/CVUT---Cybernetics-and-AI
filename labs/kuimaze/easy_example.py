#!/usr/bin/python3
'''
Very simple example how to use gym_wrapper and BaseAgent class for state space search 
@author: Zdeněk Rozsypálek, and the KUI-2018 team
@contact: svobodat@fel.cvut.cz
@copyright: (c) 2017, 2018
'''

import time
import kuimaze
import os
import random


class Agent(kuimaze.SearchAgent):
    '''
    Simple example of agent class that inherits kuimaze.BaseAgent class 
    '''

    def __init__(self, environment):
        self.environment = environment
        self.__frontier = []

    def heuristic_function(self, position, goal):
        '''
        Method that must be implemented by you. 
        We are expecting that you will implement some admissible heuristic function. 
        '''
        dx = abs(position[0] - goal[0])
        dy = abs(position[1] - goal[1])
        return dx + dy

    def find_path(self):
        '''
        Method that must be implemented by you. 
        Expects to return a path_section as a list of positions [(x1, y1), (x2, y2), ... ].
        '''
        observation = self.environment.reset()  # must be called first, it is necessary for maze initialization
        print("observation", observation)
        goal = observation[1][0:2]
        position = observation[0][0:2]  # initial state (x, y)
        print("Starting random searching from position %s to %s" % (position, goal))
        while True:
            new_positions = self.environment.expand(position)  # [[(x1, y1), cost], [(x2, y2), cost], ... ]
            self.__adjust_weights(new_positions, goal)
            # print("possible positions: ", new_positions)
            # print(new_positions)
            position = random.choice(new_positions)[0]  # select next at random, ignore the cost infor
            print(position)
            if position == goal:  # break the loop when the goal position is reached
                print("goal reached")
                break
            self.environment.render()  # show environment's GUI DO NOT FORGET TO COMMENT THIS LINE!
            time.sleep(0.1)  # sleep for demonstration DO NOT FORGET TO COMMENT THIS LINE!

        path = [(4, 0), (4, 1)]  # create path as list of lists in format: [(x1, y1), (x2, y2), ... ]
        input("press enter for exit")
        return path

    def __adjust_weights(self, positions, goal):
        for pos in positions:
            pos[1] = self.heuristic_function(pos[0], goal)
            print("possible position: %s\tweight: %s" % (pos, pos[1]))


if __name__ == '__main__':

    MAP = 'maps/easy/easy3.bmp'
    MAP = os.path.join(os.path.dirname(os.path.abspath(__file__)), MAP)
    GRAD = (0, 0)
    SAVE_PATH = False
    SAVE_EPS = False

    env = kuimaze.InfEasyMaze(map_image=MAP, grad=GRAD)  # For using random map set: map_image=None
    agent = Agent(env)

    path = agent.find_path()
    env.set_path(path)  # set path it should go from the init state to the goal state
    if SAVE_PATH:
        env.save_path()  # save path of agent to current directory
    if SAVE_EPS:
        env.save_eps()  # save rendered image to eps
    env.render(mode='human')
    time.sleep(3)
