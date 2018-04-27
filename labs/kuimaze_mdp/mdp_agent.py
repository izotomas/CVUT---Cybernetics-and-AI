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


def __find_policy_via_policy_iteration(env, gamma):
    agent = MDP_agent(env)
    utility = __init_utility(env)
    policy = __init_policy(env)
    while True:
        utility = __policy_evaluation(policy, utility, gamma, agent, env.is_goal_state)
        unchanged = True
        for s in agent.states:
            if env.is_goal_state(s):
                continue
            action = __argmax(agent.get_actions(s), lambda a: __expected_utility(a, s, utility, agent))
            if action != policy[(s.x, s.y)]:
                policy[(s.x, s.y)] = action
                unchanged = False
        if unchanged:
            return policy


def find_policy_via_policy_iteration(env, discount_factor):
    return __find_policy_via_policy_iteration(env, discount_factor)


def __policy_evaluation(policy, utility, gamma, agent, fn_goal_check, k=20):
    for i in range(k):
        for s in agent.states:
            if fn_goal_check(s):
                continue
            utility[(s.x, s.y)] = s.reward + gamma * sum([p * utility[(s.x, s.y)]
                                                          for (s1, p) in agent.get_transition(s, policy[(s.x, s.y)])])
    return utility


def __expected_utility(a, s, U, agent):
    "The expected utility of doing a in state s, according to the MDP and U."
    return sum([p * U[(s1.x, s1.y)] for (s1, p) in agent.get_transition(s, a)])

def __argmax(seq, fn):
    """Return an element with highest fn(seq[i]) score; tie goes to first one.
    """
    return __argmin(seq, lambda x: -fn(x))


def __argmin(seq, fn):
    """
    Return an element with lowest fn(seq[i]) score; tie goes to first one.
    """
    best = seq[0];
    best_score = fn(best)
    for x in seq:
        x_score = fn(x)
        if x_score < best_score:
            best, best_score = x, x_score
    return best


# region Value Iteration private functions

def value_iteration(env, agent, gamma, epsilon):
    """
    :param env: kuimaze.MDPMaze object
    :param agent: Mdp_agent object
    :param gamma: discount factor
    :param epsilon:
    :return: converged utility dictionary (k => (x, y), val => utility)
    """
    u1 = __init_utility(env)
    states = agent.states
    transit = agent.get_transition
    actions = agent.get_actions
    threshold = epsilon * (1 - gamma) / gamma

    while True:
        u = copy.deepcopy(u1)
        delta = 0
        for s in states:
            if env.is_goal_state(s):
                continue  # skip goal node utility computation

            # utility[s] = rewards(s) + gamma * max([sum([p * optimal_utility[s1] for (s1, p) in transit(s, a)])
            #                                       for a in actions(s)])
            # utility[(s.x, s.y)] = s.reward + gamma * max([__total_utility(optimal_utility, transit(s, a))
            #                                              for a in actions(s)])
            u1[(s.x, s.y)] = s.reward + gamma * max([__total_utility(u, transit(s, a))
                                                     for a in actions(s)])

            delta = max(delta, abs(u[(s.x, s.y)] - u1[(s.x, s.y)]))
        if delta < threshold:
            return u1


def __total_utility(utility, transitions):
    return sum([probability * utility[state] for (state, probability) in transitions])


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

# region Helpers for both


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
