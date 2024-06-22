from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

import math

W_Width, W_Height = 500, 500


ballx = bally = 0
speed = 0.01
ball_size = 2
create_new = False


class point:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.z = 0


def crossProduct(a, b):
    result = point()
    result.x = a.y * b.z - a.z * b.y
    result.y = a.z * b.x - a.x * b.z
    result.z = a.x * b.y - a.y * b.x

    return result


def convert_coordinate(x, y):
    global W_Width, W_Height
    a = x - (W_Width/2)
    b = (W_Height/2) - y
    return a, b


def draw_points(x, y, s):
    glPointSize(s)  # pixel size. by default 1 thake
    glBegin(GL_POINTS)
    glVertex2f(x, y)  # jekhane show korbe pixel
    glEnd()


def drawAxes():
    glLineWidth(1)
    glBegin(GL_LINES)
    glColor3f(1.0, 0.0, 0.0)
    glVertex2f(-250, 0)
    glVertex2f(250, 0)
    glColor3f(0.0, 0.0, 1.0)
    glVertex2f(0, 250)
    glVertex2f(0, -250)
    glEnd()

    glPointSize(5)
    glBegin(GL_POINTS)
    glColor3f(0, 1.0, 0.0)
    glVertex2f(0, 0)

    glEnd()


def drawShapes():
    glBegin(GL_TRIANGLES)
    glVertex2d(-170, 170)
    glColor3f(0, 1.0, 0.0)
    glVertex2d(-180, 150)
    glColor3f(1, 0, 0.0)
    glVertex2d(-160, 150)
    glEnd()

    glBegin(GL_QUADS)
    glVertex2d(-170, 120)
    glColor3f(1, 0, 1)
    glVertex2d(-150, 120)
    glColor3f(0, 0, 1)
    glVertex2d(-150, 140)
    glColor3f(0, 1, 0)
    glVertex2d(-170, 140)
    glEnd()


def keyboardListener(key, x, y):

    global ball_size
    if key == b'w':
        ball_size += 1
        print("Size Increased")
    if key == b's':
        ball_size -= 1
        print("Size Decreased")
    # if key==b's':
    #    print(3)
    # if key==b'd':
    #     print(4)

    glutPostRedisplay()


def specialKeyListener(key, x, y):
    global speed
    if key == 'w':
        print(1)
    if key == GLUT_KEY_UP:
        speed *= 2
        print("Speed Increased")
    if key == GLUT_KEY_DOWN:  #  up arrow key
        speed /= 2
        print("Speed Decreased")
    glutPostRedisplay()
    # if key==GLUT_KEY_RIGHT:

    # if key==GLUT_KEY_LEFT:

    # if key==GLUT_KEY_PAGE_UP:

    # if key==GLUT_KEY_PAGE_DOWN:

    # case GLUT_KEY_INSERT:
    #
    #
    # case GLUT_KEY_HOME:
    #
    # case GLUT_KEY_END:
    #


def mouseListener(button, state, x, y):  # /#/x, y is the x-y of the screen (2D)
    global ballx, bally, create_new
    if button == GLUT_LEFT_BUTTON:
        if (state == GLUT_DOWN):  #  2 times?? in ONE click? -- solution is checking DOWN or UP
            print(x, y)
            c_X, c_y = convert_coordinate(x, y)
            ballx, bally = c_X, c_y

    if button == GLUT_RIGHT_BUTTON:
        if state == GLUT_DOWN:
            create_new = convert_coordinate(x, y)
    # case GLUT_MIDDLE_BUTTON:
    #     ........

    glutPostRedisplay()


def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # clear the display
    glClearColor(0, 0, 0, 0)  # color black
    glViewport(0, 0, W_Width, W_Height)

    # load the correct matrix -- MODEL-VIEW matrix
    glMatrixMode(GL_MODELVIEW)
    # initialize the matrix
    glLoadIdentity()


    """
        gluLookAt function requires three info
            1. where is the camera (viewer)? - Camera Position (0, 0, 200)
            2. where is the camera looking? - Look At Point (0, 0, 0)
            3. Which direction is the camera's UP direction? - Up Vector (0, 1, 0)
        
        1. Camera Position (0, 0, 200): This is where the camera is located in the 3D space. In your case, it's positioned at (0, 0, 200), which means it is 200 units away from the origin along the Z-axis. The camera is looking towards the origin if no other rotations are applied.

        2. Look At Point (0, 0, 0): This is the point in the 3D space that the camera is looking at. Here, it's set to (0, 0, 0), the origin of the scene. This means the camera is directly looking towards the center of the scene.

        3. Up Vector (0, 1, 0): This vector defines which direction is "up" from the perspective of the camera. In this case, (0, 1, 0) corresponds to the positive Y-axis being "up". This helps OpenGL determine the orientation of the camera. The up vector is perpendicular to the direction the camera is looking at.
    """
    gluLookAt(0, 0, 200,	0, 0, 0,	0, 1, 0)
    glMatrixMode(GL_MODELVIEW)

    drawAxes()
    # global ballx, bally, ball_size
    # draw_points(ballx, bally, ball_size)
    # drawShapes()

    # glBegin(GL_LINES)
    # glVertex2d(180, 0)
    # glVertex2d(180, 180)
    # glVertex2d(180, 180)
    # glVertex2d(0, 180)
    # glEnd()

    # if (create_new):
    #     m, n = create_new
    #     glBegin(GL_POINTS)
    #     glColor3f(0.7, 0.8, 0.6)
    #     glVertex2f(m, n)
    #     glEnd()

    glutSwapBuffers()


def animate():
    # codes for any changes in Models, Camera
    glutPostRedisplay()
    global ballx, bally, speed
    ballx = (ballx+speed) % 180
    bally = (bally+speed) % 180


def init():
    # clear the screen
    glClearColor(0, 0, 0, 0)
    # load the PROJECTION matrix
    glMatrixMode(GL_PROJECTION)
    # initialize the matrix
    glLoadIdentity()

    """  
        sets up a perspective projection matrix that defines a viewing frustum. This projection transforms 3D coordinates into the 2D coordinates that you see on your screen, while maintaining a sense of depth. The function is typically used to simulate the perspective view that humans perceive in the real world, where objects appear smaller as they get further away from the viewer.

        1. Field of View (FOV): The Field of View (FOV) is the extent of the observable world that is visible at any moment from a particular position. Imagine looking through a camera or binoculars; the FOV is how wide the scene you can see is. It's usually expressed in degrees. A larger FOV allows you to see a wider area but can make objects appear smaller and further away, while a smaller FOV focuses more narrowly on objects, making them appear larger and closer.
        Example: If your FOV is 90 degrees, it means you can see 90 degrees wide in front of you, like looking through a wide-angle lens.

        2. Aspect Ratio: The Aspect Ratio is the ratio of the width to the height of an image or screen. It determines the shape of the display or the images you see. Common aspect ratios include 16:9 for most modern TVs and monitors, and 4:3 for older TVs.
        Example: If a screen has an aspect ratio of 16:9, for every 16 units of width, it has 9 units of height. This would make the screen noticeably wider than it is tall.

        3. Near Clipping Plane: The Near Clipping Plane is the closest distance at which the camera starts rendering scenes. Anything closer than this distance will not be visible (it gets "clipped"). This helps in managing the rendering workload by not drawing objects too close to the viewer that might not be visible or might distort the view.
        Example: If the near clipping plane is set at 1 meter, anything closer than 1 meter to the camera will not be shown in the rendered scene.
        
        4. Far Clipping Plane: The Far Clipping Plane is the farthest distance at which the camera stops rendering scenes. Objects beyond this distance will not be visible. This is used to optimize rendering by not drawing objects that are too far away to be seen clearly or are beyond the visible horizon of the scene.
        Example: If the far clipping plane is set at 1000 meters, anything beyond 1000 meters from the camera will not appear in the view.
    """
    gluPerspective(104,	1,	1,	1000.0)


glutInit()
glutInitWindowSize(W_Width, W_Height)
glutInitWindowPosition(0, 0)

"""  
    GLUT_DEPTH: This flag tells OpenGL to create a depth buffer for the window. The depth buffer is used to determine which objects are in front of others, which is important for rendering 3D scenes correctly.

    GLUT_DOUBLE: This flag tells OpenGL to create a double-buffered window. Double buffering is a technique used to prevent flickering in animations. Instead of drawing directly to the screen, OpenGL draws to an off-screen buffer. Once the frame is complete, it swaps the off-screen buffer with the on-screen buffer, making the new frame visible to the user.

    GLUT_RGB: This flag tells OpenGL to create a window with a red, green, and blue color buffer. This is the most common color mode used in OpenGL.
"""
glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB)

wind = glutCreateWindow(b"OpenGL Coding Practice")
init()

glutDisplayFunc(display)  # display callback function
# what you want to do in the idle time (when no drawing is occuring)
glutIdleFunc(animate)

glutKeyboardFunc(keyboardListener)
glutSpecialFunc(specialKeyListener)
glutMouseFunc(mouseListener)

glutMainLoop()  # The main loop of OpenGL
