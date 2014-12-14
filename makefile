CC= g++
BASEDIR := $(abspath $(lastword $(MAKEFILE_LIST)))

SRCDIR= $(BASEDIR)/src
Files=$(wildcard $(SRCDIR)/*.cpp)
OS := $(shell uname)
BINDIR=bin/

ifeq ($(OS),Darwin)
	LD_FLAGS := -framework GLUT -framework OpenGL
else
	LD_Flags := -lGL -lglut -lpython3.4m
endif
build:
	$(CC) $(FILES) $(LD_Flags) -o $(BINDIR)main.out