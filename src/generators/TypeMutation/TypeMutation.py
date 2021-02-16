import random
import copy

from src.generators.Generator import Generator
from src.parsing.parse import *
from src.generators.TypeMutation.util import *


class TypeMutation(Generator):
    def __init__(self, formula, args, unique_expr):
        self.args = args
        self.formula = formula
        self.unique_expr = unique_expr

    def get_replacee(self,t):
        typ_id = type2num[t.type]
        if self.unique_expr[typ_id]:
            choices = [tPrime for tPrime in self.unique_expr[typ_id] if tPrime != t]

            if len(choices) == 0:
                return None

            return random.choice(choices)
        return None

    def generate(self):
        success = False
        self.av_expr, self.expr_type = get_all_subterms(self.formula)
        num_holes = len(self.av_expr)

        for _ in range(num_holes): # Intuition try at most number of holes
            t1 = random.choice(self.av_expr)
            t2 = self.get_replacee(t1)
            if t2:
                success = True
                t1.substitute(t1, t2)
                break

        return self.formula, success
