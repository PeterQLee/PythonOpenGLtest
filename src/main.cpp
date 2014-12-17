#ifdef __APPLE__
#include <GLUT/glut.h>
#include <Python/Python.h>
#elif __linux__
#include <GL/glut.h>
#include <python3.4m/Python.h>
#include <signal.h> //temp
#endif

GLuint *filePictures; //stores textures of current file, will delete and reset
//when new file is loaded`
int filePicturessize=0;

float picturecoords[]={0.0f,0.0f,0.0f,0.0f,0.0f,0.0f,0.0f,0.0f}; //will have to be dynamically changed, may make python module responsible for this

void loadCurrentTextures();//will load texture of current session

void drawpicture(int *RGBAData, int x, int y, int textureindex) { 
  //note this is just a prototype
  //in the future may move this to another file, or class system
  //or something...
  
  //might need to call glEnable(GL_TEXTURE_2D)

  //check if filePictures is already allocated to textureindex
  /*
    //Never mind, will assume it is already loaded
  if (textureindex>=filePicturesize) {
    filePicturessize++;
    filePictures=(*GLuint)realloc(sizeof(GLuint)*filePicturessize);
    glPixelStorei(GL_UNPACK_ALIGNMENT, 4);
    glPixelStorei(GL_PACK_ALIGNMENT, 4); //not sure where to put this...
    glGenTextures(1,&filePictures[textureindex]); //may need change
    
    glTexImage2D((GLenum)GL_TEXTURE_2D, 0, GL_RGBA, x, y, 0, GL_RGBA,(GLenum)GL_UNSIGNED_BYTE, (GLvoid*)RGBAData);
     glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT);//clamp
     glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT);
     glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST);//GL_NEAREST
     glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST); //copied from file
     
     
    //set @ index to zero
    //createtexture
    }  */
    
  //error checking for texture and stuff..
  glBindTexture(GL_TEXTURE_2D,filePictures[textureindex]);
  glBegin(GL_QUADS);
  glTexCoord2f(0,1);
  glVertex2f(picturecoords[0],picturecoords[1]);

  glTexCoord2f(1,1);
  glVertex2f(picturecoords[2],picturecoords[3]);

  glTexCoord2f(1,0);
  glVertex2f(picturecoords[4],picturecoords[5]);

  glTexCoord2f(0,0);
  glVertex2f(picturecoords[6],picturecoords[7]);
  glEnd();
  //Map need to be integrated within the glutDisplayFunc or be called by it
}
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
  //PyRun_SimpleString("sys.path.append('/Users/Peter/PythonOpenGLtest/src/')");
  PyRun_SimpleString("sys.path.append('home/peter/PythonOpenGLtest/src/')");//linux
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
  Py_DECREF(modClass);
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
  //Py_DECREF(args);
  //error check
  PyObject *pt;
  pt=PyEval_CallObject(method,args);
  Py_DECREF(method);
  PyObject *dict;
  method=PyObject_GetAttrString(object, "getColormap");
  dict=PyEval_CallObject(method,args);
  Py_DECREF(method);
  Py_DECREF(object);
  Py_DECREF(args);
  printf("eyy\n");
  // PyArg_Parse(pt,"O",ret);
  
  
  /* if (!PySequence_Check(ret)){
    printf("string conversion\n");
    return -1;
    }*/

  PyObject *item;
  int *intarr;
  int arrsize, index;

  arrsize=PyObject_Length(pt);
  printf("neh\n");
  intarr= (int *)malloc(sizeof(int)*arrsize);
  
  for (index=0;index<arrsize;index++) {
    item=PySequence_GetItem(pt,index);
    if (!PyLong_Check(item)) { //used to be PyInt
      free(intarr);
      printf("dne not int messed\n");
      return -1;
    }
    intarr[index] = PyLong_AsLong(item);//As Intfor  mac
    Py_DECREF(item);
  }
  Py_DECREF(pt);

  //do the dict
  PyObject *key, *value;
  Py_ssize_t pos=0;
  Py_ssize_t sd=PyDict_Size(dict);
  char *symbols=(char*)malloc(sizeof(char)*(sd));
  char **cols=(char**)malloc(sizeof(char*)*(sd)); //Do not know if this is the format used in algorithm
  //symbols[0]='t';
  printf("%ld\n",sd);
  int c=0;
  PyObject *dumb;
  PyObject *dumb2;
  value=PyDict_Values(dict);
  key=PyDict_Keys(dict);
  PyObject *item3;
  PyObject *item2;
  int i;
  for (i=0;i<sd;i++) {
    item3=PyList_GetItem(value,i); //change to PYLIst?
    if (!PyUnicode_Check(item3)) { //PyString
	printf("string done messed\n");
	return -1;
    }
   
    //symbols[index];
    //dumb=PyUnicode_AsASCIIString(item3);//PyString_AsString(item)[0];
    cols[i]=PyUnicode_AsUTF8(item3);//=PyByteArray_AsString(dumb);
    Py_DECREF(item3);
    //Py_DECREF(dumb); //segfault?
    item2=PyList_GetItem(key,i); //changed frmo squence to list
    if (!PyUnicode_Check(item2)) {//pystring
      printf("string done messed1\n");
      return -1;
    }
    //PyObject* dumb2;
    symbols[i]=PyUnicode_AsUTF8(item2)[0];
    //cols[index]=PyByteArray_AsString(dumb2);
    //try decrefing items
    Py_DECREF(item2);
    //Py_DECREF(dumb2);
    /*SUPER NOTE, HUGE MEMORY ISSUES HERE, fix*/
  }
  //Py_DECREF(key);
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

  //right here!
  printf("%s\n",cols[1]);
  
  //raise(SIGSEGV);
  dostuff(argc, argv);
  free(cols);
  free(symbols); //freeing individual strings??
  
  free(intarr);
  Py_Finalize();
  return 0;
}
