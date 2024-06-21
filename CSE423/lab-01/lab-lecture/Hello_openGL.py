from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *


def draw_points(x, y):
    glPointSize(5) #pixel size. by default 1 thake
    glBegin(GL_POINTS)
    glVertex2f(x,y) #jekhane show korbe pixel
    glEnd()


def iterate():
    glViewport(0, 0, 500, 500)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, 500, 0.0, 500, 0.0, 1.0)
    glMatrixMode (GL_MODELVIEW)
    glLoadIdentity()

def showScreen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    iterate()
    glColor3f(1.0, 1.0, 0.0) #konokichur color set (RGB)
    #call the draw methods here
    draw_points(250, 250)
    glutSwapBuffers()



glutInit() # initialize glut, which is a utility toolkit for OpenGL. It should be called before any other GLUT functions. We need to initialize the GLUT library before setting up the display mode, window size, window position, and creating the window where OpenGL drawings will be rendered.
glutInitDisplayMode(GLUT_RGBA) # set the initial display mode. It can take a number of parameters, but the most common are GLUT_RGB and GLUT_RGBA. GLUT_RGB is the default mode, but GLUT_RGBA is just an enhanced version of GLUT_RGB, where A stands for alpha channel. The alpha channel is used for transparency.
glutInitWindowSize(500, 500) # window size
glutInitWindowPosition(0, 0)
wind = glutCreateWindow(b"OpenGL Coding Practice") #window name
glutDisplayFunc(showScreen)

glutMainLoop()