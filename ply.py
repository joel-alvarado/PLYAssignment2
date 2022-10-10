from ply import lex
import ply.yacc as yacc
import logging

# data = input("File name (ex. foo.txt): ")
# lines = ''
# with open(data) as text:
#     for line in text:
#         lines += line

data = """def f(a:Int, b:Int):Int = { var c:Int;
def g(a:Int, b:(Int)=>Int):Int = { b(a)
} def h(c:Int):Int = {
def g():Int = { c-b
}
g() }
c = a+b;
g(c,h) }"""

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


# Parser


def p_defdefs(p):
    """defdefs : defdef defdefs
               | defdef"""
    pass


def p_defdef(p):
    """defdef : DEF ID LPAREN parmsopt RPAREN COLON type BECOMES LBRACE vardefsopt defdefsopt expras RBRACE"""
    pass


def p_parmsopt(p):
    """parmsopt : parms
                | """
    pass


def p_parms(p):
    """parms : vardef COMMA parms
             | vardef"""
    pass


def p_vardef(p):
    """vardef : ID COLON type"""
    pass


def p_type(p):
    """type : INT
            | LPAREN typesopt RPAREN ARROW type"""
    pass


def p_typesopt(p):
    """typesopt : types
                | """
    pass


def p_types(p):
    """types : type COMMA types
             | """
    pass


def p_vardefsopt(p):
    """vardefsopt : VAR vardef SEMI vardefsopt
                  | """
    pass


def p_defdefsopt(p):
    """defdefsopt : defdefs
                  | """
    pass


def p_expras(p):
    """expras : expra SEMI expras
                | expra"""
    pass


def p_expra(p):
    """expra : ID BECOMES expr
             | expr"""
    pass


def p_expr(p):
    """expr : IF LPAREN test RPAREN LBRACE expras RBRACE ELSE LBRACE expras RBRACE
            | term
            | expr PLUS term
            | expr MINUS term"""
    pass


def p_term(p):
    """term : factor
            | term STAR factor
            | term SLASH factor
            | term PCT factor"""
    pass


def p_factor(p):
    """factor : ID
              | NUM
              | LPAREN expr RPAREN
              | factor LPAREN argsopt RPAREN"""
    pass


def p_test(p):
    """test : expr NE expr
            | expr LT expr
            | expr LE expr
            | expr GE expr
            | expr GT expr
            | expr EQ expr"""
    pass


def p_argsopt(p):
    """argsopt : args
               | """
    pass


def p_args(p):
    """args : expr COMMA args
            | expr"""
    pass


def p_error(p):
    if p:
         print("Syntax error at token", p.type)
         # Just discard the token and tell the parser it's okay.
         parser.errok()
    else:
         print("Syntax error at EOF")


logging.basicConfig(
    level=logging.DEBUG,
    filename="parse-log.txt",
    filemode="w",
    format="%(filename)10s:%(lineno)4d:%(message)s"
)
log = logging.getLogger()

lexer = lex.lex()
lexer.input(data)

parser = yacc.yacc(debug=True, debuglog=log)
parser.parse(data, debug=log)
