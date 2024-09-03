import random
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

W_Width, W_Height = 500, 500
pause = False
gameOver = False
showDiamond = False
diamondInfo = None
speed = 0.4
catcher_position = 200
catcher_pause = False
catcher_speed = 15
score = 0

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

def drawDiamond(x, y):
    drawLine(x, y, x - 10, y - 20)
    drawLine(x, y, x + 10, y - 20)
    drawLine(x, y - 40, x - 10, y - 20)
    drawLine(x, y - 40, x + 10, y - 20)

def generateDiamond():
    global diamondInfo
    x = random.randint(12, W_Width-12)
    y = 440
    r, g, b = random.uniform(0.5, 1.0), random.uniform(0.5, 1.0), random.uniform(0.5, 1.0)
    
    diamondInfo = [x, y, r, g, b]

def drawCatcher(x):
    global gameOver
    y = 15

    if gameOver:
        glColor(1,0,0)
    else:
        glColor3f(1,1,1)

    drawLine(x, y, x + 100, y)
    drawLine(x, y, x + 20, y - 15)
    drawLine(x + 100, y, x + 80, y - 15)
    drawLine(x + 20, y - 15, x + 80, y - 15)   

# AABB Collision Detection algorithm
def hasCollided(x1, y1, x2, y2):
    if x1 < x2 + 100 and x1 + 100 > x2 and y1 < (y2 + 15) and (y1 + 40) > y2:
        return True
    return False

def mouseListener(button, state, x, y):
    global speed, pause, gameOver, showDiamond, diamondInfo, score, catcher_position, catcher_pause

    if button==GLUT_LEFT_BUTTON:
        if state==GLUT_DOWN:

            # close button
            if 450<x<490 and 450< (W_Height - y) <490: #converting y coordinate
                print(f"Goodbye! Score: {score}")
                glutDestroyWindow(glutGetWindow())  # Close the window

            # pause button
            elif 230<x<270 and 450<(500-y)<490:
                print("Paused/Resumed")
                if pause == False:
                    pause = True
                    catcher_pause = True
                else:
                    pause = False
                    catcher_pause = False
                
            #restart
            elif 5<x<45 and 455<(500-y)<495:
                print("Starting over!")
                showDiamond=False
                diamondInfo=None
                gameOver=False
                score=0
                catcher_position=200
    glutPostRedisplay()

def specialKeyListener(key, a, b):
    global catcher_position, gameOver, catcher_pause, catcher_speed
    if not gameOver and not catcher_pause:
        if key==GLUT_KEY_RIGHT:
            if catcher_position < 400:
                catcher_position+=catcher_speed
        if key==GLUT_KEY_LEFT:
            if catcher_position > 0:
                catcher_position-=catcher_speed
    glutPostRedisplay()

def animate():
    global showDiamond, speed, diamondInfo, pause
    if showDiamond:
        x, y, r, g, b = diamondInfo
        glColor3f(r, g, b)
        drawDiamond(x, y)
        
        if not pause:
            diamondInfo[1] = diamondInfo[1] - speed

    glutPostRedisplay() 

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # clear the display
    glClearColor(0, 0, 0, 0)

    # restart button
    glColor3f(0.2,0.8,0.9)
    drawLine(10, 470, 50, 470)
    drawLine(10, 470, 30, 490)
    drawLine(10, 470, 30, 450)

    # pause button
    global pause
    if pause == False:
        glColor3f(1.0,0.8,0.2)
        drawLine(240, 490, 240, 450)
        drawLine(260, 490, 260, 450)
    else:
        glColor3f(1.0, 0.8, 0.2)
        drawLine(230, 490, 270, 470)
        drawLine(230, 490, 230, 450)
        drawLine(230, 450, 270, 470)

    # close button
    glColor3f(1.0,0.0,0.0)
    drawLine(450, 490, 490, 450)
    drawLine(450, 450, 490, 490)

    global gameOver, diamondInfo, showDiamond, score, catcher_position, speed, score

    if not gameOver:
        if not showDiamond:
            generateDiamond()
            showDiamond = True
        else:
            x1 = diamondInfo[0]
            y1 = diamondInfo[1]

            x2 = catcher_position
            y2 = 15

            # if hasCollided(x1, y1, x2, y2):
            if (y1-40) <= 15 and x2 <= x1 <= x2+100: 
                score += 1
                showDiamond = False
                diamondInfo = None
                print("Score:", score)
                speed *= 1.2
                catcher_speed *= 1.2
            elif y1 <= y2:
                gameOver = True
                print(f"Game over! Score: {score}")
                score = 0
                showDiamond = False
                diamondInfo = None
                speed = 0.4
                catcher_speed = 15

    animate()
    drawCatcher(catcher_position)
    glutSwapBuffers()

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
glutSpecialFunc(specialKeyListener)
glutMouseFunc(mouseListener)
glutMainLoop()
