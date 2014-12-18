CC= g++
BASEDIR := $(abspath $(lastword $(MAKEFILE_LIST)))

SRCDIR= $(BASEDIR)/src

Files=$(wildcard src/*.cpp)
OS := $(shell uname)
BINDIR=bin/

ifeq ($(OS),Darwin)
	LD_Flags := -I/Library/Frameworks/Python.framework/Versions/3.4/include/python3.4m -L /Library/Frameworks/Python.framework/Versions/3.4/lib/ -framework GLUT -framework OpenGL -lpython3.4m
	#in the future, will make this more dynamic.. using python3.4-config --libs.. etc
else
	LD_Flags := -lGL -lglut -lpython3.4m

endif
build:
	#ifeq ($(OS),Darwin)
	#	echo hi
	#else
	#	sudo cp src/instance.py /usr/local/lib/python3.4/dist-packages/
	#	sudo cp src/tools.py /usr/local/lib/python3.4/dist-packages
	echo $(BASEDIR)
	$(CC) -g $(Files) $(LD_Flags) -o $(BINDIR)main.out