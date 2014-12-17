CC= g++
BASEDIR := $(abspath $(lastword $(MAKEFILE_LIST)))

SRCDIR= $(BASEDIR)/src

Files=$(wildcard src/*.cpp)
OS := $(shell uname)
BINDIR=bin/

ifeq ($(OS),Darwin)
	LD_Flags := -framework GLUT -framework OpenGL -framework Python
else
	LD_Flags := -lGL -lglut -lpython3.4m

endif
build:
	sudo cp src/instance.py /usr/local/lib/python3.4/dist-packages/
	sudo cp src/tools.py /usr/local/lib/python3.4/dist-packages
	echo $(BASEDIR)
	$(CC) -g $(Files) $(LD_Flags) -o $(BINDIR)main.out