from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *


def draw_points(x, y):
    glPointSize(20)  # pixel size. default value 1
    """  
        glBegin(GL_POINTS): This function specifies how to draw one or more points.

        - GL_POINTS: This is a drawing mode that tells OpenGL to draw individual points. Each point is drawn as a single pixel on the screen. The size of the point can be controlled using glPointSize.
        - GL_LINES: This mode draws a series of connected line segments. Each pair of vertices defines a line segment. If there are an odd number of vertices, the last vertex is ignored.
        - GL_TRIANGLES: This mode draws a series of triangles. Each set of three vertices defines a single triangle. If there are an incomplete set of vertices (not a multiple of three), the last one or two vertices are ignored.
    """
    glBegin(GL_POINTS)

    # where to show the pixel, specifies the location of a point
    glVertex2f(x, y)

    # This function ends the block of code that began with glBegin. It tells OpenGL to finish processing the vertices and draw the specified points on the screen.
    glEnd()


def draw_lines():
    glLineWidth(5)
    glBegin(GL_LINES)
    glColor3f(1.0, 1.0, 0.0)
    glVertex2f(100, 100)
    glColor3f(1.0, 0.0, 0.0)
    glVertex2f(400, 200)
    glEnd()


def draw_triangles():
    glBegin(GL_TRIANGLES)
    glColor3f(1.0, 1.0, 0.0)
    glVertex2f(100, 100)
    glColor3f(1.0, 0.0, 0.0)
    glVertex2f(400, 200)
    glColor3f(0.0, 0.0, 0.1)
    glVertex2f(100, 400)
    glEnd()


def iterate():
    # glViewport takes 4 parameters
    # 1. x,y: The x and y coordinates of the lower left corner of the viewport rectangle, in pixels.
    # 2. width, height: The width and height of the viewport rectangle, in pixels.
    # the area of the window where OpenGL will draw the graphics.
    glViewport(0, 0, 500, 500)

    # glMatrixMode(GL_PROJECTION) used for setting up the camera view
    # glMatrixMode(GL_PROJECTION) sets the current matrix mode to GL_PROJECTION
    # This matrix controls how your scene is projected onto the screen (like setting up a camera lens)
    # This line tells OpenGL to start work1ing on the projection matrix, which is used to control how things we draw are shown on the screen, like setting up a camera view.
    # This is like telling OpenGL, "I'm going to set up how the camera sees the scene."
    # It switches the context to focus on camera settings, specifically how to project the 3D world onto our 2D screen.
    glMatrixMode(GL_PROJECTION)

    # glLoadIdentity replaces the current matrix with the identity matrix.
    # This clears any previous settings on the projection. It's like resetting our camera to a default, neutral position with no zoom, tilt, or pan.
    glLoadIdentity()

    # glOrtho is a transformation function that sets up a 2D orthographic viewing region.
    # glOrtho Defines a 2D orthographic projection matrix
    # An orthographic projection matrix is a way of representing three-dimensional objects in two dimensions without the effects of perspective. In simpler terms, it's a method to display 3D objects on a 2D screen where objects retain the same size and proportion regardless of their distance from the camera. This is different from perspective projection, where objects appear smaller as they get further away, mimicking how the human eye perceives depth.
    """  
        Simple Explanation (for glOrtho(0.0, 500, 0.0, 500, 0.0, 1.0)): 
        This sets up a simple, flat view where:
        - The x-coordinates of the scene will go from 0 to 500 on your screen.
        - The y-coordinates will also go from 0 to 500.
        - The z-coordinates (depth) are between 0.0 and 1.0, but for most 2D applications, this depth range isn't visually impactful.
    """
    glOrtho(0.0, 500, 0.0, 500, 0.0, 1.0)

    # GL_MODELVIEW is used for modeling and viewing transformations (like moving or rotating your entire scene)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def showScreen():
    # Clears the color and depth buffers. This means that the content of the window is cleared and ready for new drawing commands.
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # glLoadIdentity replaces the current matrix with the identity matrix.
    # Resets the current matrix, effectively "resetting" any transformations that have been applied so far.
    # In OpenGL, transformations (like translations, rotations, scaling) are applied to the current matrix.
    glLoadIdentity()

    # Call the iterate() function above
    iterate()

    # Sets the current color to yellow (RGB: 1.0, 1.0, 0.0). All subsequent drawing operations will use this color until it's changed again.
    glColor3f(1.0, 1.0, 0.0)

    # This is where we call the drawing functions
    # draw_points(250, 250)
    draw_lines()
    # draw_triangles()

    # Swaps the front and back buffers. In double-buffered rendering, drawing commands are applied to a back buffer while the front buffer is being displayed.
    # Swapping them makes the newly drawn frame visible, providing smooth animation and avoiding flicker.
    glutSwapBuffers()


# initialize glut, which is a utility toolkit for OpenGL. It should be called before any other GLUT functions. We need to initialize the GLUT library before setting up the display mode, window size, window position, and creating the window where OpenGL drawings will be rendered.
glutInit()

# set the initial display mode. It can take a number of parameters, but the most common are GLUT_RGB and GLUT_RGBA. GLUT_RGB is the default mode, but GLUT_RGBA is just an enhanced version of GLUT_RGB, where A stands for alpha channel. The alpha channel is used for transparency.
glutInitDisplayMode(GLUT_RGBA)

glutInitWindowSize(500, 500)  # window size
glutInitWindowPosition(0, 0)  # window position

'''
    glutCreateWindow: This function is called to create a window. It takes a single argument, which is the title of the window. The window title is specified as a byte string (hence the b prefix before the string literal), which is a requirement in Python 3 when interfacing with certain libraries that expect ASCII strings instead of the default Unicode strings.

    b"OpenGL Coding Practice": This is the title of the window, specified as a byte string. The b prefix indicates that what follows is a byte string, not a regular string. This is important for compatibility with the C-based libraries that GLUT wraps around, which expect strings in ASCII encoding.

    wind =: The result of glutCreateWindow (which is the window ID, a unique identifier for the created window) is assigned to the variable wind. This window ID can be used in subsequent calls to GLUT functions that require a reference to the window, although in many simple GLUT applications, this step is not strictly necessary since GLUT manages the current window implicitly.
'''
# this line creates a new window with the title "OpenGL Coding Practice" and assigns its window ID to the variable "wind".
wind = glutCreateWindow(b"OpenGL Coding Practice")

# This function sets the display callback for the current window. The display callback is the function that GLUT will call whenever the window needs to be redrawn. This can happen for several reasons, such as the window being opened for the first time, the window being resized, or explicitly requesting a redraw by calling. In this case, the showScreen function is set as the display callback, so it will be called whenever the window needs to be redrawn.
glutDisplayFunc(showScreen)

glutMainLoop()
