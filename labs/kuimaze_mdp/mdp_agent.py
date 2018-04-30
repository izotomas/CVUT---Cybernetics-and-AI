from abc import ABC, abstractmethod
import operator
import random
import copy


def find_policy_via_value_iteration(problem, discount_factor, epsilon):
    agent = __MDP_VI_agent(problem, discount_factor, epsilon)
    policy = agent.find_policy()
    return policy


def find_policy_via_policy_iteration(problem, discount_factor):
    agent = __MDP_PI_agent(problem, discount_factor)
    policy = agent.find_policy()
    return policy


class __MDP_agent(ABC):
    """
    Private (abstract) class for easier communication with provided API
    """
    def __init__(self, env, gamma):
        """
        :param env: is the environment, an object of the type kuimaze.MDPMaze
        :param gamma: discount factor - a number from range (0,1)
        """
        self.states = env.get_all_states()
        self.utility = self.__init_utility(env)
        self.gamma = gamma
        self.fn_is_terminal_state = env.is_goal_state
        self.__transitions = {}
        self.__actions = {}
        for s in self.states:
            self.__actions[s] = list(env.get_actions(s))
            for a in self.__actions[s]:
                self.__transitions[s, a] = [(s, p) for (s, p) in env.get_next_states_and_probs(s, a)]

    def get_transition(self, state, action):
        """
        Getter for transition model defined by given state and action attempt
        :param state: State object
        :param action: enum Action
        :return: list of probable outcomes for given trial [(state1, prob1), ...,(state_n, prob_n)]
        """
        return self.__transitions[(state, action)]

    def get_actions(self, state):
        """
        Getter for possible action in a given state
        :param state: State object
        :return: list of enum Actions for given state
        """
        return self.__actions[state]

    def get_optimal_action(self, state, utility):
        """
        Getter for optimal action and utility from a given state
        :param state: State object
        :param utility: list of utilities for all states in a problem scope
        :return: tuple with optimal action and its utility (action, utility)
        """
        actions = self.__actions[state]
        expected_utils = list()
        for action in actions:
            expected_utils.append((action, self.get_expected_utility(state, action, utility)))
        return max(expected_utils, key=operator.itemgetter(1))

    def get_expected_utility(self, state, action, utility):
        """
        Getter for expected utility for action from a given state
        :param state: State object
        :param action: enum Action
        :param utility: dictionary of utilities indexed by cartesian coordinates
        :return: total utility (value) for a move attempt in a given direction
        """
        return sum([prob * utility[(s.x, s.y)] for (s, prob) in self.__transitions[(state, action)]])

    @staticmethod
    def __init_utility(env):
        """
        Initialize all utilities to given states reward (except terminal states)
        :param env: kuimaze.MDPMaze object
        :return: dictionary of utilities, indexed by cartesian coordinates
        """
        utils = dict()
        x_dims = env.observation_space.spaces[0].n
        y_dims = env.observation_space.spaces[1].n

        for x in range(x_dims):
            for y in range(y_dims):
                utils[(x, y)] = 0

        for state in env.get_all_states():
            utils[(state.x, state.y)] = state.reward
        return utils

    @abstractmethod
    def find_policy(self):
        """
        :return: dictionary where the keyword is a cartesian coordinates tuple (x,y)
        and the value is the optimal action (Action enum)
        """
        pass


class __MDP_VI_agent(__MDP_agent):
    """
    MDP agent for setting policy via Value Iteration algorithm
    """
    def __init__(self, env, gamma, epsilon):
        """
        :param epsilon: maximum permitted error for the value of each state
        """
        self.__epsilon = epsilon
        self.__policy = self.__init_empty_policy(env)
        super().__init__(env, gamma)

    def find_policy(self):
        states = [s for s in self.states if not self.fn_is_terminal_state(s)]
        optimal_utility = self.utility
        policy = self.__policy
        while True:
            delta = 0
            utility = copy.deepcopy(optimal_utility)
            for state in states:
                action, expected_util = self.get_optimal_action(state, utility)
                optimal_utility[(state.x, state.y)] = state.reward + self.gamma * expected_util
                policy[(state.x, state.y)] = action
                delta = max(delta, abs(utility[(state.x, state.y)] - optimal_utility[state.x, state.y]))
            if self.__has_converged(delta):
                return policy

    @staticmethod
    def __init_empty_policy(env):
        """
        Initialize blank policy (with None values)
        :param env: kuimaze.MDPMaze object
        :return: dictionary of None, indexed by cartesian coordinates
        """
        policy = dict()
        for state in env.get_all_states():
            policy[state.x, state.y] = None
        return policy

    def __has_converged(self, delta):
        """
        Checks if policy via value iteration has converged
        :param delta: the maximum change in the utility of any state in an iteration
        :return: True, if policy has converged
        """
        return delta < (self.__epsilon * ((1 - self.gamma) / self.gamma))


class __MDP_PI_agent(__MDP_agent):
    """
    MDP agent for setting policy via Policy Iteration algorithm
    """
    def __init__(self, env, gamma):
        self.__policy = self.__init_random_policy(env)
        super().__init__(env, gamma)

    def find_policy(self):
        states = [s for s in self.states if not self.fn_is_terminal_state(s)]
        utility = self.utility
        policy = self.__policy
        while True:
            utility = self.__evaluate_policy(policy, utility)
            unchanged = True
            for state in states:
                action, action_util = self.get_optimal_action(state, utility)
                if action != policy[(state.x, state.y)]:
                    policy[(state.x, state.y)] = action
                    unchanged = False
            if unchanged:
                return policy

    def __evaluate_policy(self, policy, utility, steps=10):
        """
        :param policy: dictionary with key => cartesian coordinates (x,y) and value => Action enum
        :param utility: dictionary with key => cartesian coordinates (x,y) and value => numerical utility
        :param steps: number of utility re-evaluations before it is considered stabilized
        :return: updated utility dictionary
        """
        for i in range(steps):
            for state in self.states:
                x, y = state.x, state.y
                utility[(x, y)] = state.reward + self.gamma * self.get_expected_utility(state, policy[(x, y)], utility)
        return utility

    @staticmethod
    def __init_random_policy(env):
        """
        Initialize all policies randomly (except terminal states)
        :param env: kuimaze.MDPMaze object
        :return: dictionary of random policies, indexed by cartesian coordinates
        """
        policy = dict()
        for state in env.get_all_states():
            if env.is_goal_state(state):
                policy[state.x, state.y] = None
                continue
            actions = [action for action in env.get_actions(state)]
            policy[state.x, state.y] = random.choice(actions)
        return policy