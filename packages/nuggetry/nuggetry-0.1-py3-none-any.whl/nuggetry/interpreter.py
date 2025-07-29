def run(ast, env=None):
    if env is None: env = {}
    for stmt in ast:
        if isinstance(stmt, tuple) and stmt[0] == 'call':
            if stmt[1] == 'say':
                print(*[eval_expr(arg, env) for arg in stmt[2]])
        elif isinstance(stmt, tuple) and stmt[0] == 'assign':
            _, is_local, name, val = stmt
            env[name] = eval_expr(val, env)
    return env

def eval_expr(expr, env):
    if isinstance(expr, (int, float, str)): return expr
    if isinstance(expr, tuple):
        tag = expr[0]
        if tag == 'var': return env.get(expr[1], None)
        if tag in ('+', '-', '*', '/', '%', '^'):
            a = eval_expr(expr[1], env)
            b = eval_expr(expr[2], env)
            return eval(f"{a} {tag} {b}")
    return expr
