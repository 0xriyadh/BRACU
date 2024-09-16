from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import sys
import random
 
game = True
s_position = 250
bullets = []
circles = 0
c_data = []
speed = 0.3
score = 0
circle_miss = 0
bullet_miss = 0
pause = False
p_sign = False
 

 
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
       draw8way_line(x, y, zone)
       if d < 0:
           d += dE
           x += 1
       else:
           d += dNE
           x += 1
           y += 1
def draw8way_line(x, y, zone):
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
 

 
def draw8way(x, y, x0, y0):
   drawPixel(x+x0,  y+y0)
   drawPixel(-x+x0, y+y0)
   drawPixel(x+x0, -y+y0)
   drawPixel(-x+x0, -y+y0)
   drawPixel(y+x0, x+y0)
   drawPixel(-y+x0, x+y0)
   drawPixel(y+x0, -x+y0)
   drawPixel(-y+x0, -x+y0)
 
def drawPixel(x,y):
   glPointSize(2)
   glBegin(GL_POINTS)
   glVertex2f(x, y)
   glEnd()
 
def drawCircle_1(r, x0, y0):
   x=0
   y=r
   d=5-4*r
   draw8way(x,y, x0, y0)
   while y>x:
       if d<0:
           d+=4*(2*x+3)
           x+=1
       else:
           d+=4*(2*x-2*y+5)
           x+=1
           y-=1
       draw8way(x,y, x0, y0)

def shooter(x):
   global game
   if game:
       glColor3f(0.4, 0.8, 0.3)
   else:
       glColor(1, 0, 0)
   drawCircle_1(15, x, 16)
 
def bullet(x):
   global bullets
   bullets.append([4,x,30])
 
def circle():
   global circles, c_data
   c_data.append([25, random.randint(26,474), 500])
 
def keyboardListener(key, x, y):
   global s_position, game, pause, bullets
   if game and pause == False:
       if key==b'd':
           if s_position < 482:
               s_position+=8
       if key==b'a':
           if s_position > 18:
               s_position-=8
       if key==b' ':
           bullet(s_position)
   glutPostRedisplay()
 
 
def animate():
   global bullets, game, circles, speed, c_data, circle_miss, bullet_miss, score
   if game:
       if len(bullets) > 0:
           i = 0
           while i < (len(bullets)):
               r, x, y = bullets[i]
               glColor3f(0.4, 0.8, 0.3)
               drawCircle_1(r, x, y)
               if pause==False:
                   bullets[i][2] += 2
               if bullets[i][2] > 500:
                   bullets.pop(i)
                   bullet_miss += 1
                   print(f"Bullet misfired {bullet_miss}/3 ; Lives remaining {3-bullet_miss}")
                   if bullet_miss==3:
                       print(f"Game Over! Score: {score}")
                       game=False
                       break
                   i -= 1
               i += 1
 
       if circles > 0:
           i = 0
           while i < len(c_data):
               r, x, y = c_data[i]
               glColor3f(1, 0.6, 0.9)
               drawCircle_1(r, x, y)
               c_data[i][2] = c_data[i][2] - speed
               if c_data[i][2] < 0:
                   c_data.pop(i)
                   circles -= 1
                   circle_miss += 1
                   print(f"Circle missed {circle_miss}/3 ; Lives remaining {3-circle_miss}")
                   if circle_miss==3:
                       print(f"Game Over! Score: {score}")
                       game=False
                       break
                   i -= 1
               i += 1
   glutPostRedisplay()
 
def display():
   global s_position, circles, game, c_data, score, bullets
   glClear(GL_COLOR_BUFFER_BIT)
   # cross
   glColor3f(1.0, 0.0, 0.0)
   drawLine(455, 495, 495, 455)
   drawLine(455, 455, 495, 495)
 
   # pause
   global p_sign
   if p_sign == False:
       glColor3f(1.0, 0.8, 0.2)
       drawLine(240, 495, 240, 455)
       drawLine(260, 495, 260, 455)
   else:
       glColor3f(1.0, 0.8, 0.2)
       drawLine(230, 495, 270, 475)
       drawLine(230, 495, 230, 455)
       drawLine(230, 455, 270, 475)
 
   # restart
   glColor3f(0.2, 0.8, 0.9)
   drawLine(25, 495, 5, 475)
   drawLine(5, 475, 25, 455)
   drawLine(5, 475, 45, 475)
   
 
   if game:
       if circles==0:
           circle()
           circles=1
       else:
           if c_data[-1][2]<420:
               circle()
               circles+=1
 
       vanish_b = []
       vanish_c = []
       for i in range(len(c_data)):
           r_c = c_data[i][0]
           x_c = c_data[i][1]
           y_c = c_data[i][2]
           for j in range(len(bullets)):
               r_b, x_b, y_b = bullets[j]
               if (x_c - r_c) <= x_b <= (x_c + r_c) and (y_c - r_c) <= y_b <= (y_c + r_c):
                   score += 1
                   print("Score:", score)
                   vanish_b.append(j)
                   vanish_c.append(i)
           if (s_position+14)>=(x_c-r_c) and (s_position-14)<=(x_c+r_c) and (y_c-r_c)<=30:
               print(f"Crashed! \nGame Over! Score: {score}")
               game = False
               break
 
       for i in vanish_b:
           bullets.pop(i)
       for i in vanish_c:
           c_data.pop(i)
           circles -= 1
 

   shooter(s_position)
   animate()
   glutSwapBuffers()
 
def mouseListener(button, state, x, y):
   global score, pause, p_sign, speed, c_data, s_position, game, bullets, circles, bullet_miss, circle_miss
   if button==GLUT_LEFT_BUTTON:
       if state==GLUT_DOWN:
           if 455<x<495 and 455< (500-y) <495: #converting y coordinate
               print(f"Goodbye! Score: {score}")
               glutLeaveMainLoop()
           #pause
           elif 230<x<260 and 455<(500-y)<495:
               if pause == False:
                   pause = speed
                   speed = 0
                   p_sign = True
               else:
                   speed = pause
                   pause = False
                   p_sign = False
           #restart
           elif 5<x<45 and 455<(500-y)<495:
               print("Starting over!")
               game = True
               s_position = 250
               bullets = []
               circles = 0
               c_data = []
               score = 0
               circle_miss = 0
               bullet_miss = 0
               pause = False
               p_sign = False
 
   glutPostRedisplay()

def init():
   glutInit(sys.argv)
   glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
   glutInitWindowSize(500, 500)
   glutInitWindowPosition(0,0)
   glutCreateWindow(b"Assignment 3")
   glClearColor(0, 0, 0, 0)
   glOrtho(0, 500, 0, 500, 1, 0)
 
init()
glutDisplayFunc(display)
glutKeyboardFunc(keyboardListener)
glutMouseFunc(mouseListener)
glutMainLoop()