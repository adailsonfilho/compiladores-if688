#####################
## Minijava Parser ##
#####################

#########
# LEXER #
#########

reserved = {
		'System':'SYSTEM',
		'class':'CLASS',
		'String' :'STRING',
		'public':'PUBLIC',
		'extends':'EXTENDS',
		'static': 'STATIC',
		'void':'VOID',
		'main':'MAIN',
		'int': 'INT',
		'boolean': 'BOOLEAN',
		'while':'WHILE',
		'if':'IF',
		'else':'ELSE',
		'return':'RETURN',
		'false':'FALSE',
		'true': 'TRUE',
		'this':'THIS',
		'new':'NEW'
	}

_tokens = [
	# 'eof',
	'SYSTEM_PRINTLN',
	'LENGTH',
	'WHITESPACE',
	'BLOCK_COMMENT',
	'LINE_COMMENT',
	'ID',
	'LIT_INT',
	'AND',
	'LESS_THAN',
	'NOT',
	'PLUS',
	'MINUS',
	'TIMES',
	'LPAREN',
	'RPAREN',
	'LBRACE',
	'RBRACE',
	'LBRACKET',
	'RBRACKET',
	'SEMICOLON',
	'DOT',
	'COMMA',
	'LET'
	# 'RAW_STRING'
	] + list(reserved.values())

#The parser input for the variable called 'tokens must be a tuple
tokens = tuple(_tokens)

#- Whitespace: espaços em branco, quebra de linha, tabulação e carriage return;
def t_WHITESPACE(t):
	r'\s'
	pass # No return value. Token discarded

#- Comentários: qualquer texto entre /* e */;
def t_BLOCK_COMMENT(t):
	r'(/\*(.|\n)*\*/)'
	pass # No return value. Token discarded

def t_SYSTEM_PRINTLN(t):
	r'System\.out\.println'
	return t

#- Delimitadores: ; . , = ( ) { } [ ]
t_LENGTH = r'length'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_SEMICOLON = r';'
t_DOT = r'\.'
t_COMMA = r','
t_LET = r'='
# t_RAW_STRING = r'\".\"'

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'

def t_LINE_COMMENT(t):
	r'(//.*)'
	pass # No return value. Token discarded

#- Identificadores: um identificador começa com uma letra ou underline e é seguido por qualquer quantidade de letras, underline e dígitos. Apenas letras entre A/a e Z/z são permitidos, há diferença entre maiúscula e minúscula. Palavras-chave não são identificadores;
def t_ID(t):
	r'[a-zA-Z_][a-zA-Z_0-9]*'
	t.type = reserved.get(t.value,'ID')    # Check for reserved words
	return t

#- Literais Inteiros: uma sequência de dígitos iniciada com qualquer um dos dígitos entre 1 e 9 e seguida por qualquer número de dígitos entre 0 e 9. O dígito 0 também é um inteiro.
def t_LIT_INT(t):
	r'\d+'
	t.value = int(t.value)
	return t

	#Comentários e whitespace não tem significado algum, exceto para separar os tokens.
# Error handling rule
def t_error(t):
  print("Illegal character '%s'" % t.value[0])
  t.lexer.skip(1)

t_AND = r'&&'
t_LESS_THAN = r'<'
t_NOT = r'!'
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'

# Build the lexer
import ply.lex as lex
# Build the lexer
lexer = lex.lex()

##########
# PARSER #
##########

# dictionary of names
names = { }

precedence = (
    ('left','PLUS','MINUS'),
    ('left','TIMES')
)

#BFN>> Goal	::=	MainClass ( ClassDeclaration )* <EOF>
def p_goal(p):
    '''goal : mainclass classdeclaration_star'''
    print("Goal")

#BFN>> MainClass	::=	"class" Identifier "{" "public" "static" "void" "main" "(" "String" "[" "]" Identifier ")" "{" Statement "}" "}"
def p_mainclass(p):
    '''mainclass : CLASS id LBRACE PUBLIC STATIC VOID MAIN LPAREN STRING LBRACKET RBRACKET id RPAREN LBRACE statement RBRACE RBRACE
    '''
    print('MainClass')

def p_classdeclaration_star(p):
	'''classdeclaration_star : classdeclaration_star classdeclaration
							| empty
	'''
	print('Many Vars declarations')

#BFN>> ClassDeclaration	::=	"class" Identifier ( "extends" Identifier )? "{" ( VarDeclaration )* ( MethodDeclaration )* "}"
def p_classdeclaration(p):
	'''classdeclaration : CLASS id extends_opt LBRACE vardeclaration_star methoddeclaration_star RBRACE
	'''
	print('ClassDeclaration')

def p_extends_opt(p):
	'''extends_opt : EXTENDS id
				| empty
	'''
	print('Extends '+str(p[1]))

#( Statement )*
def p_statement_star(p):
	'''statement_star : statement_star statement
					| empty
	'''
	print('Many or empty Statements')

#BFN>> Statement	::=	"{" ( Statement )* "}"
def p_statement_block(p):
	'''statement : LBRACE statement_star RBRACE
	'''
	print('Statement BLOCK')

#BFN>> Statement	::=	"if" "(" Expression ")" Statement "else" Statement
def p_statement_if(p):
	'''statement : IF LPAREN expression RPAREN statement ELSE statement
	'''
	print('IF Statement')

#BFN>> Statement	::=	"while" "(" Expression ")" Statement
def p_statement_while(p):
	'''statement : WHILE LPAREN expression RPAREN statement
	'''
	print('WHILE Statement')

#BFN>> Statement	::=	"System.out.println" "(" Expression ")" ";"
def p_statement_syso(p):
	'''statement :  SYSTEM_PRINTLN LPAREN expression RPAREN SEMICOLON
	'''
	print('SYSO')

#BFN>> Statement	::=	Identifier "=" Expression ";"
def p_statement_id_exp(p):
	'''statement : id LET expression SEMICOLON
	'''
	print('id LET Expression')

#BFN>> Statement	::=	Identifier "[" Expression "]" "=" Expression ";"
def p_statement_id_array_exp(p):
	'''statement : id LBRACKET expression RBRACKET LET expression SEMICOLON
	'''
	print('LET array position statement')

def p_vardeclaration_star(p):
	'''vardeclaration_star : empty
							| vardeclaration_star vardeclaration
	'''
	print('Many Vars declarations')

#BFN>> VarDeclaration	::=	Type Identifier ";"
def p_vardeclaration(p):
	'''vardeclaration : type id SEMICOLON
	'''
	print('Single var declaration')

#BFN>> Type	::=	"int" "[" "]"
def p_type_int_array(p):
	'''type : INT LBRACKET RBRACKET
	'''
	print('Type: int[]')

#BFN>> Type	::=	boolean
def p_type_boolean(p):
	'''type : BOOLEAN
	'''
	print('Type: Boolean')

#BFN>> Type	::=	boolean
def p_type_int(p):
	'''type : INT
	'''
	print('Type: int')

#BFN>> Type	::=	boolean
def p_type_id(p):
	'''type : id
	'''
	print('Type: id')

def p_methoddeclaration_star(p):
	'''methoddeclaration_star : methoddeclaration_star methoddeclaration
							| empty
	'''
	print('Many methods declarations')

#BFN>> MethodDeclaration	::=	"public" Type Identifier "(" ( Type Identifier ( "," Type Identifier )* )? ")" "{" ( VarDeclaration )* ( Statement )* "return" Expression ";" "}"
def p_methoddeclaration(p):
	'''methoddeclaration : PUBLIC type id LPAREN type id params_opt RPAREN LBRACE methodbody RETURN expression SEMICOLON RBRACE
	'''
	print('Single method declaration')
	
def p_method_body(p):
	'''methodbody : vardeclaration_star statement_star
	'''
#( "," Type Identifier )*
def p_params_opt(p):
	'''params_opt : COMMA type id params_opt
				| empty
	'''
	print('optional parameters')

# Expression	::=	Expression ( "&&" | "<" | "+" | "-" | "*" ) Expression
def p_expression_bin(p):
	'''expression : expression AND expression
				| expression LESS_THAN expression
				| expression PLUS expression
				| expression MINUS expression
				| expression TIMES expression
	'''
	print('Expression bin')

# Expression	::=	Expression "[" Expression "]"
def p_expression_array(p):
	'''expression : expression LBRACKET expression RBRACKET
	'''
	print('Expression [ Expression ]')

# Expression	::=	Expression "." "length"
def p_expression_length(p):
	'''expression : expression DOT LENGTH
	'''
	print('Expression.length')

# Expression	::=	Expression "." Identifier "(" ( Expression ( "," Expression )* )? ")"
def p_expression_params(p):
	'''expression : expression DOT id LPAREN expression expression_opt RPAREN
	'''
	print('Method calling')

def p_expression_opt(p):
	'''expression_opt : COMMA expression expression_opt
					| empty
	'''
	print('Methods parameters')

# Expression	::=	<INTEGER_LITERAL>
def p_expression_litint(p):
	'''expression : LIT_INT
	'''
	print('Literal inteiro: '+str(p[1]))

# Expression	::=	"true"
def p_expression_true(p):
	'''expression : TRUE
	'''
	print('Literal BOOLEAN: '+str(p[1]))

# Expression	::=	"false"
def p_expression_false(p):
	'''expression : FALSE
	'''
	print('Literal BOOLEAN: '+str(p[1]))

# Expression	::=	Identifier
def p_expression_id(p):
	'''expression : id
	'''
	print('Expression: id: '+str(p[1]))

# Expression	::=	"this"
def p_expression_this(p):
	'''expression : THIS
	'''
	print('Expression: THIS')

# Expression	::=	"new" "int" "[" Expression "]"
def p_expression_new_array(p):
	'''expression : NEW INT LBRACKET expression RBRACKET
	'''
	print('Expression: NEW ARRAY')

# Expression	::=	"new" Identifier "(" ")"
def p_expression_new_instance(p):
	'''expression : NEW id LPAREN RPAREN
	'''
	print('Expression: new Instance of :'+ str(p[2]))

# Expression	::=	"!" Expression
def p_expression_not(p):
	'''expression : NOT expression
	'''
	print('! Expression')

# Expression	::=	"(" Expression ")"
def p_expression_paren(p):
	'''expression : LPAREN expression RPAREN
	'''
	print('(Expression)')

def p_id(p):
    'id : ID'
    print('ID :'+str(p[1]))
    # try:
    # 	print(names[p[1]])
    # except LookupError:
    #     print("Que tal de '%s' é esse que tás tentando usar?" % p[1])
    #     p[0] = 0

def p_empty(p):
    'empty :'
    print('EMPTY')
    pass

def p_error(p):
	print("Syntax error at '"+str(p)+"'")

import ply.yacc as yacc
# Build the parser
parser = yacc.yacc()

# while True:
#    try:
#        s = raw_input('calc > ')
#    except EOFError:
#        break
#    if not s: continue
#    result = parser.parse(s)
#    print(result)

import os

rel_root = '.\inputs_test'

paths = os.listdir(rel_root)

# print(paths)

# while True:
#     try:
#         s = input('minijavis_môfi> ')   # Use raw_input on Python 2
#     except EOFError:
#         break
#     parser.parse(s)

for path in paths:
	print('Analisis of file: '+path)

	input('>> Press any key to syntax analysis')
	# if path.endswith("2.java"):
	with open (rel_root+'\\'+path, "r") as my_file:
		# print('Do you want to proceed?')
		# print('Y/n')
		
		file_data = my_file.read().replace(r'\s','')
		result = parser.parse(file_data)
		print(result)
