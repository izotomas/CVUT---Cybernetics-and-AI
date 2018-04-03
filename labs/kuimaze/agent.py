#!/usr/bin/python3
import kuimaze
import os
import heapq


class Agent(kuimaze.SearchAgent):

    def __init__(self, environment):
        self.environment = environment

        # currently discovered nodes that are not evaluated yet
        self.__frontier_pq = []

        # the set of already evaluated coordinates (x, y)
        self.__explored_set = set()

        # which node can a given node be most efficiently reached from
        self.__came_from = {}

        # cost of getting from the start node to a given node
        self.__g_score = {}

        # total cost of getting from the start to the goal (including heuristic)
        self.__f_score = {}

        # goal coordinates (x, y)
        self.__goal = None

        # max path length constant
        self.__MAX_PATH_LEN = 99999999

    # region API Functions

    def heuristic_function(self, position, goal):
        dx = abs(position[0] - goal[0])
        dy = abs(position[1] - goal[1])
        return dx + dy

    def find_path(self):
        self.__setup_start_and_goal()

        while self.__is_something_on_the_frontier():
            current = self.__pop()
            if self.__is_goal_state_reached(current.state):
                return self.__get_the_path()

            self.__mark_state_explored(current.state)

            neighbors = self.__get_neighbors_of(current.state)
            for neighbor in neighbors:
                (state, transition_cost) = neighbor
                self.__assign_costs_to(state, transition_cost, current.state)

                node = self.Node(self.__g_score[state], self.__f_score[state], transition_cost, state)
                if self.__is_state_unexplored(node.state):
                    if self.__is_node_worthy_of_exploring(node):
                        self.__push(node)
                    self.environment.render()   # show environment's GUI DO NOT FORGET TO COMMENT THIS LINE!
                    # time.sleep(0.1)             # sleep for demonstration DO NOT FORGET TO COMMENT THIS LINE!

        return None

    # endregion

    # region Helper Functions

    def __is_goal_state_reached(self, state):
        return state == self.__goal

    def __is_something_on_the_frontier(self):
        return len(self.__frontier_pq) > 0

    def __is_state_unexplored(self, state):
        return state not in self.__explored_set

    def __is_node_worthy_of_exploring(self, node):
        """
            Returns True if node with the same coordinates does not lie on the frontier
            or if the current one has a better cost
        """
        return len([n for n in self.__frontier_pq if (n.state == node.state and n < node)]) == 0

    def __get_neighbors_of(self, state):
        return self.environment.expand(state)

    def __get_the_path(self):
        """
            Builds the shortest path from start to goal as [(x0, y0), (x1, y1), ..., (xn, yn)]
            once the goal is reached
        """
        shortest_path = [self.__goal]
        current = self.__goal
        while current in self.__came_from.keys():
            current = self.__came_from[current]
            shortest_path.insert(0, current)
        return shortest_path

    def __get_g_score_of(self, state):
        return self.__g_score.get(state, self.__MAX_PATH_LEN)

    def __get_f_score_of(self, state):
        return self.__f_score.get(state, self.__MAX_PATH_LEN)

    def __assign_costs_to(self, state, transition_cost, from_state):
        """Assigns f_score and g_score to a given state"""
        g_old = self.__get_g_score_of(state)
        g_new = self.__g_score[from_state] + transition_cost
        if g_new < g_old:
                self.__g_score[state] = g_new
                self.__came_from[state] = from_state
        f_old = self.__get_f_score_of(state)
        f_new = self.heuristic_function(state, self.__goal) + self.__g_score[state]
        self.__f_score[state] = min(f_old, f_new)

    def __mark_state_explored(self, state):
        self.__explored_set.add(state)

    def __pop(self):
        return heapq.heappop(self.__frontier_pq)

    def __push(self, node):
        return heapq.heappush(self.__frontier_pq, node)

    def __setup_start_and_goal(self):
        """ Identifies the goal and sets up starting node """
        (start, goal) = self.environment.reset()[0:2]
        (s_state, s_transition_cost) = (start[0:2], start[2])
        (g_state, g_transition_cost) = (goal[0:2], goal[2])
        self.__goal = g_state
        self.__g_score[s_state] = s_transition_cost
        self.__f_score[s_state] = self.heuristic_function(s_state, g_state) + s_transition_cost
        node = self.Node(self.__g_score[s_state], self.__f_score[s_state], s_transition_cost, s_state)
        self.__push(node)

    # endregion

    # region Node - Inner Class

    class Node:
        def __init__(self, g, f, transition_cost, state):
            self.g = g
            self.f = f
            self.transition_cost = transition_cost
            self.state = state

        # comparing for heapq
        def __lt__(self, other):
            if self.f == other.f:
                return self.g <= other.g
            else:
                return self.f <= other.f

    # endregion


# region Main

if __name__ == '__main__':

    MAP = 'maps/normal/normal10.bmp'
    MAP = os.path.join(os.path.dirname(os.path.abspath(__file__)), MAP)
    GRAD = (0, 0)
    SAVE_PATH = False
    SAVE_EPS = False

    env = kuimaze.InfEasyMaze(map_image=MAP, grad=GRAD)  # For using random map set: map_image=None
    agent = Agent(env)

    path = agent.find_path()
    env.set_path(path)  # set path it should go from the init state to the goal state
    if SAVE_PATH:
        env.save_path() # save path of agent to current directory
    if SAVE_EPS:
        env.save_eps()  # save rendered image to eps
    env.render(mode='human')
    input("Press Return for exit")

# endregion
