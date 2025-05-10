import ast              # Enables working with Python's Abstract Syntax Tree.
import astunparse       # Converts an AST back into Python source code.
import sys              # Provides access to system-specific parameters and functions.
import textwrap         # Offers functions for wrapping and formatting text.
import argparse         # Helps in creating user-friendly command-line interfaces.
import random           # Implements pseudo-random number generators.
import string           # Contains common string constants (like lowercase letters).
import datetime

VERSION = "1.0.1"

# A class that inherits from ast.NodeTransformer to modify AST nodes.
class PythonObfuscator(ast.NodeTransformer): 
    def __init__(self): 
        self.var_map = {}               # Stores the mapping of original variable names to obfuscated names.
        self.func_map = {}              # Stores the mapping of original function names to obfuscated names.
        self.next_var_id = 0            # Counter used to generate unique variable names.
        self.next_func_id = 0           # Counter used to generate unique function names.
        self.global_names = set()       # Intended to hold global names (currently not actively used).
        self.random = random.Random()   # Creates a local random number generator instance.
        
    # Generates a unique, random lowercase variable name.
    def get_unique_var_name(self):
        length = self.random.randint(5, 10)
        return ''.join(self.random.choice(string.ascii_lowercase) for _ in range(length))

    # Generates a unique function name starting with a lowercase letter followed by lowercase letters or digits.
    def get_unique_func_name(self):
        length = self.random.randint(7, 12)
        return ''.join(self.random.choice(string.ascii_lowercase) for _ in range(1)) + \
               ''.join(self.random.choice(string.ascii_lowercase + string.digits) for _ in range(length - 1))

    # Visits 'Name' nodes in the AST (representing variable or function names) and potentially renames them.
    def visit_Name(self, node):
        if isinstance(node.ctx, ast.Load):
            if node.id in self.var_map:
                node.id = self.var_map[node.id]
            elif node.id in self.func_map:
                node.id = self.func_map[node.id]
        elif isinstance(node.ctx, ast.Store):
            if node.id not in self.var_map:
                new_name = self.get_unique_var_name()
                self.var_map[node.id] = new_name
            node.id = self.var_map[node.id]
        return node

    # Visits 'FunctionDef' nodes (representing function definitions) and renames the function and its arguments.
    def visit_FunctionDef(self, node):
        if node.name not in self.func_map:
            new_name = self.get_unique_func_name()
            self.func_map[node.name] = new_name
        node.name = self.func_map[node.name]

        for arg in node.args.args:
            if arg.arg not in self.var_map:
                new_name = self.get_unique_var_name()
                self.var_map[arg.arg] = new_name
            arg.arg = self.var_map[arg.arg]

        self.generic_visit(node)
        return node

    # Visits 'Call' nodes (representing function calls) and renames the function being called.
    def visit_Call(self, node):
        if isinstance(node.func, ast.Name):
            if node.func.id in self.func_map:
                node.func.id = self.func_map[node.func.id]
        self.generic_visit(node)
        return node

    # Visits 'comprehension' nodes (used in list/dict/set comprehensions) and renames variables within them.
    def visit_comprehension(self, node):
        if isinstance(node.target, ast.Name):
            original_name = node.target.id
            if original_name not in self.var_map:
                new_name = self.get_unique_var_name()
                self.var_map[original_name] = new_name
            node.target.id = self.var_map[original_name]

        node.iter = self.visit(node.iter)
        for if_node in node.ifs:
            self.visit(if_node)

        return node

    # Visits 'GeneratorExp' nodes (representing generator expressions) and renames variables within them.
    def visit_GeneratorExp(self, node):
        for gen in node.generators:
             self.visit(gen) 

        node.elt = self.visit(node.elt)
        return node

    # Visits 'Subscript' nodes (representing indexing) and ensures variables within are renamed.
    def visit_Subscript(self, node):
        node.value = self.visit(node.value)
        node.slice = self.visit(node.slice)
        return node

# Takes Python code as a string, parses it into an AST, obfuscates it using PythonObfuscator, and returns the obfuscated code as a string.
def obfuscate_code(code):
    try:
        tree = ast.parse(code)
        obfuscator = PythonObfuscator()
        new_tree = obfuscator.visit(tree)
        obfuscated_code = astunparse.unparse(new_tree)
        return obfuscated_code
    except Exception as e:
        print(f"Error during obfuscation: {e}")
        return code

# Removes inline comments and leading/trailing whitespace from a line of code.
def clean_line(line):
    line = line.split('#', 1)[0]
    return line.strip()

# Takes Python code, extracts and combines all import statements into a single 'import' line at the beginning.
def combine_imports(code):
    lines = code.splitlines()
    import_lines = []
    other_lines = []

    for line in lines:
        stripped = clean_line(line)
        if stripped.startswith("import "):
            modules = stripped.replace("import ", "").split(",")
            import_lines.extend([m.strip() for m in modules])
        else:
            other_lines.append(line)
    if import_lines:
        combined = "import " + ", ".join(sorted(set(import_lines)))
        other_lines.insert(0, combined)
    return "\n".join(other_lines)

# Takes the source code of a function definition and attempts to flatten it onto fewer lines while preserving block structure.
def compress_def_code(source):
    lines = source.splitlines()
    if not lines:
        return source

    header = lines[0].rstrip()
    body = lines[1:]

    dedented = textwrap.dedent("\n".join(body)).strip()
    if not dedented:
        return f"{header} pass"

    compressed_lines = []
    for line in dedented.splitlines():
        stripped = line.lstrip()
        if stripped.startswith(('if ', 'for ', 'while ', 'with ', 'try', 'except', 'else:', 'elif ', 'finally:')):
            compressed_lines.append(line)
        else:
            if compressed_lines and not compressed_lines[-1].endswith(':'):
                compressed_lines[-1] += f"; {stripped}"
            else:
                compressed_lines.append(line)

    compressed_body = "\n".join(compressed_lines)
    return f"{header}\n{textwrap.indent(compressed_body, '    ')}"

# Parses code, extracts top-level function definitions, compresses their bodies, and replaces the original definitions in the code.
def extract_and_compress_functions(code):
    tree = ast.parse(code)
    lines = code.splitlines()
    new_lines = lines.copy()
    functions = []

    for node in reversed(tree.body):
        if isinstance(node, ast.FunctionDef):
            start = node.lineno - 1
            end = getattr(node, 'end_lineno', None)

            if end is None:
                indent = len(lines[start]) - len(lines[start].lstrip())
                end = start + 1
                while end < len(lines):
                    if lines[end].strip() and len(lines[end]) - len(lines[end].lstrip()) <= indent:
                        break
                    end += 1

            func_source = "\n".join(lines[start:end])
            functions.append((node.name, func_source))

            compressed = compress_def_code(func_source)
            new_lines[start:end] = [compressed]

    modified_code = "\n".join(new_lines)
    return modified_code, functions


def main(argv):
    parser = argparse.ArgumentParser(description="Obfuscate Python code.", formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("input_file", help="The Python file to obfuscate (required)")
    parser.add_argument("-O", "--outfile", metavar="filename", help="Write the obfuscated code to the specified file")
    parser.add_argument("-p", "--print", action="store_true", help="Print the obfuscated code to the screen")
    parser.add_argument("-F", "--flatten", action="store_true", help="Flatten the code (remove newlines)")
    parser.add_argument("-V", "--VERSION", action="version", version=f"Python Obfuscator Version: {VERSION}", help="Show the version of the obfuscator and exit")

    args = parser.parse_args(argv[1:])
    input_file = args.input_file
    output_file = args.outfile
    print_to_screen = args.print
    flatten = args.flatten

    try:
        with open(input_file, "r") as infile:
            code = infile.read()
    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found.")
        sys.exit(2)

    if flatten:
        obfuscated_code = combine_imports(code)
        obfuscated_code = obfuscate_code(obfuscated_code)
        obfuscated_code, funcs = extract_and_compress_functions(obfuscated_code)
    else:
        obfuscated_code = obfuscate_code(code)

    now = datetime.datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")      # Format the date and time as you prefer, e.g., YYYY-MM-DD HH:MM:SS
    obfuscated_code = f"#!/usr/bin/env python3\n# Python Code Obfuscated on {timestamp}:\n{obfuscated_code}"    # Include a newline at the end
 
    if print_to_screen:
        print(f"Obfuscated Code:\n{obfuscated_code}")

    if output_file:
        try:
            with open(output_file, "w") as outfile:
                outfile.write(obfuscated_code)
            print(f"Obfuscated code written to {output_file}")
        except Exception as e:
            print(f"Error writing to output file '{output_file}': {e}")
            sys.exit(1)
    elif not print_to_screen:
        try:
            print(obfuscated_code)
        except Exception as e:
            print(f"Error printing to console: {e}")
            sys.exit(1)
    else:
        print("Not writing to file or printing to screen")

if __name__ == "__main__":
    main(sys.argv)