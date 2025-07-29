from lark import Lark, Transformer, v_args
from pathlib import Path

grammar_path = Path(__file__).parent / "grammar.lark"

@v_args(inline=True)
class NuggetryTransformer(Transformer):
    def number(self, token): return float(token)
    def string(self, token): return str(token)[1:-1]
    def var(self, name): return ('var', str(name))

    def assign_stmt(self, *args):
        is_local = len(args) == 3
        if is_local:
            _, name, value = args
        else:
            name, value = args
        return ('assign', is_local, str(name), value)

    def func_call(self, name, *args): return ('call', str(name), args)
    def if_stmt(self, *args): return ('if', args)
    def while_stmt(self, cond, *body): return ('while', cond, body)
    def repeat_stmt(self, *body_and_cond): *body, cond = body_and_cond; return ('repeat', body, cond)
    def func_def(self, name, *rest):
        if isinstance(rest[0], list): params, body = rest[0], rest[1:]
        else: params, body = [], rest
        return ('function', str(name), params, body)
    def return_stmt(self, value): return ('return', value)
    def break_stmt(self): return ('break',)
    def expr_list(self, *args): return list(args)
    def param_list(self, *args): return [str(arg) for arg in args]
    def not_expr(self, value): return ('not', value)
    def neg(self, value): return ('neg', value)

    def logic_or(self, *args): return reduce_binop('or', args)
    def logic_and(self, *args): return reduce_binop('and', args)
    def comparison(self, *args): return reduce_binop_seq(args)
    def sum(self, *args): return reduce_binop_seq(args)
    def term(self, *args): return reduce_binop_seq(args)
    def power(self, *args): return reduce_binop_seq(args)

def reduce_binop(op, items):
    if len(items) == 1: return items[0]
    res = items[0]
    for item in items[1:]: res = (op, res, item)
    return res

def reduce_binop_seq(args):
    if len(args) == 1: return args[0]
    result = args[0]
    for i in range(1, len(args), 2):
        result = (args[i], result, args[i+1])
    return result

def get_parser():
    with open(grammar_path) as f:
        grammar = f.read()
    return Lark(grammar, parser='lalr', transformer=NuggetryTransformer())
