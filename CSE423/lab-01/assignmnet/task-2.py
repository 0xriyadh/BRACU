import random
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

W_Width, W_Height = 500, 500
day_light = [0, 0, 0]
opposite_day_light = [1, 1, 1]
points = []


def convert_coordinate(x, y):
    global W_Width, W_Height
    a = x - (W_Width/2)
    b = (W_Height/2) - y
    return a, b


def draw_point(x, y, color):
    x, y = convert_coordinate(x, y)
    glPointSize(15)
    glBegin(GL_POINTS)
    glColor3f(*color)
    glVertex2f(x, y)
    glEnd()


def draw_points():
    for point in points:
        draw_point(point[0], point[1], point[2])


def random_color():
    return random.random(), random.random(), random.random()


def random_direction():
    return random.choice([-1, 1])


def new_point(x, y):
    return [x, y, random_color(), random_direction(), random_direction()]


def keyboardListener(key, x, y):
    if key == b'd':
        print("Day Light Increased")
    if key == b'n':
        print("Day Light Decreased")

    glutPostRedisplay()


def specialKeyListener(key, x, y):
    if key == GLUT_KEY_LEFT:
        print("Rain Direction Changing towards Left")
    if key == GLUT_KEY_RIGHT:  # up arrow key
        print("Rain Direction Changing towards Right")

    glutPostRedisplay()


def mouseListener(button, state, x, y):
    if button == GLUT_RIGHT_BUTTON:
        if state == GLUT_DOWN:
            points.append(new_point(x, y))
            print("New Point Added at", x, y)

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

    draw_points()

    glutSwapBuffers()


def animate():
    # codes for any changes in Models, Camera
    glutPostRedisplay()
    for point in points:
        point[0] += point[3]
        point[1] += point[4]

        if point[0] >= W_Width or point[0] <= 0:
            point[3] *= -1
        if point[1] >= W_Height or point[1] <= 0:
            point[4] *= -1


def init():
    # clear the screen
    glClearColor(*day_light, 0)
    # load the PROJECTION matrix
    glMatrixMode(GL_PROJECTION)
    # initialize the matrix
    glLoadIdentity()
    gluPerspective(104,	1,	1,	1000.0)


glutInit()
glutInitWindowSize(W_Width, W_Height)
glutInitWindowPosition(0, 0)
glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB)
wind = glutCreateWindow(b"Amazing Box")
init()
glutDisplayFunc(display)  # display callback function

glutIdleFunc(animate)

glutMouseFunc(mouseListener)
glutKeyboardFunc(keyboardListener)
glutSpecialFunc(specialKeyListener)

glutMainLoop()  # The main loop of OpenGL
