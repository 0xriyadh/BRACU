add:
	git add -A
	git commit -S -m "$(m)"
	git push

flex:
	flex lexAnalyzer.l
	g++ lex.yy.c -o out
	./out input.txt
	cat my_log.txt
