from enum import Enum
from pprint import pprint

class TokenType(Enum):
    IDK = 0

    SEMICOLON = 1

    STRING = 2
    FLOAT = 3
    INT = 4

    IDENTIFIER = 5
    KEYWORD = 6

    START_BLOCK = 7
    END_BLOCK = 8
    START_LIST = 9
    END_LIST = 10

    DOT = 11
    STREAM = 12

    SEP = 13

    NEG = 14
    COMMA = 15

    LIST = 16
    BLOCK = 17
    PROGRAM = 18

token_map_1 = {
    ";": TokenType.SEMICOLON,
    "[": TokenType.START_LIST,
    "]": TokenType.END_LIST,
    "{": TokenType.START_BLOCK,
    "}": TokenType.END_BLOCK,
    ".": TokenType.DOT,
    "-": TokenType.NEG,
    " ": TokenType.SEP,
    "\n": TokenType.SEP,
    "\t": TokenType.SEP,
    ",": TokenType.COMMA,
}

token_map_2 = {
    ">>": TokenType.STREAM
}

type GenericDataType = int | float | str | list

class Token:
    def __init__(self, type: TokenType, data: GenericDataType):
        self.type = type
        self.data = data
    
    def __str__(self):
        if type(self.data) is list:
            return f"({self.type.name} [LIST])"
        
        return f"({self.type.name} '{self.data if self.data != '\n' else '\\n'}')"

def remove_comments(data: str) -> str:
    mid = ""
    out = ""

    ignore = False
    p = 0
    l = len(data)

    while p < l:
        if data[p] == "#":
            ignore = True
        
        elif data[p] == "\n":
            ignore = False
        
        if not ignore:
            mid += data[p]
        
        p += 1


    ignore = False
    p = -1
    l = len(mid)

    while p < l:
        if mid[p:p+2] == "/*":
            p += 2
            while p < l and mid[p:p+2] != "*/":
                p += 1
            p += 2  # skip the closing */
        else:
            out += mid[p]
            p += 1

    if ignore:
        raise SyntaxError("Didn't close comment.")
    
    return out

def tokenize(data: str) -> list[Token]:
    out: list[Token] = []

    p = 0
    l = len(data)

    while p < l:
        c = data[p]
        cc = data[p:p+2]

        if cc in token_map_2:
            out.append(Token(token_map_2[cc], cc))
            p += 2
        elif c in token_map_1:
            out.append(Token(token_map_1[c], c))
            p += 1
        else:
            out.append(Token(TokenType.IDK, c))
            p += 1

    return out

def collect_strings(tokens: list[Token]) -> list[Token]:
    out: list[Token] = []

    tmp_str = ""
    in_str = False

    for token in tokens:
      # t = token.type # ignored
        c = token.data


        if c == '"':
            if in_str:
                out.append(Token(TokenType.STRING, tmp_str))
                tmp_str = ""
                in_str = False
            else:
                in_str = True
        else:
            if in_str:
                tmp_str += c
            else:
                out.append(token)
    
    return out

def remove_sep(tokens: list[Token]) -> list[Token]:
    return [token for token in tokens if token.type != TokenType.SEP]

def collect_identifiers(tokens: list[Token]) -> list[Token]:

    out: list[Token] = []

    id = ""
    for token in tokens:
        if token.type != TokenType.IDK:
            if id != "":
                out.append(Token(TokenType.IDENTIFIER, id))
                id = ""
                
            out.append(token)
        else:
            id += token.data
    
    return out

def make_tree(tokens: list[Token], t=TokenType.PROGRAM) -> Token:
    out = Token(t, [])

    block_start = None
    block_end = None
    block_depth = 0

    list_start = None
    list_end = None
    list_depth = 0

    for i, token in enumerate(tokens):
        if token.type == TokenType.START_BLOCK:
            block_depth += 1
            if block_depth == 1:
                block_start = i

        elif token.type == TokenType.END_BLOCK:
            block_depth -= 1
            if block_depth == 0:
                block_end = i
                out.data.append(make_tree(tokens[block_start+1:block_end], TokenType.BLOCK))
                continue
        
        elif token.type == TokenType.START_LIST:
            list_depth += 1
            if list_depth == 1:
                list_start = i

        elif token.type == TokenType.END_LIST:
            list_depth -= 1
            if list_depth == 0:
                list_end = i
                out.data.append(make_tree(tokens[list_start+1:list_end], TokenType.LIST))
                continue
        
        if list_depth == 0 and block_depth == 0:
            out.data.append(token)
    
    return out

def printl(l: list):
    for item in l:
        print(item)

def print_ast(t: Token, depth=0):
    print(depth * "\t" + str(t))

    if type(t.data) is list:
        for node in t.data:
            print_ast(node, depth+1)

with open("main.garbage", "r") as f:
    code = f.read() + "\n"

def main():
    global code
    print("Source code:")
    print(code)

    code = remove_comments(code)
    print("\nremove_comments:")
    print(code)

    code = tokenize(code)
    print("\ntokenize:")
    printl(code)

    code = collect_strings(code)
    print("\ncollect_strings:")
    printl(code)

    code = remove_sep(code)
    print("\nremove_sep:")
    printl(code)

    code = collect_identifiers(code)
    print("\ncollect_identifiers:")
    printl(code)

    code = make_tree(code)
    print("\nmake_tree:")
    print_ast(code)

if __name__ == "__main__":
    main()