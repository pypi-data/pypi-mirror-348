from nuggetry.parser import get_parser
from nuggetry.interpreter import run

def main():
    parser = get_parser()
    env = {}
    print("Nuggetry REPL. Type 'exit;' to quit.")
    while True:
        try:
            line = input(">>> ")
            if line.strip() == "exit;": break
            tree = parser.parse(line)
            run(tree.children, env)
        except Exception as e:
            print("Error:", e)
