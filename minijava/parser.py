import ipdb

#####################
## Minijava Parser ##
#####################

# Build the lexer
from lexer import MiniJavaLexer
# Build the lexer

vessel = MiniJavaLexer()
vessel.build()
lexer = vessel.lexer
tokens = vessel.tokens
##########
# PARSER #
##########

# dictionary of names
names = { }

precedence = (
    ('left','PLUS','MINUS'),
    ('left','AND', 'LESS_THAN'),
    ('right','NOT'),
    ('left','TIMES')    
)

#By default, in yacc, the first rule found is considered the initial symbol

#BFN>> Goal	::=	MainClass ( ClassDeclaration )* <EOF>
def p_goal(p):
    '''goal : mainclass classdeclaration_star'''
    print("Goal")

#BFN>> MainClass	::=	"class" Identifier "{" "public" "static" "void" "main" "(" "String" "[" "]" Identifier ")" "{" Statement "}" "}"
def p_mainclass(p):
    '''mainclass : CLASS ID LBRACE PUBLIC STATIC VOID MAIN LPAREN STRING LBRACKET RBRACKET ID RPAREN LBRACE statement RBRACE RBRACE
    '''
    #print('MainClass')

def p_classdeclaration_star(p):
	'''classdeclaration_star : classdeclaration_star classdeclaration
							| empty
	'''
	#print('Many Vars declarations')

#BFN>> ClassDeclaration	::=	"class" Identifier ( "extends" Identifier )? "{" ( VarDeclaration )* ( MethodDeclaration )* "}"
def p_classdeclaration(p):
	'''classdeclaration : CLASS ID extends_opt LBRACE vardeclaration_star methoddeclaration_star RBRACE
	'''
	#print('ClassDeclaration')

# def p_class_declaration_body(p):
# 	'''classdecl_body : 
# 	'''
# 	#print('class decl. body')

def p_extends_opt(p):
	'''extends_opt : EXTENDS ID
				| empty
	'''
	#print('Extends '+str(p[1]))

#( Statement )*
def p_statement_star(p):
	'''statement_star : statement_star statement
					| empty
	'''
	#print('Many or empty Statements')

#BFN>> Statement	::=	"{" ( Statement )* "}"
def p_statement_block(p):
	'''statement : LBRACE statement_star RBRACE
	'''
	#print('Statement BLOCK')

#BFN>> Statement	::=	"if" "(" Expression ")" Statement "else" Statement
def p_statement_if(p):
	'''statement : IF LPAREN expression RPAREN statement ELSE statement
	'''
	#print('IF Statement')

#BFN>> Statement	::=	"while" "(" Expression ")" Statement
def p_statement_while(p):
	'''statement : WHILE LPAREN expression RPAREN statement
	'''
	#print('WHILE Statement')
	# while p[1]:		


#BFN>> Statement	::=	"System.out.println" "(" Expression ")" ";"
def p_statement_syso(p):
	'''statement :  SYSTEM_PRINTLN LPAREN expression RPAREN SEMICOLON
	'''
	#print('SYSO'+"; exp:"+str(p[3]))

#BFN>> Statement	::=	Identifier "=" Expression ";"
def p_statement_id_exp(p):
	'''statement : ID LET expression SEMICOLON
	'''
	#print('ID LET Expression')
	# names[p[1],p[3]]

#BFN>> Statement	::=	Identifier "[" Expression "]" "=" Expression ";"
def p_statement_id_array_exp(p):
	'''statement : ID LBRACKET expression RBRACKET LET expression SEMICOLON
	'''
	#print('LET array position statement')

def p_vardeclaration_star(p):
	'''vardeclaration_star : vardeclaration_star vardeclaration
							| empty
	'''
	#print('Many Vars declarations')

#BFN>> VarDeclaration	::=	Type Identifier ";"
def p_vardeclaration(p):
	'''vardeclaration : type ID SEMICOLON
	'''
	#print('Single var declaration')
	#names[p[2],None]

#BFN>> Type	::=	"int" "[" "]"

def p_type_int_array(p):
	'''type : type_array
	'''
	#print('Type: int[]')

def p_type_int_array_(p):
	'''type_array : INT LBRACKET RBRACKET
	'''
	#print('Type: int[]')

#BFN>> Type	::=	boolean
def p_type_boolean(p):
	'''type : BOOLEAN
	'''
	#print('Type: Boolean')

#BFN>> Type	::=	boolean
def p_type_int(p):
	'''type : INT
	'''
	#print('Type: int')

#BFN>> Type	::=	boolean
def p_type_id(p):
	'''type : ID
	'''
	#print('Type: ID')

def p_methoddeclaration_star(p):
	'''methoddeclaration_star : methoddeclaration_star methoddeclaration
							| empty
	'''
	#print('Many methods declarations')

#BFN>> MethodDeclaration	::=	"public" Type Identifier "(" ( Type Identifier ( "," Type Identifier )* )? ")" "{" ( VarDeclaration )* ( Statement )* "return" Expression ";" "}"
def p_methoddeclaration(p):
	'''methoddeclaration : PUBLIC type ID LPAREN args_opt RPAREN LBRACE vardeclaration_star statement_star RETURN expression SEMICOLON RBRACE
	'''
	#print('Single method declaration')

def p_args_opt(p):
	'''args_opt : type ID
				| comma_args 
	'''
	#print("many or single argument")

#( "," Type Identifier )*
def p_comma_args(p):
	'''comma_args : comma_args COMMA type ID
				| empty
	'''
	#print('many arguments')

# Expression	::=	Expression ( "&&" | "<" | "+" | "-" | "*" ) Expression
def p_expression_bin(p):
	'''expression : expression LESS_THAN expression
				| expression AND expression
				| expression PLUS expression
				| expression MINUS expression
				| expression TIMES expression
	'''

	if p[2] == '<' :
		p[0] = p[1] < p[3]
		#print('EXP BIN: <')
	elif p[2] == '&&' :
		p[0] = p[1] and p[3]
		#print('EXP BIN: &&')
	elif p[2] == '+' :
		p[0] = p[1] + p[3]
		#print('EXP BIN: +')
	elif p[2] == '-' :
		p[0] = p[1] - p[3]
		#print('EXP BIN: -')
	elif p[2] == '*' :
		p[0] = p[1] * p[3]	
		#print('EXP BIN: *')


# Expression	::=	Expression "[" Expression "]"
def p_expression_array(p):
	'''expression : expression LBRACKET expression RBRACKET
	'''
	#print('Expression [ Expression ]')
	p[0] = p[1][p[3]]

# Expression	::=	Expression "." "length"
def p_expression_length(p):
	'''expression : expression DOT LENGTH
	'''
	#print('Expression.length')

# Expression	::=	Expression "." Identifier "(" ( Expression ( "," Expression )* )? ")"
def p_expression_params(p):
	'''expression : expression DOT ID LPAREN expressions_opt RPAREN
	'''
	#print('Method calling')


def p_expression_opt(p):
	'''expressions_opt : expression expression_comma
					| empty
	'''
	#print('Methods argument')

def p_expression_comme(p):
	'''expression_comma : expression_comma COMMA expression
						| empty'''
	#print('Many arguments')

# Expression	::=	<INTEGER_LITERAL>
def p_expression_litint(p):
	'''expression : LIT_INT
	'''
	#print('Literal inteiro: '+str(p[1]))
	p[0] = int(p[1]);

# Expression	::=	"true"
def p_expression_true(p):
	'''expression : TRUE
	'''
	#print('Literal BOOLEAN: '+str(p[1]))
	p[0] = True

# Expression	::=	"false"
def p_expression_false(p):
	'''expression : FALSE
	'''
	#print('Literal BOOLEAN: '+str(p[1]))
	p[0] = False

# Expression	::=	Identifier
def p_expression_id(p):
	'''expression : ID
	'''
	#print('Expression: ID: '+str(p[1]))
	# p[0] = names[p[1]]

# Expression	::=	"this"
def p_expression_this(p):
	'''expression : THIS
	'''
	#print('Expression: THIS '+str(p[1]))

# Expression	::=	"new" "int" "[" Expression "]"
def p_expression_new_array(p):
	'''expression : NEW INT LBRACKET expression RBRACKET
	'''
	#print('Expression: NEW ARRAY')
	p[0] = []

# Expression	::=	"new" Identifier "(" ")"
def p_expression_new_instance(p):
	'''expression : NEW ID LPAREN RPAREN
	'''
	#print('Expression: new Instance of :'+ str(p[2]))

# Expression	::=	"(" Expression ")"
def p_expression_paren(p):
	'''expression : LPAREN expression RPAREN
	'''
	#print('(Expression)')
	p[0] = (p[2])

# Expression	::=	"!" Expression
def p_expression_not(p):
	'''expression : NOT expression
	'''
	#print('! Expression')
	p[0] = not p[2]

# def p_id(p):
#     'id : ID'
#     #print('ID :'+str(p[1]))
    # try:
    # 	#print(names[p[1]])
    # except LookupError:
    #     #print("Que tal de '%s' é esse que tás tentando usar?" % p[1])
    #     p[0] = 0



def p_empty(p):
    'empty :'
    #print('EMPTY')
    pass

def p_error(p):
	print("ERROR: >>>>>> Syntax error at '"+str(p)+"'")

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
#    #print(result)

import os

rel_root = '.\inputs_test'

paths = os.listdir(rel_root)

# #print(paths)

# while True:
#     try:
#         s = input('minijavis_môfi> ')   # Use raw_input on Python 2
#     except EOFError:
#         break
#     parser.parse(s)

for path in paths:
	# #print('Analisis of file: '+path)

	# input('>> Press any key to syntax analysis')
	if path.endswith("binarytree.java"):
		with open (rel_root+'\\'+path, "r") as my_file:
			# #print('Do you want to proceed?')
			# #print('Y/n')
			
			file_data = my_file.read().replace(r'\s','')
			result = parser.parse(file_data)
			print("RESULT: "+str(result))
