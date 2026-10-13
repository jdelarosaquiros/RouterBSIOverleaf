# Use a complete system TeX installation when one is available.
ifneq ($(wildcard /usr/bin/latexmk),)
export PATH := /usr/bin:/bin:$(PATH)
endif
LATEXMK ?= latexmk
FLAGS := -pdf -interaction=nonstopmode -halt-on-error -file-line-error
.DEFAULT_GOAL := build
.PHONY: build rebuild watch clean

build:
	$(LATEXMK) $(FLAGS) main.tex

rebuild:
	$(LATEXMK) -g $(FLAGS) main.tex

watch:
	$(LATEXMK) $(FLAGS) -pvc main.tex

clean:
	$(LATEXMK) -C main.tex
	rm -f main.bbl main.run.xml main.synctex.gz
