import random
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

W_Width, W_Height = 700, 700
p_sign = False

def drawPixel(x, y):
    glPointSize(2)
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()

def zone_identifier(dx, dy):
    if dx >= 0:
        if dy >= 0:
            if abs(dx) >= abs(dy):
                return 0
            else:
                return 1
        else:
            if abs(dx) >= abs(dy):
                return 7
            else:
                return 6
    else:
        if dy >= 0:
            if abs(dx) >= abs(dy):
                return 3
            else:
                return 2
        else:
            if abs(dx) >= abs(dy):
                return 4
            else:
                return 5

# convert from zone 0 to other zones
def zone_converter_0_to_others(x, y, zone):
    if zone == 0:
        return x, y
    elif zone == 1:
        return y, x
    elif zone == 2:
        return -y, x
    elif zone == 3:
        return -x, y
    elif zone == 4:
        return -x, -y
    elif zone == 5:
        return -y, -x
    elif zone == 6:
        return y, -x
    elif zone == 7:
        return x, -y
    
# convert from other zones to zone 0
def zone_converter_other_to_0(x, y, zone):
    if zone == 0:
        return x, y
    elif zone == 1:
        return y, x
    elif zone == 2:
        return y, -x
    elif zone == 3:
        return -x, y
    elif zone == 4:
        return -x, -y
    elif zone == 5:
        return -y, -x
    elif zone == 6:
        return -y, x
    elif zone == 7:
        return x, -y
  
def drawLine(x0, y0, x1, y1):
    dx = x1 - x0
    dy = y1 - y0

    zone = zone_identifier(dx, dy) 

    x0, y0 = zone_converter_other_to_0(x0, y0, zone)
    x1, y1 = zone_converter_other_to_0(x1, y1, zone)

    drawFinalLine(x0, y0, x1, y1, zone)

def drawFinalLine(x0, y0, x1, y1, zone):
    dx = x1-x0
    dy = y1-y0
    dE = 2*(dy)
    dNE = 2*(dy - dx)
    d = 2*(dy) - dx
    x=x0
    y=y0
    while x < x1:
        drawPixel(*zone_converter_0_to_others(x, y, zone))
        if d < 0:
            d += dE
            x += 1
        else:
            d += dNE
            x += 1
            y += 1

def keyboardListener(key, x, y):
    if key == b'd':
        if day_light[0] >= 1 and day_light[1] >= 1 and day_light[2] >= 1:
            print("Day Mode Activated")
            return
        day_light[0] += 0.2
        day_light[1] += 0.2
        day_light[2] += 0.2
        opposite_day_light[0] -= 0.2
        opposite_day_light[1] -= 0.2
        opposite_day_light[2] -= 0.2
        print("Day Light Increased", day_light)
    if key == b'n':
        if day_light[0] <= 0 and day_light[1] <= 0 and day_light[2] <= 0:
            print("Night Mode Activated")
            return
        day_light[0] -= 0.2
        day_light[1] -= 0.2
        day_light[2] -= 0.2
        opposite_day_light[0] += 0.2
        opposite_day_light[1] += 0.2
        opposite_day_light[2] += 0.2
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
    glClearColor(0, 0, 0, 0)

    #cross
    glColor3f(1.0,0.0,0.0)
    drawLine(455, 495, 495, 455)
    drawLine(455, 455, 495, 495)

    glColor3f(1.0,0.8,0.2)
    # drawLine(240, 495, 240, 455)
    # drawLine(260, 495, 260, 455)

    #pause
    global p_sign
    if p_sign==False:
        glColor3f(1.0,0.8,0.2)
        drawLine(240, 495, 240, 455)
        drawLine(260, 495, 260, 455)
    else:
        glColor3f(1.0, 0.8, 0.2)
        drawLine(230, 495, 270, 475)
        drawLine(230, 495, 230, 455)
        drawLine(230, 455, 270, 475)

    #restart
    glColor3f(0.2,0.8,0.9)
    drawLine(25, 495, 5, 475)
    drawLine(5, 475, 25, 455)
    drawLine(5, 475, 45, 475)

    glutSwapBuffers()

def animate():
    # codes for any changes in Models, Camera
    glutPostRedisplay()
    global rain_drops
    for i in range(len(rain_drops)):
        rain_drops[i][1] += 6
        rain_drops[i][0] += rain_direction * 0.1
        if rain_drops[i][1] > 700:
            rain_drops[i][0] = random.randint(0, W_Width)
            rain_drops[i][1] = 0
        if rain_drops[i][0] > W_Width:
            rain_drops[i][0] = 0
        if rain_drops[i][0] < 0:
            rain_drops[i][0] = W_Width
        
def init():
    # clear the screen
    glClearColor(0, 0, 0, 0)
    # # load the PROJECTION matrix 
    # glMatrixMode(GL_PROJECTION)
    # # initialize the matrix
    # glLoadIdentity()
    # gluPerspective(104,	1,	1,	1000.0)
    glOrtho(0, 500, 0, 500, 0, 1)

glutInit()
glutInitWindowSize(W_Width, W_Height)
glutInitWindowPosition(0, 0)
glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB)
wind = glutCreateWindow(b"Catch The Diamond")
init()
glutDisplayFunc(display)

# for i in range(300):
#     x = random.randint(0, W_Width)
#     y = random.randint(0, W_Height)
#     rain_drops.append([x, y])
# glutIdleFunc(animate)
# print(rain_drops)

# # glutMouseFunc(mouseListener)
# glutKeyboardFunc(keyboardListener)
# glutSpecialFunc(specialKeyListener)

glutMainLoop()  # The main loop of OpenGL
