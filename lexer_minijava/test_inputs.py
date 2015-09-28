
# # Give the lexer some input
import os
from minijava_lexer import MiniJavaLexer

rel_root = '.\input_test'

paths = os.listdir(rel_root)

# # Build the lexer and try it out
mj_lexer = MiniJavaLexer()
mj_lexer.build()           # Build the lexer

for path in paths:
	print('Analising Lex of file: '+path)

	with open (rel_root+'\\'+path, "r") as myfile:
		data = myfile.read().replace(r'\s','')
		mj_lexer.test(data)

		# Tokenize
		while True:
		    tok = mj_lexer.token()
		    if not tok: 
		        break      # No more input
		    print(tok)

		    input()