import random
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

W_Width, W_Height = 500, 500
black_color = [0, 0, 0]
blink_box_state = [0, 0, 0, 0]
points = []
speed = 1
should_blink = False


def draw_blink_box():
    global blink_box_state
    glEnable(GL_BLEND)  # Set up blending for transparency
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glBegin(GL_QUADS)
    glColor4f(*blink_box_state)
    glVertex2d(-250, 250)
    glVertex2d(-250, -250)
    glVertex2d(250, -250)
    glVertex2d(250, 250)
    glEnd()


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
    global speed

    if key == GLUT_KEY_UP:
        speed += 1
        print("Speed Increased")

    if key == GLUT_KEY_DOWN:
        speed -= 1
        print("Speed Decreased")

    glutPostRedisplay()


def mouseListener(button, state, x, y):
    global points, should_blink

    if button == GLUT_RIGHT_BUTTON:
        if state == GLUT_DOWN:
            points.append(new_point(x, y))
            print("New Point Added at", x, y)
    if button == GLUT_LEFT_BUTTON:
        if state == GLUT_DOWN:
            print("Left Button Pressed")
            should_blink = not should_blink
            toggle_blink_box(0)

    glutPostRedisplay()


def toggle_blink_box(value):
    global blink_box_state, should_blink

    if not should_blink:
        return
    # Toggle the alpha value for transparency
    blink_box_state[3] = 1 - blink_box_state[3]
    glutPostRedisplay()  # Request a redraw to see the changes
    # Call toggle_blink_box again after 3 seconds
    glutTimerFunc(500, toggle_blink_box, 0)



def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # clear the display
    glClearColor(*black_color, 0)  # color black
    glViewport(0, 0, W_Width, W_Height)

    # load the correct matrix -- MODEL-VIEW matrix
    glMatrixMode(GL_MODELVIEW)
    # initialize the matrix
    glLoadIdentity()

    gluLookAt(0, 0, 200,	0, 0, 0,	0, 1, 0)
    glMatrixMode(GL_MODELVIEW)

    draw_points()
    draw_blink_box()

    glutSwapBuffers()


def animate():
    # codes for any changes in Models, Camera
    glutPostRedisplay()
    for point in points:
        point[0] += point[3] * speed
        point[1] += point[4] * speed

        if point[0] >= W_Width or point[0] <= 0:
            point[3] *= -1
        if point[1] >= W_Height or point[1] <= 0:
            point[4] *= -1


def init():
    # clear the screen
    glClearColor(*black_color, 0)
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
