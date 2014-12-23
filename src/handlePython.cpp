#include "handlePython.h"

int updateImage(PyObject *object,int index, unsigned char *rgb,int x,int y,int colsize) {
  printf("wtf?\n");
  PyObject *func ,*args, *list, *item;
  list=PyTuple_New(x*y*colsize);
  int i;
  for (i=0;i<x*y*colsize;i++) {
    //error check
    item=PyLong_FromLong(rgb[i]);
    PyTuple_SetItem(list,i,item);
    }
  Py_DECREF(item);
  args=Py_BuildValue("(i,O)",index,list);
  Py_DECREF(list);
  func=PyObject_GetAttrString(object,"updateImage");
  PyEval_CallObject(func,args);
   Py_DECREF(func);
   PyObject_Print(args,stdout,Py_PRINT_RAW);
    if (args==NULL) printf("yyyy?\n");
   Py_DECREF(args);
  
  printf("way?\n");
  
  
  
  return 0;
}
int saveStack(PyObject *object) {
  
  PyObject *func ,*args;
  args=Py_BuildValue("()");
  func=PyObject_GetAttrString(object,"saveStack");
  printf("??\n");
  PyEval_CallObject(func,args);
  Py_DECREF(args);
  Py_DECREF(func);
  return 0;
}
