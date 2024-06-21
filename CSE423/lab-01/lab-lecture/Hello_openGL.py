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
    # Clears the color and depth buffers. This means that the content of the window is cleared and ready for new drawing commands.
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    
    # Resets the current matrix. In OpenGL, transformations (like translations, rotations, scaling) are applied to the current matrix. 
    # glLoadIdentity replaces the current matrix with the identity matrix, effectively "resetting" any transformations that have been applied so far.
    glLoadIdentity()
    
    # Calls the iterate function. This function is not defined here, but typically, it would set up or update parameters for the drawing, 
    # such as setting up viewing transformations or preparing dynamic data for rendering.
    iterate()
    
    # Sets the current color to yellow (RGB: 1.0, 1.0, 0.0). All subsequent drawing operations will use this color until it's changed again.
    glColor3f(1.0, 1.0, 0.0)
    
    # This is a placeholder comment indicating where drawing functions should be called. 
    # Based on the comment, draw_points(250, 250) is called here to draw something at the specified coordinates.
    # The specifics of draw_points are not shown, but it likely involves OpenGL commands to draw points or other primitives.
    draw_points(250, 250)
    
    # Swaps the front and back buffers. In double-buffered rendering, drawing commands are applied to a back buffer while the front buffer is being displayed.
    # Swapping them makes the newly drawn frame visible, providing smooth animation and avoiding flicker.
    glutSwapBuffers()



glutInit() # initialize glut, which is a utility toolkit for OpenGL. It should be called before any other GLUT functions. We need to initialize the GLUT library before setting up the display mode, window size, window position, and creating the window where OpenGL drawings will be rendered.
glutInitDisplayMode(GLUT_RGBA) # set the initial display mode. It can take a number of parameters, but the most common are GLUT_RGB and GLUT_RGBA. GLUT_RGB is the default mode, but GLUT_RGBA is just an enhanced version of GLUT_RGB, where A stands for alpha channel. The alpha channel is used for transparency.
glutInitWindowSize(500, 500) # window size
glutInitWindowPosition(0, 0) # window position
'''
    glutCreateWindow: This function is called to create a window. It takes a single argument, which is the title of the window. The window title is specified as a byte string (hence the b prefix before the string literal), which is a requirement in Python 3 when interfacing with certain libraries that expect ASCII strings instead of the default Unicode strings.

    b"OpenGL Coding Practice": This is the title of the window, specified as a byte string. The b prefix indicates that what follows is a byte string, not a regular string. This is important for compatibility with the C-based libraries that GLUT wraps around, which expect strings in ASCII encoding.

    wind =: The result of glutCreateWindow (which is the window ID, a unique identifier for the created window) is assigned to the variable wind. This window ID can be used in subsequent calls to GLUT functions that require a reference to the window, although in many simple GLUT applications, this step is not strictly necessary since GLUT manages the current window implicitly.
'''
wind = glutCreateWindow(b"OpenGL Coding Practice") # this line creates a new window with the title "OpenGL Coding Practice" and assigns its window ID to the variable "wind".
glutDisplayFunc(showScreen)

glutMainLoop()