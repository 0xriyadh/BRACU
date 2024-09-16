import random
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math

W_Width, W_Height = 500, 500
pause = False
gameOver = False
speed = 0.4
score = 0
circles = []
bullets = []
circle_miss_count = 0
bullet_miss_count = 0
shooter_position = 250
shooter_radius = 20
shooter_y = 30

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

def drawCircle(x0, y0, radius):
    x = radius
    y = 0
    d = 1 - radius

    while x >= y:
        # Draw 8 octants of the circle
        drawPixel(x0 + x, y0 + y)
        drawPixel(x0 - x, y0 + y)
        drawPixel(x0 + x, y0 - y)
        drawPixel(x0 - x, y0 - y)
        drawPixel(x0 + y, y0 + x)
        drawPixel(x0 - y, y0 + x)
        drawPixel(x0 + y, y0 - x)
        drawPixel(x0 - y, y0 - x)

        y += 1
        if d <= 0:
            d += 2 * y + 1
        else:
            x -= 1
            d += 2 * (y - x) + 1

def shooter(x):
    global gameOver, shooter_radius, shooter_y
    if not gameOver:
        glColor3f(1, 1, 1)
    else:
        glColor3f(1, 0, 0)
    drawCircle(x, shooter_y, shooter_radius)

def mouseListener(button, state, x, y):
    global speed, pause, gameOver, score, circles, bullets, bullet_miss_count, circle_miss_count, shooter_position

    if button==GLUT_LEFT_BUTTON:
        if state==GLUT_DOWN:

            # close button
            if 450<x<490 and 450< (W_Height - y) <490: #converting y coordinate
                print(f"Goodbye! Score: {score}")
                glutDestroyWindow(glutGetWindow())  # Close the window

            # pause button
            elif 230<x<270 and 450<(500-y)<490:
                if pause == False:
                    print("Game Paused!")
                    pause = True
                else:
                    print("Game Resumed!")
                    pause = False
                
            #restart
            elif 5<x<45 and 455<(500-y)<495:
                print("Game Restarted!")
                gameOver=False
                score=0
                shooter_position = 250
                circles = []
                bullets = []
                bullet_miss_count = 0
                circle_miss_count = 0
                pause = False

    glutPostRedisplay()

def keyboardListener(key, a, b): 
    global gameOver, pause, shooter_position, bullets
    
    if not gameOver and not pause:
        if key==b'a':
            if shooter_position > 28:
                shooter_position -= 10
        if key==b'd':
            if shooter_position < 472:
                shooter_position += 10
        if key==b' ':
            bullets.append([shooter_position, shooter_y, 7])

    glutPostRedisplay()

def animate():
    global gameOver, circles, circle_miss_count, bullets, bullet_miss_count, speed, score

    if not gameOver:
        if len(bullets) > 0:
            i = 0
            while i < (len(bullets)):
                x, y, r = bullets[i]
                glColor3f(0.8, 0.3, 1)
                drawCircle(x, y, r)
                if not pause:
                    bullets[i][1] += 1
                if bullets[i][1] > 500:
                    bullets.pop(i)
                    bullet_miss_count += 1
                    print(f"Misfired {bullet_miss_count}/3")
                    if bullet_miss_count == 3:
                        gameOver = True
                        print(f"Game Over! Your Score: {score}")
                        break
                    i -= 1       
                i += 1                 

        if len(circles) > 0:
            i = 0
            while i < len(circles):
                x, y, r = circles[i]
                glColor3f(0.8, 1, 0.3)
                drawCircle(x, y, r)
                if not pause:
                    circles[i][1] -= speed
                if circles[i][1] < 0:
                    circles.pop(i)
                    circle_miss_count += 1
                    print(f"Circle Missed {circle_miss_count}/3")
                    if circle_miss_count == 3:
                        gameOver = True
                        print(f"Game Over! Your Score: {score}")
                        break
                    i -= 1
                i += 1

    glutPostRedisplay() 

def display():
    global shooter_position, gameOver, pause, shooter_y, shooter_radius, score, circles, bullets

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # clear the display
    glClearColor(0, 0, 0, 0)

    # restart button
    glColor3f(0.2,0.8,0.9)
    drawLine(10, 470, 50, 470)
    drawLine(10, 470, 30, 490)
    drawLine(10, 470, 30, 450)

    # pause button
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

    if not gameOver:
        if len(circles) == 0:
            circles.append([random.randint(35, 465), 500, 30])
        elif circles[-1][1] < 400:
            circles.append([random.randint(35, 465), 500, 30])

        vanishing_circles = []
        vanishing_bullets = []

        # collision detection between circles and bullets
        for i in range(len(circles)):
            x_circle, y_circle, r_circle = circles[i]
            for j in range(len(bullets)):
                x_bullet, y_bullet, r_bullet = bullets[j]
                distance = math.sqrt((x_bullet - x_circle) ** 2 + (y_bullet - y_circle) ** 2)
                if distance <= (r_bullet + r_circle):
                    print("Hit!")
                    score += 1
                    print("Score:", score)
                    vanishing_circles.append(i)
                    vanishing_bullets.append(j)
        
            # collision detection between circles and shooter
            distance = math.sqrt((shooter_position - x_circle) ** 2 + (shooter_y - y_circle) ** 2)
            if distance <= (shooter_radius + r_circle):
                print(f"Oh NO, Crashed!!! \nGame Over! Score: {score}")
                gameOver = True
                break

        for i in vanishing_circles:
            circles.pop(i)

        for i in vanishing_bullets:
            bullets.pop(i)


    shooter(shooter_position)
    animate()
    glutSwapBuffers()

def init():
    glClearColor(0, 0, 0, 0)
    glOrtho(0, 500, 0, 500, 0, 1)

glutInit()
glutInitWindowSize(W_Width, W_Height)
glutInitWindowPosition(0, 0)
glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB)
wind = glutCreateWindow(b"Shoot The Circles")
init()
glutDisplayFunc(display)
glutKeyboardFunc(keyboardListener)
glutMouseFunc(mouseListener)
glutMainLoop()
