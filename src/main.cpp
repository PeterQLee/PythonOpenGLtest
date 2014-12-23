#ifdef __APPLE__
#include <GLUT/glut.h>
#include <Python.h>
#elif __linux__
#include <GL/glut.h>
#include <python3.4m/Python.h>
#endif
#include <signal.h> //temp
#include "handlePython.h"

GLuint *filePictures; //stores textures of current file, will delete and reset
//when new file is loaded`
int filePicturessize=0;
int pictureIndex;
int curPictureWidth;
int curPictureHeight;
int colorSize=3; //for now, if no alpha

float picturecoords[]={-16.0f,-16.0f,16.0f,-16.0f,16.0f,16.0f,-16.0f,16.0f};
//-150.0f,-150.0f,150.0f,-150.0f,150.0f,150.0f,-150.0f,150.0f};//-150.0f,150.0f,150.0f,150.0f,150.0f,-150.0f,-150.0f,-150.0f}; //will have to be dynamically changed, may make python module responsible for this
unsigned char *rgb;
PyObject *object;
void loadCurrentTextures();//will load texture of current session unused...
void mouseClick(int button, int state, int x, int y);
void mouseMotion(int x, int y);
void reshape(GLsizei width, GLsizei height);
void fKeyboard(unsigned char key, int x, int y);
void drawpicture(int textureindex) { 
  //note this is just a prototype
  //in the future may move this to another file, or class system
  //or something...  
  //error checking for texture and stuff..
  glEnable(GL_TEXTURE_2D);
  glBindTexture(GL_TEXTURE_2D,filePictures[textureindex]);
  glBegin(GL_QUADS);
  glTexCoord2f(0,1); //--,+-,++,-+
  glVertex2f(picturecoords[0],picturecoords[1]);

  glTexCoord2f(1,1);
  glVertex2f(picturecoords[2],picturecoords[3]);

  glTexCoord2f(1,0);
  glVertex2f(picturecoords[4],picturecoords[5]);

  glTexCoord2f(0,0);
  glVertex2f(picturecoords[6],picturecoords[7]);
  glEnd();
  //Map need to be integrated within the glutDisplayFunc or be called by it
  glDisable(GL_TEXTURE_2D);
}
void draw() {
  
  glClear(GL_COLOR_BUFFER_BIT);
  glDisable(GL_DEPTH_TEST);
  //glColor3f(1.0, 1.0, 1.0);
  //drawpicture(0);
  
  glEnable(GL_TEXTURE_2D);
  glBindTexture(GL_TEXTURE_2D,filePictures[0]);
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
  glDisable(GL_TEXTURE_2D);
  glFlush();
}

void initialize() {
  glClearColor(1.00f,0.0f,1.0f,0.0f);
  PyRun_SimpleString("print ('hey i work here too')");
}
void regenTexture() {
  glPixelStorei(GL_UNPACK_ALIGNMENT,4);
  glPixelStorei(GL_PACK_ALIGNMENT, 4); 
  glGenTextures(1,&filePictures[pictureIndex]); //may need change//&[index]
  glBindTexture(GL_TEXTURE_2D,filePictures[pictureIndex]);
  glTexImage2D((GLenum)GL_TEXTURE_2D, 0,GL_RGB , curPictureWidth, curPictureHeight, 0, GL_RGB ,(GLenum)GL_UNSIGNED_BYTE, (GLvoid*)rgb);
  //glTexEnvi( GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE,GL_MODULATE );
  glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT);//clamp
  glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT);
  glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST);//GL_NEAREST
  glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST);
  
//GL_UNISNGED_BYTE
  glBindTexture(GL_TEXTURE_2D,0);
}
void loadImage(int index) { //loads the texture into memory
  //when getting a new image, make sure you free rgb!
  
  if (index>=filePicturessize) {
    filePicturessize++;
    filePictures=(GLuint*)realloc(filePictures,sizeof(GLuint)*filePicturessize);//error checking..
  }
  
  //retrieve data from python module
  PyObject *args, *method, *data, *item, *dim;
  args=Py_BuildValue("(i)",index);
  method=PyObject_GetAttrString(object,"getRGBMap");
  data=PyEval_CallObject(method,args);
  //free up some of that precious, delicious memory
  
  Py_DECREF(method);
  //while we're at it, get the dimensions too
  int x,y;
  method=PyObject_GetAttrString(object,"getDimensions");
  dim=PyEval_CallObject(method,args);
  item=PySequence_GetItem(dim,0);
  if (!PyLong_Check(item)) {
    printf("invalid conversion of dimensionsx!");
    raise(SIGSEGV);
  }
  x=PyLong_AsLong(item);
  Py_DECREF(item);
  item=PySequence_GetItem(dim,1);
  if (!PyLong_Check(item)) {
    printf("invalid conversion of dimensionsy!");
    raise(SIGSEGV);
  }
  y=PyLong_AsLong(item);
  Py_DECREF(item);
  Py_DECREF(dim);
  
  //extract values from list
  //unsigned char *rgb;
  int arrsize, i;

  arrsize=PyObject_Length(data);
  printf("neh\n");
  rgb= (unsigned char *)malloc(sizeof(unsigned char)*arrsize);

  //evaluate and extract list
  for (i=0;i<arrsize;i++) {
    item=PySequence_GetItem(data,i);
    if (!PyLong_Check(item)) { //used to be PyInt
      free(rgb);
      printf("dne not int messed\n");
      raise(SIGSEGV);
    }
    rgb[i] = PyLong_AsLong(item);//As Intfor  mac
    Py_DECREF(item);
  }
  //free up
  Py_DECREF(data);
  printf("%d %d %d %d %d %d %d %d\n",rgb[0],rgb[1],rgb[2],rgb[3],rgb[4],rgb[5],x,y);
  glPixelStorei(GL_UNPACK_ALIGNMENT,4);
  glPixelStorei(GL_PACK_ALIGNMENT, 4); 
  glGenTextures(1,&filePictures[index]); //may need change//&[index]
  glBindTexture(GL_TEXTURE_2D,filePictures[index]);
  glTexImage2D((GLenum)GL_TEXTURE_2D, 0,GL_RGB , x, y, 0, GL_RGB ,(GLenum)GL_UNSIGNED_BYTE, (GLvoid*)rgb);
  //glTexEnvi( GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE,GL_MODULATE );
  glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT);//clamp
  glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT);
  glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST);//GL_NEAREST
  glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST);
  
  glBindTexture(GL_TEXTURE_2D,0);

  //set width and height of picture
  curPictureWidth=x;
  curPictureHeight=y;
  
}
    
void clearImage() {//may need error checking
  free(rgb);
}

void newFrame() {
  PyObject *args, *method;
  args=Py_BuildValue("(i,i)",300,300);
  method=PyObject_GetAttrString(object,"newImage");
  PyEval_CallObject(method,args);
  filePicturessize=1; //arbitrary
  pictureIndex=0;
  filePictures=(GLuint*)malloc(sizeof(GLuint));
}
void dostuff(int argc,char ** argv) {
  glutInit(&argc, argv);
  glutInitWindowPosition(150, 150);
  glutInitWindowSize(300, 300);
  
  glutCreateWindow("Pythontest");
  glutInitDisplayMode(GLUT_DOUBLE);
  glutMouseFunc(mouseClick);
  glutMotionFunc(mouseMotion);
  glutKeyboardFunc(fKeyboard);
  glutDisplayFunc(draw);
  glutReshapeFunc(reshape);
  newFrame();
  initialize();
  
  loadImage(0);
  
 
  //
  glutMainLoop();

}
bool mouseDownFlag=false;
void mouseClick(int button, int state, int x, int y) {
  if (button==GLUT_LEFT_BUTTON && state==GLUT_DOWN) {
    mouseDownFlag=true;
  }
  else if (button==GLUT_LEFT_BUTTON && state==GLUT_UP) {
    mouseDownFlag=false;
  }
}
void mouseMotion(int x, int y) {
  //obviously this is really choppy due to low refresh rate, will implement a draw line function later
  if (x<curPictureWidth && y<curPictureHeight && x>0 && y>0 && mouseDownFlag) {
    //will need to change depending on scaling..

    //changed to image being saved at end of stack to promote speed
    
    /*PyObject *method, *args;
    args=Py_BuildValue("(i,i,i,i,i,i,i)",x,y,0,0,0,0,pictureIndex);
    method=PyObject_GetAttrString(object,"mouseChange");//I should probably do error checking here...
    PyEval_CallObject(method,args);*/

    //will need to scale x and y values according to how stretched
    rgb[y*curPictureWidth*colorSize+x*colorSize]=0;
    rgb[y*curPictureWidth*colorSize+x*colorSize+1]=0;
    rgb[y*curPictureWidth*colorSize+x*colorSize+2]=0;
    //rgb[y][x+3]=0;
     
    //update image...
    //loadImage(pictureIndex);
    regenTexture();
    draw();
  }
}

void killfunction() {
  updateImage(object,pictureIndex,rgb,curPictureWidth,curPictureHeight,colorSize);
  //free(rgb);
  printf("mofo\n");
  saveStack(object);
  
    
}
void fKeyboard(unsigned char key, int x, int y) {
  if (key=='q') {
    killfunction();
  }
}

void reshape(GLsizei width, GLsizei height) {  // GLsizei for non-negative integer
   // Compute aspect ratio of the new window
   if (height == 0) height = 1;                // To prevent divide by 0
   GLfloat aspect = (GLfloat)width / (GLfloat)height;
 
   // Set the viewport to cover the new window
   glViewport(0, 0, width, height);
 
   // Set the aspect ratio of the clipping area to match the viewport
   glMatrixMode(GL_PROJECTION);  // To operate on the Projection matrix
   glLoadIdentity();
   gluOrtho2D(-16.0 , 16.0 , -16.0, 16.0);
  
}

int initializePython() {
  Py_Initialize();
  PyRun_SimpleString("print ('done and done')");
  PyRun_SimpleString("import site");

  PyRun_SimpleString("site.addsitedir('../src/')");
  PyObject *module, *modClass, *args,*method,*ret ;
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
  args=Py_BuildValue(" (s)","Saysay");
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
  return 0;
}


int main(int argc, char** argv) {
  //initalizePython
  if (initializePython()!=0) {
    return -1;
  }
  dostuff(argc, argv);
  printf("EJECT!\n");
  Py_Finalize();

  return 0;
}
