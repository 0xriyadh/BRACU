import random
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

W_Width, W_Height = 700, 700

rain_drops = []
rain_direction = 0
day_light = [0, 0, 0]


def convert_coordinate(x, y):
    global W_Width, W_Height
    a = x - (W_Width/2)
    b = (W_Height/2) - y
    return a, b


def draw_rain_drop(x, y):
    x, y = convert_coordinate(x, y)
    glPointSize(2)
    glBegin(GL_POINTS)
    glColor3f(0, 0.7, 1)
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
    glLineWidth(8)
    glColor3f(1, 0.9, 0.5)
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
    glColor3f(1, 0.8, 0.3)
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
    glColor3f(1, 0.8, 0)
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
    glColor3f(1, 0.5, 0)
    glVertex2d(-42, -180)
    glEnd()

    """
    /*//////////////////////////////////////////////////////////////
                                 WINDOW
    //////////////////////////////////////////////////////////////*/
    """
    glLineWidth(3)
    glColor3f(1, 0.5, 0)
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
    glColor3f(1, 0.8, 0.6)
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
    if key == b'd':
        if day_light[0] >= 1 and day_light[1] >= 1 and day_light[2] >= 1:
            print("Day Mode Activated")
            return
        day_light[0] += 0.1
        day_light[1] += 0.1
        day_light[2] += 0.1
        print("Day Light Increased", day_light)
    if key == b'n':
        if day_light[0] <= 0 and day_light[1] <= 0 and day_light[2] <= 0:
            print("Night Mode Activated") 
            return
        day_light[0] -= 0.1
        day_light[1] -= 0.1
        day_light[2] -= 0.1
        print("Day Light Decreased")

    glutPostRedisplay()

def specialKeyListener(key, x, y):
    global rain_direction
    if key == GLUT_KEY_LEFT:
        rain_direction -= 5
        print("Rain Direction Changing towards Left")
    if key == GLUT_KEY_RIGHT:  # up arrow key
        rain_direction += 5
        print("Rain Direction Changing towards Right")

    glutPostRedisplay()

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # clear the display
    glClearColor(*day_light, 0)  # color black
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

    glutSwapBuffers()


def animate():
    # codes for any changes in Models, Camera
    glutPostRedisplay()
    global rain_drops
    for i in range(len(rain_drops)):
        rain_drops[i][1] += 4
        rain_drops[i][0] += rain_direction * 0.1
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
glutKeyboardFunc(keyboardListener)
glutSpecialFunc(specialKeyListener)

glutMainLoop()  # The main loop of OpenGL
