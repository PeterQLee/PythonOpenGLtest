#ifdef __APPLE__
#include <GLUT/glut.h>
#include <Python/Python.h>
#elif __linux__
#include <GL/glut.h>
#include <python3.4m/Python.h>

#endif

void draw() {
  //glClearColor(0.0f,0.0f,0.0f,1.0f);
  glClear(GL_COLOR_BUFFER_BIT);
  //glColor3f(1.0, 1.0, 1.0);
  glBegin(GL_QUADS);
  glColor3f(1.0f,1.0f,0.0f);
  glVertex2f(-0.1f, 0.1f);    // x, y
  glVertex2f( -0.2f, 0.1f);
  glVertex2f( -0.2f,  0.1f);
  glVertex2f(-0.1f,  -0.1f);


  //glBegin(GL_LINES);
  //glVertex3f(0.25, 0.25, 0.0);
  //glVertex3f(0.75, 0.75, 0.0);
  
  glEnd();
  glFlush();
}

void initialize() {
  glClearColor(0.0, 0.0, 0.0, 0.0);
  //glMatrixMode(GL_PROJECTION);
  //glLoadIdentity();
  //gluOrtho2D(-1.0, 1.0, -1.0, 1.0);
  PyRun_SimpleString("print ('hey i work here too')");
}
void dostuff(int argc,char ** argv) {
  glutInit(&argc, argv);
  //glutInitDisplayMode(GLUT_DOUBLE);
  glutInitWindowSize(300, 300);
  glutInitWindowPosition(150, 150);
  glutCreateWindow("Pythontest");
  initialize();
  glutDisplayFunc(draw);
  glutMainLoop();
  
}
int main(int argc, char** argv) {
  Py_Initialize();
  PyRun_SimpleString("print ('done and done')");
  PyRun_SimpleString("import sys");
  PyRun_SimpleString("sys.path.append('/Users/Peter/PythonOpenGLTest/src/')");
  PyObject *module, *modClass, *object, *args,*method,*ret ;
  module=PyImport_ImportModule("instance");
  //check loading
  if (module==NULL) {
    printf("Can't load module\n");
    return -1;
  }
  
  modClass= PyObject_GetAttrString(module, "instance");
  
  Py_DECREF(module);
  if (modClass==NULL) {
    Py_DECREF(modClass);
    printf("can't class instance\n");
    return -1;
  }
  args=Py_BuildValue(" (s)","Saysay.qcard");
  if (args==NULL) {
    Py_DECREF(args);
    printf("can't args instance\n");
    return -1;
  }
  
  object=PyEval_CallObject(modClass,args);
  if (object==NULL) {
    Py_DECREF(object);
    printf("can't object instance\n");
    return -1;
  }
  //error object
  
  Py_DECREF(args);

  method=PyObject_GetAttrString(object, "getPixmap");
  if (method==NULL) {
    Py_DECREF(method);
    printf("can't method instance\n");
    return -1;
  }
  //error method
  
  //Py_DECREF(object);
  args=Py_BuildValue("()");
  if (args==NULL) {
    Py_DECREF(args);
    printf("can't args instance\n");
    return -1;
  }
 
  //error check
  PyObject *pt;
  pt=PyEval_CallObject(method,args);
  Py_DECREF(method);
  PyObject *dict;
  method=PyObject_GetAttrString(object, "getColormap");
  dict=PyEval_CallObject(method,args);
  Py_DECREF(method);
  Py_DECREF(object);
  printf("eyy\n");
  // PyArg_Parse(pt,"O",ret);
  
  
  /* if (!PySequence_Check(ret)){
    printf("string conversion\n");
    return -1;
    }*/

  PyObject *item;
  int *intarr, arrsize, index;

  arrsize=PyObject_Length(pt);
  printf("neh\n");
  intarr= (int *)malloc(sizeof(int)*arrsize);
  
  for (index=0;index<arrsize;index++) {
    item=PySequence_GetItem(pt,index);
    if (!PyInt_Check(item)) {
      free(intarr);
      printf("dne not int messed\n");
      return -1;
    }
    intarr[index] = PyInt_AsLong(item);
  }
  Py_DECREF(pt);

  //do the dict
  PyObject *key, *value;
  Py_ssize_t pos=0;
  Py_ssize_t sd=PyDict_Size(dict);
  char *symbols=(char*)malloc(sizeof(char)*(sd+1));
  char **cols=(char**)malloc(sizeof(char*)*(sd+1)); //Do not know if this is the format used in algorithm
  symbols[0]='t';
  printf("%ld\n",sd);
  int c=0;

  value=PyDict_Values(dict);
  key=PyDict_Keys(dict);
  for (index=0;index<sd;index++) {
    item=PySequence_GetItem(key,index);
    if (!PyString_Check(item)) {
	printf("string done messed\n");
	return -1;
    }
    symbols[index]=PyString_AsString(item)[0];
    item=PySequence_GetItem(value,index);
    if (!PyString_Check(item)) {
      printf("string done messed1\n");
      return -1;
    }
    cols[index]=PyString_AsString(item);
  }
  Py_DECREF(key);
  Py_DECREF(value);
  Py_DECREF(dict);
  /*
  while (PyDict_Next(dict,&pos,&key,&value)) { //memory leak?
    char *d=PyString_AsString(key);
    symbols[pos]=d[0];
   
    d=PyString_AsString(value);
    cols[pos]=d;
    printf("%s %ld\n",cols[pos],pos);
    c++;
    //free(d);
    }*/
  printf("%s\n",cols[1]);
  
  
  dostuff(argc, argv);
  free(cols);
  free(symbols); //freeing individual strings??
  free(intarr);
  Py_Finalize();
  return 0;
}
