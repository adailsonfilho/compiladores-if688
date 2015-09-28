#***************************************
#** Elementos Léxicos de MiniJava **
#***************************************

import ply.lex as lex

class MiniJavaLexer(object):

	reserved = {
		'class':'CLASS',
		'public':'PUBLIC',
		'extends':'EXTENDS',
		'static': 'STATIC',
		'void':'VOID',
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

	tokens = [
		'WHITESPACE',
		'BLOCK_COMMENT',
		'LINE_COMMENT',
		'ID',
		'LIT_INT',
		'LIT_FLOAT',
		#Bool OPs
		'OR',
		'AND',
		'EQUAL',	
		'DIFFERENT',
		'LESS_THAN',
		'LESS_THAN_OR_EQUAL',
		'GREATER_THEN',
		'GREATER_THEN_OR_EQUAL',
		'NOT',
		#Aritimetic OPs
		'PLUS',
		'MINUS',
		'MULTIPLY',
		'DIVIDE',
		'MOD',
		#BOUNDARY
		'BOUNDARY',
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
		]+ list(reserved.values())

	#- Whitespace: espaços em branco, quebra de linha, tabulação e carriage return;
	def t_WHITESPACE(self,t):
		r'\s'
		pass # No return value. Token discarded

	#- Comentários: qualquer texto entre /* e */;
	def t_BLOCK_COMMENT(self, t):
		r'(/\*(.|\n)*?\*/)'
		pass # No return value. Token discarded

	# Palavras-chave e operadores: class, public, extends, static, void, int boolean, void, while, if, else, return, ||, &&, ==, !=, <, <=, >, >=, +, -, *, /, %, !, false, true, this, new;
	# Described at the begin: reserved

	#- Delimitadores: ; . , = ( ) { } [ ]
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

	def t_LINE_COMMENT(self, t):
		r'(//.*?)'
		pass # No return value. Token discarded

	def t_BOUNDARY(self, t):
		"BOUNDARY: LPAREN | RPAREN | LBRACE | RBRACE | LBRACKET | RBRACKET"
		return t

	#- Identificadores: um identificador começa com uma letra ou underline e é seguido por qualquer quantidade de letras, underline e dígitos. Apenas letras entre A/a e Z/z são permitidos, há diferença entre maiúscula e minúscula. Palavras-chave não são identificadores;
	def t_ID(self, t):
		r'[a-zA-Z_][a-zA-Z_0-9]*'
		t.type = self.reserved.get(t.value,'ID')    # Check for reserved words
		return t

	#- Literais Inteiros: uma sequência de dígitos iniciada com qualquer um dos dígitos entre 1 e 9 e seguida por qualquer número de dígitos entre 0 e 9. O dígito 0 também é um inteiro.
	def t_LIT_INT(self, t):
		r'\d+'
		t.value = int(t.value)
		return t

	#- Literais ponto flutuante: Uma parte inteira seguida de uma parte fracionária, separada por ponto. Na parte fracionária, podemos incluir um expoente, seguindo os exemplos dos slides de análise léxica.
	def t_LIT_FLOAT(self, t):
		r'\d*\.\d+'
		t.value = float(t.value)
		return t

		#Comentários e whitespace não tem significado algum, exceto para separar os tokens.
	# Error handling rule
	def t_error(self, t):
	  print("Illegal character '%s'" % t.value[0])
	  t.lexer.skip(1)

	#Bool OPs
	t_OR = r'\|\|'
	t_AND = r'&&'
	t_EQUAL = r'=='
	t_DIFFERENT = r'!='
	t_LESS_THAN = r'<'
	t_LESS_THAN_OR_EQUAL = r'<='
	t_GREATER_THEN = r'>'
	t_GREATER_THEN_OR_EQUAL = r'>='
	t_NOT = r'!'
	#Aritimetic OPs
	t_PLUS = r'\+'
	t_MINUS = r'-'
	t_MULTIPLY = r'\*'
	t_DIVIDE = r'/'
	t_MOD = r'%'

	## TEST WITH INPUTS ##
	# Build the lexer

	def build(self,**kwargs):
		self.lexer = lex.lex(module=self,**kwargs)
	
	# Test it output
	def test(self,data):
		self.lexer.input(data)
		while True:
			 tok = self.lexer.token()
			 if not tok: 
				 break
			 print(tok)

	def token(self):
		return self.lexer.token()



##HOW USE IT OUTHERE:
# # Build the lexer and try it out
# m = MiniJavaLexer()
# m.build()           # Build the lexer
# m.test("3 + 4")     # Test it
# m.token     		  # itarat over the tokens readed
