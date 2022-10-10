from ply import lex
import ply.yacc as yacc
import logging

# keywords tokens
reserved = {
    'def': 'DEF',
    'var': 'VAR',
    'Int': 'INT',
    'if': 'IF',
    'else': 'ELSE'
}
# List of token names
tokens = [
             'ID',
             'NUM',
             'LPAREN',
             'RPAREN',
             'LBRACE',
             'RBRACE',
             'BECOMES',
             'EQ',
             'NE',
             'LT',
             'GT',
             'LE',
             'GE',
             'PLUS',
             'MINUS',
             'STAR',
             'SLASH',
             'PCT',
             'COMMA',
             'SEMI',
             'COLON',
             'ARROW',
             'COMMENT',
             'WHITESPACE'
         ] + list(reserved.values())  # Adding the keyword tokens

t_ignore_COMMENT = r'\#.*'
t_ignore_WHITESPACE = r'\t|\n|\r|\s'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_EQ = r'\=='
t_BECOMES = r'\='
t_NE = r'\!='
t_LT = r'<'
t_GT = r'>'
t_LE = r'<='
t_GE = r'>='
t_PLUS = r'\+'
t_MINUS = r'-'
t_STAR = r'\*'
t_SLASH = r'/'
t_PCT = r'%'
t_COMMA = r','
t_SEMI = r';'
t_COLON = r':'
t_ARROW = r'=>'


# Rule to track lines numbers


def t_newline(t):
    r"""\n+"""
    t.lexer.lineno += len(t.value)


# String consisting of a single or more digits in the range 0-9


def t_NUM(t):
    r"""\d+"""
    t.value = int(t.value)
    return t


# String consisting of a letter followed by zero or more letters


def t_ID(t):
    r"""[a-zA-Z_][a-zA-Z_0-9]*"""
    t.type = reserved.get(t.value, 'ID')
    return t


# Warning error message


def t_error(t):
    print("Invalid token: " + t.value)
    t.lexer.skip(1)


# Input program to scan


data = '''def f(a:Int, b:Int):Int = { var c:Int;
def g(a:Int, b:(Int)=>Int):Int = { b(a)
}def h(c:Int):Int = {
def g():Int = { c-b 
}
g() }
c = a+b;
g(c,h) }'''
lexer = lex.lex()
lexer.input(data)

precedence = (
    ('nonassoc', 'LT', 'GT'),  # Nonassociative operators
    ('left', 'PLUS', 'MINUS'),
    ('left', 'STAR', 'SLASH'),
)


def p_defdefs(p):
    """defdefs : defdef defdefs
               | defdef"""
    print("defdefs" + list(p).__str__())
    pass


def p_defdef(p):
    """defdef : DEF ID LPAREN parmsopt RPAREN COLON type BECOMES LBRACE vardefsopt defdefsopt expras RBRACE"""
    print("defdef" + list(p).__str__())
    pass


def p_parmsopt(p):
    """parmsopt : parms
                | """
    # print("parmsopt" + list(p).__str__())
    if len(p) != 1:
        p[0] = p[1]
    pass


def p_parms(p):
    """parms : vardef COMMA parms
             | vardef """
    # print("parms" + list(p).__str__())
    p[0] = p[1]
    pass


def p_vardef(p):
    """vardef : ID COLON type"""
    # print("vardef" + list(p).__str__())
    p[0] = p[1]
    pass


def p_type(p):
    """type : INT
            | LPAREN typesopt RPAREN ARROW type"""
    # print("type" + list(p).__str__())
    p[0] = p[1]
    pass


def p_typesopt(p):
    """typesopt : types
                | """
    print("typesopt" + list(p).__str__())
    pass


def p_types(p):
    """types : type COMMA types
             | """

    print("types" + list(p).__str__())
    pass


def p_vardefsopt(p):
    """vardefsopt : VAR vardef SEMI vardefsopt
                  | """
    # print("p_vardefsopt" + list(p).__str__())
    if len(p) != 1:
        p[0] = p[2]
    pass


def p_defdefsopt(p):
    """defdefsopt : defdefs
                  | """
    print("defdefsopt" + list(p).__str__())
    pass


def p_expras(p):
    """expras : expra SEMI expras
                | expra"""
    print("Expras" + list(p).__str__())
    pass


def p_expra(p):
    """expra : expr
             | ID BECOMES expr"""

    print("Expra" + list(p).__str__())
    pass


def p_expr(p):
    """expr : expr PLUS term
            | expr MINUS term
            | term"""
    print("expr" + list(p).__str__())
    if len(p) == 2:
        p[0] = p[1]
    else:
        match p[2]:
            case '+': p[0] = p[1] + p[3]
            case '-': p[0] = p[1] - p[3]
    pass


def p_term(p):
    """term : factor
            | term STAR factor
            | term SLASH factor
            | term PCT factor"""
    # print("term" + list(p).__str__())

    if len(p) == 2:
        p[0] = p[1]
    else:
        match p[2]:
            case '*': p[0] = p[1] * p[3]
            case '/': p[0] = p[1] / p[3]
            case '%': p[0] = p[1] % p[3]


    pass


def p_factor(p):
    """factor : ID
              | NUM
              | LPAREN expr RPAREN
              | factor LPAREN argsopt RPAREN"""
    # print("factor" + list(p).__str__())
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 4:
        p[0] = p[3]


def p_test(p):
    """test : expr NE expr
            | expr LT expr
            | expr LE expr
            | expr GE expr
            | expr GT expr
            | expr EQ expr"""
    print("test" + list(p).__str__())



def p_argsopt(p):
    """argsopt : args
               | """
    print("argsopt" + list(p).__str__())
    pass


def p_args(p):
    """args : expr COMMA args
            | expr"""
    print("args" + list(p).__str__())



def p_error(p):
    print(f"Syntax error {p}")


# Set up a logging object
logging.basicConfig(
    level=logging.DEBUG,
    filename="parse-log.txt",
    filemode="w",
    format="%(filename)10s:%(lineno)4d:%(message)s"
)
log = logging.getLogger()

parser = yacc.yacc(debug=True, debuglog=log)
parser.parse(data, debug=log)
