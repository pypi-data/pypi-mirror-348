import speech_recognition as sr
import pyttsx3
from lark import Lark, Transformer, v_args
import os

engine = pyttsx3.init()
def speak(text):
    print(f"SpokenPy: {text}")
    engine.say(text)
    engine.runAndWait()

grammar = r"""
    start: statement+

    ?statement: assign_stmt
              | print_stmt
              | if_stmt
              | while_stmt
              | for_stmt

    assign_stmt : NAME "equals" expr              -> assign
    print_stmt  : "print" expr                     -> print
    if_stmt     : "if" condition "then" statement+ ("else" statement+)?   -> ifelse
    while_stmt  : "while" condition "do" statement+                      -> whileloop
    for_stmt    : "for" NAME "in" "range" NUMBER "to" NUMBER "do" statement+  -> forloop

    ?condition  : expr comparator expr

    ?expr       : term
                | expr "+" term   -> add
                | expr "-" term   -> sub

    ?term       : factor
                | term "*" factor -> mul
                | term "/" factor -> div

    ?factor     : NUMBER           -> number
                | NAME             -> var
                | "(" expr ")"

    comparator : "greater than"   -> gt
               | "less than"      -> lt
               | "equals"         -> eq
               | "not equals"     -> neq

    %import common.CNAME -> NAME
    %import common.NUMBER
    %import common.WS
    %ignore WS
"""

@v_args(inline=True)
class SpokenPyTransformer(Transformer):
    def __init__(self):
        self.vars = {}
        self.code_buffer = []

    def assign(self, name, value):
        self.vars[str(name)] = value
        line = f"{name} = {value}"
        self.code_buffer.append(line)
        speak(f"Assigned {name} equals {value}")

    def print(self, value):
        line = f"print({value})"
        self.code_buffer.append(line)
        speak(f"Print statement added")

    def number(self, token):
        return int(token)

    def var(self, name):
        if str(name) in self.vars:
            return self.vars[str(name)]
        else:
            speak(f"Warning: variable {name} not defined")
            return 0

    def add(self, a, b): return a + b
    def sub(self, a, b): return a - b
    def mul(self, a, b): return a * b
    def div(self, a, b): return a // b

    def gt(self): return ">"
    def lt(self): return "<"
    def eq(self): return "=="
    def neq(self): return "!="

    def condition(self, left, op, right):
        ops = {">": lambda a,b: a > b,
               "<": lambda a,b: a < b,
               "==": lambda a,b: a == b,
               "!=": lambda a,b: a != b}
        return ops[op](left, right)

    def ifelse(self, cond, then_block, else_block=None):
        # Store as Python code string
        then_code = "\n".join([str(s) for s in then_block.children])
        else_code = "\n".join([str(s) for s in else_block.children]) if else_block else ""
        if_code = f"if {cond}:\n    {then_code.replace(chr(10), chr(10)+'    ')}"
        if else_code:
            if_code += f"\nelse:\n    {else_code.replace(chr(10), chr(10)+'    ')}"
        self.code_buffer.append(if_code)
        speak("If-else statement added")

    def whileloop(self, cond, stmts):
        body = "\n".join([str(s) for s in stmts.children])
        code = f"while {cond}:\n    {body.replace(chr(10), chr(10)+'    ')}"
        self.code_buffer.append(code)
        speak("While loop added")

    def forloop(self, varname, start, end, stmts):
        body = "\n".join([str(s) for s in stmts.children])
        code = f"for {varname} in range({start}, {end+1}):\n    {body.replace(chr(10), chr(10)+'    ')}"
        self.code_buffer.append(code)
        speak("For loop added")

def listen_command():
    r = sr.Recognizer()
    mic = sr.Microphone()
    with mic as source:
        speak("Listening...")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
    try:
        command = r.recognize_google(audio).lower()
        print(f"You said: {command}")
        return command
    except Exception as e:
        speak("Sorry, I didn't catch that.")
        return ""

def save_code(filename, code_lines):
    with open(filename, "w") as f:
        f.write("\n".join(code_lines))
    speak(f"Code saved to {filename}")

def load_code(filename):
    if os.path.exists(filename):
        with open(filename, "r") as f:
            lines = f.readlines()
        speak(f"Loaded code from {filename}")
        return [line.strip() for line in lines]
    else:
        speak(f"No file named {filename} found")
        return []

def main():
    transformer = SpokenPyTransformer()
    parser = Lark(grammar, parser='lalr', transformer=transformer)

    speak("Welcome to SpokenPy voice coding environment.")
    speak("Say 'run code' to execute, 'save code' to save, 'load code' to load, 'clear code' to reset.")

    while True:
        cmd = listen_command()
        if not cmd:
            continue

        if "run code" in cmd:
            try:
                code = "\n".join(transformer.code_buffer)
                speak("Running your code now.")
                print("Executing:\n", code)
                exec(code, {}, transformer.vars)
            except Exception as e:
                speak(f"Error running code: {e}")
        elif "save code" in cmd:
            speak("Please say the filename.")
            filename = listen_command()
            if filename:
                save_code(filename, transformer.code_buffer)
        elif "load code" in cmd:
            speak("Please say the filename to load.")
            filename = listen_command()
            if filename:
                loaded_lines = load_code(filename)
                transformer.code_buffer = loaded_lines
        elif "clear code" in cmd:
            transformer.code_buffer.clear()
            transformer.vars.clear()
            speak("Code cleared")
        else:
            # Try to parse as code statement
            try:
                parser.parse(cmd)
            except Exception as e:
                speak(f"Could not parse command: {e}")

if __name__ == "__main__":
    main()
