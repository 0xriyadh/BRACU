import random
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

import math

W_Width, W_Height = 700, 700


ball_x = ball_y = 0
# speed = 0.01
speed = 1
ball_size = 2
create_new = False
rain_drops = []


def convert_coordinate(x, y):
    global W_Width, W_Height
    a = x - (W_Width/2)
    b = (W_Height/2) - y
    return a, b


def draw_rain_drop(x, y):
    x, y = convert_coordinate(x, y)
    glPointSize(2)
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glVertex2f(x, y + 1)
    glVertex2f(x, y + 2)
    glVertex2f(x, y + 3)
    glVertex2f(x, y + 4)
    glEnd()


def drawHouse():
    """
    /*//////////////////////////////////////////////////////////////
                            HOUSE'S BASE
    //////////////////////////////////////////////////////////////*/
    """
    glLineWidth(8)  # width of the lines
    glColor3f(1, 1, 1)  # color of the lines: white
    glBegin(GL_LINES)

    # bottom line
    glVertex2d(-140, -247)
    glVertex2d(140, -247)

    # right line
    glVertex2d(140, -250)
    glVertex2d(140, -30)

    # upper line
    glVertex2d(140, -33)
    glVertex2d(-140, -33)

    # left line
    glVertex2d(-140, -30)
    glVertex2d(-140, -250)

    glEnd()

    """
    /*//////////////////////////////////////////////////////////////
                            HOUSE'S ROOF
    //////////////////////////////////////////////////////////////*/
    """
    glBegin(GL_TRIANGLES)
    glColor3f(0.7, 0.7, 0.7)  # color of the roof: gray
    glVertex2d(-160, -36)
    glVertex2d(160, -36)
    glVertex2d(0, 80)
    glEnd()

    """
    /*//////////////////////////////////////////////////////////////
                              DOOR
    //////////////////////////////////////////////////////////////*/
    """
    glLineWidth(3)
    glColor3f(0.7, 0.7, 0.7)  # color of the door: gray
    glBegin(GL_LINES)

    # left line
    glVertex2d(-100, -120)
    glVertex2d(-100, -245)

    # right line
    glVertex2d(-30, -120)
    glVertex2d(-30, -245)

    # upper line
    glVertex2d(-100, -121)
    glVertex2d(-30, -121)

    glEnd()

    """
    /*//////////////////////////////////////////////////////////////
                               DOOR KNOB
    //////////////////////////////////////////////////////////////*/
    """
    glPointSize(8)
    glBegin(GL_POINTS)
    glColor3f(0, 1, 1)
    glVertex2d(-42, -180)
    glEnd()

    """
    /*//////////////////////////////////////////////////////////////
                                 WINDOW
    //////////////////////////////////////////////////////////////*/
    """
    glLineWidth(3)
    glColor3f(0.7, 0.7, 0.7)  # color of the window: gray
    glBegin(GL_LINES)

    # left line
    glVertex2d(40, -70)
    glVertex2d(40, -130)

    # right line
    glVertex2d(100, -70)
    glVertex2d(100, -130)

    # upper line
    glVertex2d(40, -71)
    glVertex2d(100, -71)

    # lower line
    glVertex2d(40, -129)
    glVertex2d(100, -129)

    glEnd()

    glLineWidth(1)
    glBegin(GL_LINES)

    # vertical line
    glVertex2d(70, -72)
    glVertex2d(70, -130)

    # horizontal line
    glVertex2d(40, -100)
    glVertex2d(100, -100)

    glEnd()


def keyboardListener(key, x, y):

    global ball_size
    if key == b'w':
        ball_size += 1
        print("Size Increased")
    if key == b's':
        ball_size -= 1
        print("Size Decreased")

    glutPostRedisplay()


def specialKeyListener(key, x, y):
    global speed
    if key == GLUT_KEY_UP:
        speed *= 2
        print("Speed Increased")
    if key == GLUT_KEY_DOWN:  # up arrow key
        speed /= 2
        print("Speed Decreased")

    glutPostRedisplay()


def mouseListener(button, state, x, y):  # /#/x, y is the x-y of the screen (2D)
    global ball_x, ball_y, create_new
    if button == GLUT_LEFT_BUTTON:
        if (state == GLUT_DOWN):  # 2 times?? in ONE click? -- solution is checking DOWN or UP
            print(x, y)
            ball_x, ball_y = convert_coordinate(x, y)

    if button == GLUT_RIGHT_BUTTON:
        if state == GLUT_DOWN:
            print(x, y)
            create_new = convert_coordinate(x, y)
    # case GLUT_MIDDLE_BUTTON:
    #     ........

    # glutPostRedisplay() ensures that any changes in object positions or new objects are rendered on the screen.
    glutPostRedisplay()


def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # clear the display
    glClearColor(0, 0, 0, 0)  # color black
    glViewport(0, 0, W_Width, W_Height)

    # load the correct matrix -- MODEL-VIEW matrix
    glMatrixMode(GL_MODELVIEW)
    # initialize the matrix
    glLoadIdentity()

    gluLookAt(0, 0, 200,	0, 0, 0,	0, 1, 0)
    glMatrixMode(GL_MODELVIEW)

    drawHouse()
    for raindrop in rain_drops:
        draw_rain_drop(raindrop[0], raindrop[1])
    # drawAxes()
    # global ball_x, ball_y, ball_size
    # draw_points(ball_x, ball_y, ball_size)
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
    global rain_drops
    for i in range(len(rain_drops)):
        rain_drops[i][1] += 5
        if rain_drops[i][1] > 700:
            rain_drops[i][0] = random.randint(0, W_Width)
            rain_drops[i][1] = 0


def init():
    # clear the screen
    glClearColor(0, 0, 0, 0)
    # load the PROJECTION matrix
    glMatrixMode(GL_PROJECTION)
    # initialize the matrix
    glLoadIdentity()
    gluPerspective(104,	1,	1,	1000.0)


glutInit()
glutInitWindowSize(W_Width, W_Height)
glutInitWindowPosition(0, 0)
glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB)
wind = glutCreateWindow(b"Rainfall House")
init()
glutDisplayFunc(display)  # display callback function

for i in range(250):
    x = random.randint(0, W_Width)
    y = random.randint(0, W_Height)
    rain_drops.append([x, y])
glutIdleFunc(animate)
print(rain_drops)

# glutMouseFunc(mouseListener)
# glutKeyboardFunc(keyboardListener)
# glutSpecialFunc(specialKeyListener)

glutMainLoop()  # The main loop of OpenGL
