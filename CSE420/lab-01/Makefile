add:
	git add -A
	git commit -S -m "$(m)"
	git push

flex:
	flex lexAnalyzer.l
	g++ lex.yy.c -o lexAnalyzerExe
	./lexAnalyzerExe input.txt
	cat my_log.txt
