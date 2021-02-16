import random
import copy

from src.generators.Generator import Generator
from src.parsing.parse import *
from src.parsing.typechecker_recur import *

type2num = {'Bool': 0, 'Real': 1, 'Int': 2, 'RoundingMode': 3, 'String': 4, 
'RegLan': 5, 'Unknown': 6}

class TypeMutation(Generator):
    def __init__(self, formula, args, unique_expr):
        self.args = args 
        self.formula = formula 
        self.unique_expr = unique_expr
        
    def get_replacee(self):
        av_expr = []
        expr_type = []
        for i in range(len(self.formula.assert_cmd)):
            exps, typ = typecheck_recur(self.formula.assert_cmd[i]) 
            av_expr += exps
            expr_type += typ
        pool = [i for i in range(len(av_expr))]
        counter = 0
        while counter <= 5:
            if pool:
                k = random.choice(pool)
                t1 = av_expr[k]
                typ = type2num[expr_type[k]]
                if self.unique_expr[typ]:
                    t2 = random.choice(self.unique_expr[typ])
                    if t1 == t2:
                        pool.remove(k)
                        counter += 1 
                    else:
                        return t1, t2
                else:
                    pool.remove(k)
                    counter += 1
            else:
                return False
        return False 

    def generate(self):
        for _ in range(self.args.modulo):
            res = self.get_replacee()
            if res:
                t1, t2 = res
                t1.substitute(t1, t2)
                return self.formula, True      
        return None, False
