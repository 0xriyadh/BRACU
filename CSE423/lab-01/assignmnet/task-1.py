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
    glPointSize(2)
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glVertex2f(x, y + 1)
    glVertex2f(x, y + 2)
    glVertex2f(x, y + 3)
    glVertex2f(x, y + 4)
    glVertex2f(x, y + 5)
    glVertex2f(x, y + 6)
    glVertex2f(x, y + 7)
    glVertex2f(x, y + 8)
    glVertex2f(x, y + 9)
    glVertex2f(x, y + 10)
    glVertex2f(x, y + 11)
    glVertex2f(x, y + 12)
    glVertex2f(x, y + 13)
    glVertex2f(x, y + 14)
    glVertex2f(x, y + 15)
    glVertex2f(x, y + 16)
    glVertex2f(x, y + 17)
    glVertex2f(x, y + 18)
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

    """  
        1. Swap Buffers: When you draw using OpenGL in a double-buffered mode, all rendering operations are performed on a back buffer. The front buffer is what is currently being displayed on your screen. glutSwapBuffers() swaps the front and back buffers. This means that the back buffer, where the latest frame was drawn, becomes the front buffer and is displayed on the screen, and the previous front buffer becomes the new back buffer for the next round of drawing.
        
        2. Reduce Flickering: This buffer swapping is crucial for creating smooth animations because it ensures that only complete frames are displayed, reducing flickering and tearing that can occur if drawing directly to the display buffer.
        
        3. Synchronization: It also helps in synchronizing the display with the refresh rate of the monitor, which can further smooth out the animation.
    """
    glutSwapBuffers()


def animate():
    # codes for any changes in Models, Camera
    glutPostRedisplay()
    global rain_drops
    for i in range(len(rain_drops)):
        rain_drops[i][1] -= 1
        if rain_drops[i][1] < -250:
            rain_drops[i][1] = 250


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

wind = glutCreateWindow(b"Rainfall House")
init()

glutDisplayFunc(display)  # display callback function

# what you want to do in the idle time (when no drawing is occurring)
# Idle Function: The idle function (animate() in this case) is called when there are no other events to process, such as mouse or keyboard input. It's a way to continuously update the scene or perform animations when the application is idle.
# Inside the animate() function, glutPostRedisplay() is called to mark the current window as needing to be redisplayed. This triggers the display() function to be called, refreshing the window and updating the visual content.
for i in range(245, -250, -100):
    rain_drops.append([-200, i])
glutIdleFunc(animate)
# glutTimerFunc(10, animate, 0)

# glutMouseFunc(mouseListener)
# glutKeyboardFunc(keyboardListener)
# glutSpecialFunc(specialKeyListener)

glutMainLoop()  # The main loop of OpenGL
