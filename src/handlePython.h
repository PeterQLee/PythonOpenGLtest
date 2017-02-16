#ifndef HANDLEPYTHON_H
#define HANDLEPYTHON_H
#endif

#ifdef __APPLE__
#include <Python.h>
#elif __linux__
#include <python3.4m/Python.h>
#endif

int updateImage(PyObject *object,int index, unsigned char *rgb,int x, int y, int colsize); 
int saveStack(PyObject *object);
  
