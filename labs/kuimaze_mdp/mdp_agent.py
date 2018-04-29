import operator
import random
import copy


class __MDP_agent:
    """
    Private class for easier communication with provided API
    """
    def __init__(self, env):
        self.states = env.get_all_states()
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

    def get_expected_utility(self, state, utility):
        """
        Getter for optimal action and utility from a given state
        :param state: State object
        :param utility: list of utilities for all states in a problem scope
        :return: tuple with optimal action and its utility (action, utility)
        """
        actions = self.__actions[state]
        expected_utils = list()
        for action in actions:
            t_util = sum([prob * utility[(s.x, s.y)] for (s, prob) in self.__transitions[(state, action)]])
            expected_utils.append((action, t_util))
        return max(expected_utils, key=operator.itemgetter(1))


# region Policy Iteration

def find_policy_via_policy_iteration(problem, discount_factor):
    None
    
# endregion


# region Value Iteration

def find_policy_via_value_iteration(problem, discount_factor, epsilon):
    agent = __MDP_agent(problem)
    states = [s for s in agent.states if not problem.is_goal_state(s)]
    optimal_utility = __init_utility(problem)
    policy = {}
    while True:
        delta = 0
        utility = copy.deepcopy(optimal_utility)
        for state in states:
            action, expected_util = agent.get_expected_utility(state, utility)
            optimal_utility[(state.x, state.y)] = state.reward + discount_factor * expected_util
            policy[(state.x, state.y)] = action
            delta = max(delta, abs(utility[(state.x, state.y)] - optimal_utility[state.x, state.y]))
        if __has_converged(delta, discount_factor, epsilon):
            return policy


def __has_converged(delta, gamma, epsilon):
    """
    Checks if policy via value iteration has converged
    :param delta: the maximum change in the utility of any state in an iteration
    :param gamma: discount factor
    :param epsilon: the maximum error allowed in the utility of any state
    :return: True, if policy has converged
    """

    return delta < (epsilon * ((1 - gamma) / gamma))

# endregion

# region Helpers


def __get_visualisation_values(dictionary):
    if dictionary is None:
        return None
    ret = []
    for key, value in dictionary.items():
        # ret.append({'x': key[0], 'y': key[1], 'value': [value, value, value, value]})
        ret.append({'x': key[0], 'y': key[1], 'value': value})
    return ret


def __init_policy(env):
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

# endregion
