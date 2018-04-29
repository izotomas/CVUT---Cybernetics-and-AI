import operator
import random
import copy


class MDP_agent:

    def __init__(self, env):
        self.__states = dict(((s.x, s.y), s) for s in env.get_all_states())
        self.__transitions = {}
        self.__actions = {}
        for s in self.__states.values():
            self.__actions[s] = list(env.get_actions(s))
            for a in self.__actions[s]:
                self.__transitions[s, a] = [(s, p) for (s, p) in env.get_next_states_and_probs(s, a)]

    @property
    def states(self):
        return list(self.__states.values())

    def get_transition(self, state, action):
        """
        :param state: tuple with cartesian coordinates (x, y)
        :param action: enum Action
        :return: list of probable outcomes for given trial [(state1, prob1), ...,(state_n, prob_n)]
        """
        return self.__transitions[(state, action)]

    def get_actions(self, state):
        """
        :param state: tuple with cartesian coordinates (x, y)
        :return: list of enum Actions
        """
        return self.__actions[state]


def find_policy_via_policy_iteration(env, discount_factor):
    None


# region Value Iteration private functions

def find_policy_via_value_iteration(problem, discount_factor, epsilon):
    policy = {}
    optimal_utility = __init_utility(problem)
    agent = MDP_agent(problem)
    while True:
        delta = 0
        utility = copy.deepcopy(optimal_utility)
        for s in agent.states:
            if problem.is_goal_state(s):
                continue
            action, expected_util = __expected_utility(agent, s, utility)
            optimal_utility[(s.x, s.y)] = s.reward + discount_factor * expected_util
            policy[(s.x, s.y)] = action
            delta = max(delta, abs(utility[(s.x, s.y)] - optimal_utility[s.x, s.y]))
        if __has_converged(delta, discount_factor, epsilon):
            return policy


def expected_utility(agent, state, utility):
    actions = agent.get_actions(state)
    expected_utils = list()
    for a in actions:
        t_util = 0
        for s, prob in agent.get_transition(state, a):
            t_util += prob * utility[(s.x, s.y)]
        expected_utils.append((a, t_util))
    return max(expected_utils, key=operator.itemgetter(1))


def __expected_utility(agent, state, utility):
    actions = agent.get_actions(state)
    expected_utils = list()
    for a in actions:
        t_util = 0
        for s, prob in agent.get_transition(state, a):
            t_util += prob * utility[(s.x, s.y)]
        expected_utils.append((a, t_util))
    return max(expected_utils, key=operator.itemgetter(1))


def __total_utility(utility, transitions):
    return sum([probability * utility[state] for (state, probability) in transitions])

# endregion

# region Helpers for both


def __has_converged(delta, gamma, epsilon):
    """
    Checks if policy via value iteration has converged
    :param delta: the maximum change in the utility of any state in an iteration
    :param gamma: discount factor
    :param epsilon: the maximum error allowed in the utility of any state
    :return: True, if policy has converged
    """

    return delta < (epsilon * ((1 - gamma) / gamma))


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
