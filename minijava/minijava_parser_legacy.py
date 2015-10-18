#####################
## Minijava Parser ##
#####################

# Get the token map from the lexer.  This is required.
#from calclex import tokens
# from minijava_lexer import MiniJavaLexer

reserved = {
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
		'new':'NEW',
		'System.out.println' : 'SYSTEM_PRINTLN'
	}

_tokens = [
	# 'eof',
	'LENGTH',
	'WHITESPACE',
	'BLOCK_COMMENT',
	'LINE_COMMENT',
	'ID',
	'LIT_INT',
	# 'LIT_FLOAT',
	#Bool OPs
	# 'OR',
	'AND',
	# 'EQUAL',	
	# 'DIFFERENT',
	'LESS_THAN',
	# 'LESS_THAN_OR_EQUAL',
	# 'GREATER_THEN',
	# 'GREATER_THEN_OR_EQUAL',
	'NOT',
	#Aritimetic OPs
	'PLUS',
	'MINUS',
	'MULTIPLY',
	# 'DIVIDE',
	# 'MOD',
	#BOUNDARY
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
	] + list(reserved.values())

#The parser input for the variable called 'tokens must be a tuple
tokens = tuple(_tokens)

#- Whitespace: espaços em branco, quebra de linha, tabulação e carriage return;
def t_WHITESPACE(t):
	r'\s'
	pass # No return value. Token discarded

#- Comentários: qualquer texto entre /* e */;
def t_BLOCK_COMMENT(t):
	r'(/\*(.|\n)*?\*/)'
	pass # No return value. Token discarded

# Palavras-chave e operadores: class, public, extends, static, void, int boolean, void, while, if, else, return, ||, &&, ==, !=, <, <=, >, >=, +, -, *, /, %, !, false, true, this, new;
# Described at the begin: reserved

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

  # A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'

def t_LINE_COMMENT(t):
	r'(//.*?)'
	pass # No return value. Token discarded

# def t_BOUNDARY(t):
# 	"BOUNDARY: LPAREN | RPAREN | LBRACE | RBRACE | LBRACKET | RBRACKET"
# 	return t

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

#- Literais ponto flutuante: Uma parte inteira seguida de uma parte fracionária, separada por ponto. Na parte fracionária, podemos incluir um expoente, seguindo os exemplos dos slides de análise léxica.
# def t_LIT_FLOAT(t):
# 	r'\d*\.\d+'
# 	t.value = float(t.value)
# 	return t

	#Comentários e whitespace não tem significado algum, exceto para separar os tokens.
# Error handling rule
def t_error(t):
  print("Illegal character '%s'" % t.value[0])
  t.lexer.skip(1)

# # EOF handling rule
# def t_eof(t):
#     # Get more input (Example)
#     if not t:
#     	return None
#     else:
#     	pass

#Bool OPs
# t_OR = r'\|\|'
t_AND = r'&&'
# t_EQUAL = r'=='
# t_DIFFERENT = r'!='
t_LESS_THAN = r'<'
# t_LESS_THAN_OR_EQUAL = r'<='
# t_GREATER_THEN = r'>'
# t_GREATER_THEN_OR_EQUAL = r'>='
t_NOT = r'!'
#Aritimetic OPs
t_PLUS = r'\+'
t_MINUS = r'-'
t_MULTIPLY = r'\*'
# t_DIVIDE = r'/'
# t_MOD = r'%'

# Build the lexer
import ply.lex as lex
# Build the lexer
lexer = lex.lex()

# dictionary of names
names = { }

# # Give the lexer some input
import os

precedence = (
    ('left','PLUS','MINUS'),
    ('left','MULTIPLY')
)

#Goal	::=	MainClass ( ClassDeclaration )* <EOF>
def p_goal(p):
    '''goal : mainclass classdeclarations'''
    print("Goal")

#MainClass	::=	"class" Identifier "{" "public" "static" "void" "main" "(" "String" "[" "]" Identifier ")" "{" Statement "}" "}"
def p_mainclass(p):
    '''mainclass : CLASS ID LBRACE PUBLIC STATIC VOID MAIN LPAREN STRING LBRACKET RBRACKET ID RPAREN LBRACE statements RBRACE RBRACE'''
    print('MainClass')

#da regra 1 ( ClassDeclaration )*
def p_classdeclarations(p):
	'''classdeclarations : classdeclaration classdeclarations
						| empty'''# depois do ultimo pipeline nao tem nada pois pode ser "nada" também.
	pass

#ClassDeclaration	::=	"class" Identifier ( "extends" Identifier )? "{" ( VarDeclaration )* ( MethodDeclaration )* "}"    
#                                          ### extending ##########
def p_classdeclaration(p):
	'''classdeclaration : CLASS ID extending LBRACE vardeclarations methoddeclarations RBRACE'''
	pass

def p_extending(p):
	'''extending : EXTENDS ID
				| empty
	'''
	pass
	#empty because it's optional


#Da regra de "ClassDeclaration": ( VarDeclaration )*
def p_vardeclarations(p):
	'''vardeclarations : vardeclaration vardeclarations
						| empty
	'''# depois do ultimo pipeline nao tem nada pois pode ser "nada" também.
	pass

#Da regra de "ClassDeclaration": ( MethodDeclaration )*
def p_methoddeclarations(p):
	'''methoddeclarations : methoddeclaration methoddeclarations
						| empty'''# depois do ultimo pipeline nao tem nada pois pode ser "nada" também.
	pass

#MethodDeclaration	::=	"public" Type Identifier "(" ( Type Identifier ( "," Type Identifier )* )? ")" "{" ( VarDeclaration )* ( Statement )* "return" Expression ";" "}"
#                                                                      ######## commaparams ########       #vardeclarations#  #statements#   
#                                                     ############### params ########################
def p_methoddeclaration(p):
	'''methoddeclaration : PUBLIC type ID LPAREN params RPAREN LBRACE vardeclarations statements RETURN  expression SEMICOLON RBRACE
	'''
	pass

def p_params(p):
	'''params : type ID commaparams
	'''
	pass

def p_commaparams(p):
	'''commaparams : COMMA type ID commaparams
				| empty
	'''
	pass

#VarDeclaration	::=	Type Identifier ";"
def p_vardeclaration(p):
	'''vardeclaration : type ID SEMICOLON
	'''
	names[p[2]] = None
	pass

# Type	::=	"int" "[" "]"
# |	"boolean"
# |	"int"
# |	Identifier

def p_type_int_array(p):
	"type : INT LBRACKET RBRACKET"
	# p[0] = []
	pass

def p_type_boolean(p):
	"type : BOOLEAN"
	# p[0] : bool
	pass

def p_type(p):
	'''type : INT
			| ID
	'''
	pass

#Da regra de "MethodDeclaration": ( Statement )*
def p_statements(p):
	'''statements : statement statements
				| empty'''# depois do ultimo pipeline nao tem nada pois pode ser "nada" também.
	pass

# Statement	::=	"{" ( Statement )* "}"
# |	"if" "(" Expression ")" Statement "else" Statement
# |	"while" "(" Expression ")" Statement
# |	"System.out.println" "(" Expression ")" ";"
# |	Identifier "=" Expression ";"
# |	Identifier "[" Expression "]" "=" Expression ";"
def p_statement_braces(p):
	"statement : LBRACE statements RBRACE"
	p[0] = p2

def p_statement_if(p):
	'''statement : IF LPAREN expression RPAREN statement ELSE statement'''
	if p[3]:
		p[0] = p[5]
	else:
		p[0] = p[7]

def p_statement_while(p):
	'''statement : WHILE LPAREN expression RPAREN statement'''
	while p[3]:
		p[5]

def p_statement_syso(p):
	'''statement : SYSTEM_PRINTLN LPAREN expression RPAREN SEMICOLON'''
	print(str(p[3]))

def p_statement_let(p):
	'''statement : ID LET expression SEMICOLON'''
	names[p[1]] = p[3]

def p_statement(p):
	'''statement : ID LBRACKET expression RBRACKET LET expression SEMICOLON
	'''
	names[p[1]][p[3]] = t[6]
	pass

# Expression	::=	Expression ( "&&" | "<" | "+" | "-" | "*" ) Expression
# |	Expression "[" Expression "]"
# |	Expression "." "length"
# |	Expression "." Identifier "(" ( Expression ( "," Expression )* )? ")"
#                                              ## commaexpression ##
#                                  ########## expressions ##########
# |	<INTEGER_LITERAL>
# |	"true"
# |	"false"
# |	Identifier
# |	"this"
# |	"new" "int" "[" Expression "]"
# |	"new" Identifier "(" ")"
# |	"!" Expression
# |	"(" Expression ")"

def p_expression_and(p):
	"expression : expression AND expression"
	p[0] = p[1] and p[2]

def p_expression_less_than(p):
	"expression : expression LESS_THAN expression"
	p[0] = p[1] < p[2]

def p_expression_plus(p):
	"expression : expression PLUS expression"
	p[0] = p[1] + p[2]	

def p_expression_minus(p):
	"expression : expression MINUS expression"
	p[0] = p[1] - p[2]

def p_expression_multiply(p):
	"expression : expression MULTIPLY expression"
	p[0] = p[1] * p[2]

def p_expression_brackets(p):
	"expression : expression LBRACKET expression RBRACKET"
	p[0] = p[1][p[3]]

def p_expression_length(p):
	"expression : expression DOT LENGTH"
	p[0] = len(p[1])

def p_expression_lit(p):
	"expression : LIT_INT"
	p[0] = int(p[1])

def p_expression_true(p):
	"expression : TRUE"
	p[0] = True

def p_expression_false(p):
	'''expression : FALSE
	'''
	p[0] = False

def p_expression_id(p):
	"expression : ID"
	p[0] = names[p[1]]

def p_expression_this(p):
	"expression : THIS"
	#p[0] = self
	pass

def p_expression_not(p):
	"expression : NOT expression"
	p[0] = not (p[1])

def p_expression_new_int_array(p):
	"expression : NEW INT LBRACKET expression RBRACKET"
	p[0] = []

def p_expression_parens(p):
	"expression : LPAREN expression RPAREN"
	p[0] = p[2]

def p_expression(p):
	'''expression : expression DOT ID LPAREN expressions RPAREN
				  | NEW ID LPAREN RPAREN
	'''
	pass

def p_expressions(p):
	'''expressions : expression commaexpression
	'''
	pass

def p_commaexpression(p):
	'''commaexpression : COMMA expression
						| empty
	'''
	pass

def p_empty(p):
    'empty :'
    pass

# Error rule for syntax errors
def p_error(p):
    print("Syntax error in input!"+str(p))

import ply.yacc as yacc
# Build the parser
parser = yacc.yacc()

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

	if path.endswith(".java2"):
		with open (rel_root+'\\'+path, "r") as my_file:
			print('Do you want to proceed?')
			print('Y/n')
			if input() == 'Y' or 'y':
				file_data = my_file.read().replace(r'\s','')

				# mj_lexer.test(data)

				# while True:
				#    try:
				#        s = file_data
				#    except EOFError:
				#        break
				#    if not s: continue

				parser.parse(file_data)
				


##AUX ON AUTOCOMPLETE

# reserved = {
# 		'class':'CLASS',
# 		'String' :'STRING',
# 		'public':'PUBLIC',
# 		'extends':'EXTENDS',
# 		'static': 'STATIC',
# 		'void':'VOID',
# 		'int': 'INT',
# 		'boolean': 'BOOLEAN',
# 		'while':'WHILE',
# 		'if':'IF',
# 		'else':'ELSE',
# 		'return':'RETURN',
# 		'false':'FALSE',
# 		'true': 'TRUE',
# 		'this':'THIS',
# 		'new':'NEW'
# 	}

# 	_tokens = [
# 		'WHITESPACE',
# 		'BLOCK_COMMENT',
# 		'LINE_COMMENT',
# 		'ID',
# 		'LIT_INT',
# 		'LIT_FLOAT',
# 		#Bool OPs
# 		'OR',
# 		'AND',
# 		'EQUAL',	
# 		'DIFFERENT',
# 		'LESS_THAN',
# 		'LESS_THAN_OR_EQUAL',
# 		'GREATER_THEN',
# 		'GREATER_THEN_OR_EQUAL',
# 		'NOT',
# 		#Aritimetic OPs
# 		'PLUS',
# 		'MINUS',
# 		'MULTIPLY',
# 		# 'DIVIDE',
# 		'MOD',
# 		#BOUNDARY
# 		'LPAREN',
# 		'RPAREN',
# 		'LBRACE',
# 		'RBRACE',
# 		'LBRACKET',
# 		'RBRACKET',
# 		'SEMICOLON',
# 		'DOT',
# 		'COMMA',
# 		'LET'
# 		] + list(reserved.values())