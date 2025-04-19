from enum import Enum
from os import system

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
            return f"({self.type.name})"
        
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
    i = 0

    while i < len(tokens):
        token = tokens[i]

        if token.type == TokenType.START_BLOCK:
            depth = 1
            block_start = i
            i += 1
            while i < len(tokens) and depth > 0:
                if tokens[i].type == TokenType.START_BLOCK:
                    depth += 1
                elif tokens[i].type == TokenType.END_BLOCK:
                    depth -= 1
                i += 1
            block_end = i - 1
            out.data.append(make_tree(tokens[block_start + 1:block_end], TokenType.BLOCK))
            continue

        elif token.type == TokenType.START_LIST:
            depth = 1
            list_start = i
            i += 1
            while i < len(tokens) and depth > 0:
                if tokens[i].type == TokenType.START_LIST:
                    depth += 1
                elif tokens[i].type == TokenType.END_LIST:
                    depth -= 1
                i += 1
            list_end = i - 1
            out.data.append(make_tree(tokens[list_start + 1:list_end], TokenType.LIST))
            continue

        else:
            out.data.append(token)
            i += 1

    return out

def parse_streams(program: Token, base=True) -> Token:
    this_level = []

    for token in program.data:
        if isinstance(token.data, list):
            if token.type == TokenType.LIST:
                this_level.append(Token(TokenType.LIST, parse_streams(token, False)))
            
            elif token.type == TokenType.BLOCK:
                this_level.append(Token(TokenType.BLOCK, parse_streams(token, False)))
        else:
            this_level.append(token)
    
    

    if base:
        return Token(TokenType.PROGRAM, this_level)
    else:
        return this_level

def print_ast(t: Token, depth=0):
    print(depth * "\t" + str(t))

    if isinstance(t.data, list):
        for node in t.data:
            print_ast(node, depth+1)

def main():
    with open("main.garbage", "r") as f:
        code = f.read() + "\n"

    code = remove_comments(code)
    code = tokenize(code)
    code = collect_strings(code)
    code = remove_sep(code)
    code = collect_identifiers(code)
    code = make_tree(code)

    system("clear")
    code = parse_streams(code)
    print_ast(code)

if __name__ == "__main__":
    main()