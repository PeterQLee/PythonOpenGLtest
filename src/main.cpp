#ifdef __APPLE__
#include <GLUT/glut.h>
#include <Python/Python.h>
#elif __linux__
#include <GL/glut.h>
#include <python3.4m/Python.h>

#endif

void draw() {
  glClear(GL_COLOR_BUFFER_BIT);
  glColor3f(1.0, 1.0, 1.0);
  glBegin(GL_LINES);
  glVertex3f(0.25, 0.25, 0.0);
  glVertex3f(0.75, 0.75, 0.0);
  glEnd();
  glFlush();
}

void initialize() {
  glClearColor(0.0, 0.0, 0.0, 0.0);
  glMatrixMode(GL_PROJECTION);
  glLoadIdentity();
  glOrtho(0.0, 1.0, 0.0, 1.0, -1.0, 1.0);
}
void dostuff(int argc,char ** argv) {
  glutInit(&argc, argv);
  glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB);
  glutInitWindowSize(300, 300);
  glutInitWindowPosition(150, 1500);
  glutCreateWindow("Pythontest");
  initialize();
  glutDisplayFunc(draw);
  glutMainLoop();
  
}
int main(int argc, char** argv) {
  dostuff(argc, argv);
  return 0;
}
