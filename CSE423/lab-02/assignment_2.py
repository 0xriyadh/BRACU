
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import sys
import random

d_data = None
game = True
c_position = 0
diam = False
speed = 0.8
score = 0
pause = False
p_sign = False
c_pause = False

def drawLine(x0, y0, x1, y1):
    dx = x1-x0
    dy = y1-y0
    if abs(dx)>=abs(dy):
        if dx>=0:
            if dy>=0:
                drawLine_0(x0, y0, x1, y1, 0)
            else:
                drawLine_0(x0, -y0, x1, -y1, 7)
        else:
            if dy>=0:
                drawLine_0(-x0, y0, -x1, y1, 3)
            else:
                drawLine_0(-x0, -y0, -x1, -y1, 4)
    else:
        if dx>=0:
            if dy>=0:
                drawLine_0(y0, x0, y1, x1, 1)
            else:
                drawLine_0(-y0, x0, -y1, x1, 6)
        else:
            if dy>=0:
                drawLine_0(y0, -x0, y1, -x1, 2)
            else:
                drawLine_0(-y0, -x0, -y1, -x1, 5)

def drawLine_0(x0, y0, x1, y1, zone):
    dx = x1-x0
    dy = y1-y0
    dE = 2*(dy)
    dNE = 2*(dy - dx)
    d = 2*(dy) - dx
    x=x0
    y=y0
    while x < x1:
        draw8way(x, y, zone)
        if d < 0:
            d += dE
            x += 1
        else:
            d += dNE
            x += 1
            y += 1

def draw8way(x, y, zone):
    if zone == 0:
        drawPixel(x, y)
    elif zone == 1:
        drawPixel(y, x)
    elif zone == 2:
        drawPixel(-y, x)
    elif zone == 3:
        drawPixel(-x, y)
    elif zone == 4:
        drawPixel(-x, -y)
    elif zone == 5:
        drawPixel(-y, -x)
    elif zone == 6:
        drawPixel(y, -x)
    elif zone == 7:
        drawPixel(x, -y)

def drawPixel(x,y):
    glPointSize(2)
    glBegin(GL_POINTS)
    glVertex2f(x,y)
    glEnd()
    #print(f"Coordinates at ({x},{y})")

#drawLine(-10,-20,-20,70)

def diamond():
    global d_data, diam
    r = random.random()
    g = random.random()
    b = random.random()
    if r<0.4 and g<0.4 and b<0.4:
        b=1
    d_data = [random.randint(20, 480), 500, r, g, b] #x,y,r,g,b  #top of diamond is the point

def catcher(x):
    global game
    if game:
        glColor3f(1,1,1)
    else:
        glColor(1,0,0) #red if game over

    drawLine(x + 220, 10, x + 280, 10)
    drawLine(x + 225, 1, x + 275, 1)
    drawLine(x + 220, 10, x + 225, 1)
    drawLine(x + 280, 10, x + 275, 1)

def specialKeyListener(key, x, y):
    global c_position, game, c_pause
    if game and c_pause == False:
        if key==GLUT_KEY_RIGHT:
            if c_position < 220:
                c_position+=10
        if key==GLUT_KEY_LEFT:
            if c_position > -220:
                c_position-=10
    glutPostRedisplay()

def mouseListener(button, state, x, y):
    global speed, pause, game, diam, d_data, score, c_position, p_sign, c_pause
    if button==GLUT_LEFT_BUTTON:
        if state==GLUT_DOWN:
            #cross
            #print(x,y)
            if 455<x<495 and 455< (500-y) <495: #converting y coordinate
                print(f"Goodbye! Score: {score}")
                glutLeaveMainLoop()
            #pause
            elif 230<x<260 and 455<(500-y)<495:
                if pause == False:
                    pause = speed
                    speed = 0
                    p_sign = True
                    c_pause = True
                else:
                    speed = pause
                    pause = False
                    p_sign = False
                    c_pause = False
            #restart
            elif 5<x<45 and 455<(500-y)<495:
                print("Starting over!")
                game=True
                diam=False
                d_data=None
                score=0
                c_position=0
    glutPostRedisplay()

def init():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(500, 500)
    glutInitWindowPosition(650,50)
    wind = glutCreateWindow(b"Assignment 2")
    glClearColor(0, 0, 0, 0)
    glOrtho(0, 500, 0, 500, 0, 1)

def animate():
    global diam, speed, d_data
    if diam:
        #diamond()
        x, y, r, g, b = d_data
        glColor3f(r,g,b)
        drawLine(x, y, x - 15, y - 25)
        drawLine(x, y, x + 15, y - 25)
        drawLine(x - 15, y - 25, x, y - 50)
        drawLine(x + 15, y - 25, x, y - 50)
        d_data[1] = d_data[1] - speed
    glutPostRedisplay()


def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glColor3f(1.0, 1.0, 1.0)
    drawLine(0, 0, 500, 300)

    #cross
    glColor3f(1.0,0.0,0.0)
    drawLine(455, 495, 495, 455)
    drawLine(455, 455, 495, 495)

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

    global game, diam, c_position, d_data, speed, score

    if game:
        if diam == False:
            diamond()
            diam = True
        else:
            #diamond()
            x = d_data[0]
            y = d_data[1]
            c = c_position

            if (y-50) <= 10 and c+220 <= x <= c+280: 
                score += 1
                diam = False
                d_data = None
                print("Score:", score)
                # speed = min(speed*1.2,2)
                speed = speed*1.2

            elif (y-50) <= 1:
                print(f"Game over! Score: {score}")
                score = 0
                game= False
                diam = False
                d_data = None
                speed = 0.2


    animate()
    catcher(c_position)
    glutSwapBuffers()


init()
glutDisplayFunc(display)
glutSpecialFunc(specialKeyListener)
glutMouseFunc(mouseListener)
glutMainLoop()







