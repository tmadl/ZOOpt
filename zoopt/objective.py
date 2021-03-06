
from zoopt.solution import Solution
from zoopt.utils.zoo_global import pos_inf
from zoopt.utils.tool_function import ToolFunction
"""
The class Objective represents the objective function and its associated variables

Author:
    Yuren Liu
"""


class Objective:

    def __init__(self, func=None, dim=None, constraint=None, resample_func=None, balance_rate=1):
        # Objective function defined by the user
        self.__func = func
        # Number of dimensions, dimension bounds are in the dim object
        self.__dim = dim
        # the function for inheriting solution attachment
        self.__inherit = self.default_inherit
        self.__post_inherit = self.default_post_inherit
        # the constraint function
        self.__constraint = constraint
        # the history of optimization
        self.__history = []
        self.__resample_func = self.resample_func if resample_func is None else resample_func
        self.__balance_rate = balance_rate

    # Construct a solution from x
    def construct_solution(self, x, parent=None):
        new_solution = Solution()
        new_solution.set_x(x)
        new_solution.set_attach(self.__inherit(parent))
        # new_solution.set_value(self.__func(new_solution)) # evaluation should
        # be invoked explicitly
        return new_solution

    # evaluate the objective function of a solution
    def eval(self, solution, intermediate_print=False, times=0, freq=100):
        val = self.__func(solution)
        solution.set_value(val)
        self.__history.append(solution.get_value())
        solution.set_post_attach(self.__post_inherit())
        if intermediate_print is True and times % freq == 0:
            ToolFunction.log(("budget %d, fx result: " % times) + str(val))
            ToolFunction.log("x: " + str(solution.get_x()))

    def resample(self, solution, repeat_times):
        if solution.get_resample_value() is None:
            solution.set_resample_value(self.__resample_func(solution, repeat_times))
            solution.set_value((1 - self.__balance_rate) * solution.get_value() +
                               self.__balance_rate * solution.get_resample_value())
            solution.set_post_attach(self.__post_inherit())

    def resample_func(self, solution, iteration_num):
        result = []
        for i in range(iteration_num):
            result.append(self.__func(solution))
        return sum(result) * 1.0 / len(result)

    def eval_constraint(self, solution):
        solution.set_value(
            [self.__func(solution), self.__constraint(solution)])
        self.__history.append(solution.get_value())
        solution.set_post_attach(self.__post_inherit())

    # set the optimization function
    def set_func(self, func):
        self.__func = func

    # get the optimization function
    def get_func(self):
        return self.__func

    # set the dimension object
    def set_dim(self, dim):
        self.__dim = dim

    # get the dimension object
    def get_dim(self):
        return self.__dim

    # set the attachment inheritance function
    def set_inherit_func(self, inherit_func):
        self.__inherit = inherit_func

    def set_post_inherit_func(self, inherit_func):
        self.__post_inherit = inherit_func

    def get_post_inherit_func(self):
        return self.__post_inherit

    # get the attachment inheritance function
    def get_inherit_func(self):
        return self.__inherit

    # set the constraint function
    def set_constraint(self, constraint):
        self.__constraint = constraint
        return

    # return the constraint function
    def get_constraint(self):
        return self.__constraint

    # get the optimization history
    def get_history(self):
        return self.__history

    # get the best-so-far history
    def get_history_bestsofar(self):
        history_bestsofar = []
        bestsofar = pos_inf
        for i in range(len(self.__history)):
            if self.__history[i] < bestsofar:
                bestsofar = self.__history[i]
            history_bestsofar.append(bestsofar)
        return history_bestsofar

    # clean the optimization history
    def clean_history(self):
        self.__history = []

    @staticmethod
    def default_inherit(parent=None):
        return None

    @staticmethod
    def default_post_inherit(parent=None):
        return None
