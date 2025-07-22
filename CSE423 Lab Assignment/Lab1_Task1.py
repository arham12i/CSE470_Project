from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from math import *
import random

rain_drops = []
rain_speed = 10
rain_bend = 2
max_rain = 1000
bg_brightness = 0.0
lightning_flash = 0.0
is_day = False


def drawRoof():
    glBegin(GL_TRIANGLES)
    glColor3f(0.4, 0.7, 1.0)
    glVertex2d(-100, 60)
    glVertex2d(0, 150)
    glVertex2d(100, 60)
    glEnd()

def drawWall():
    glBegin(GL_TRIANGLES)
    glColor3f(1.0, 1.0, 1.0)
    glVertex2d(-80, -60)
    glVertex2d(80, -60)
    glVertex2d(80, 60)
    glVertex2d(-80, -60)
    glVertex2d(80, 60)
    glVertex2d(-80, 60)
    glEnd()

def drawDoor():
    door_width = 40
    door_height = 80
    door_bottom_y = -60
    door_top_y = door_bottom_y + door_height

    glBegin(GL_TRIANGLES)
    glColor3f(0.4, 0.7, 1.0)
    glVertex2d(-door_width // 2, door_bottom_y)
    glVertex2d(door_width // 2, door_bottom_y)
    glVertex2d(door_width // 2, door_top_y)
    glVertex2d(-door_width // 2, door_bottom_y)
    glVertex2d(door_width // 2, door_top_y)
    glVertex2d(-door_width // 2, door_top_y)
    glEnd()

def drawDoorHandle():
    glPointSize(6)
    glBegin(GL_POINTS)
    glColor3f(0.0, 0.0, 0.0)
    glVertex2f(15, -20)
    glEnd()

def drawWindows():
    window_width = 30
    window_height = 30
    offset = 40
    bottom_y = -10
    top_y = bottom_y + window_height
    
    # Left window
    glColor3f(0, 0, 0)
    glBegin(GL_LINES)
    glVertex2d(-offset - window_width // 2, bottom_y)
    glVertex2d(-offset - window_width // 2, top_y)
    glVertex2d(-offset - window_width, bottom_y + window_height // 2)
    glVertex2d(-offset, bottom_y + window_height // 2)
    glEnd()

    glBegin(GL_TRIANGLES)
    glColor3f(0.4, 0.7, 1.0)
    glVertex2d(-offset - window_width, bottom_y)
    glVertex2d(-offset, bottom_y)
    glVertex2d(-offset, top_y)
    glVertex2d(-offset - window_width, bottom_y)
    glVertex2d(-offset, top_y)
    glVertex2d(-offset - window_width, top_y)
    glEnd()

    # Right window
    glColor3f(0, 0, 0)
    glBegin(GL_LINES)
    glVertex2d(offset + window_width // 2, bottom_y)
    glVertex2d(offset + window_width // 2, top_y)
    glVertex2d(offset, bottom_y + window_height // 2)
    glVertex2d(offset + window_width, bottom_y + window_height // 2)
    glEnd()
    
    glBegin(GL_TRIANGLES)
    glColor3f(0.4, 0.7, 1.0)
    glVertex2d(offset, bottom_y)
    glVertex2d(offset + window_width, bottom_y)
    glVertex2d(offset + window_width, top_y)
    glVertex2d(offset, bottom_y)
    glVertex2d(offset + window_width, top_y)
    glVertex2d(offset, top_y)
    glEnd()

def drawBackgroundTrees():
    for x in range(-300, 300, 30):
        glBegin(GL_TRIANGLES)
        glColor3f(0.0, 1.0, 0.0)
        glVertex2f(x, 60)
        glVertex2f(x + 15, 120)
        glVertex2f(x + 30, 60)
        glEnd()

def drawBackground():
    glBegin(GL_TRIANGLES)
    glColor3f(0.4, 0.26, 0.13)
    glVertex2d(-300, -300)
    glVertex2d(300, -300)
    glVertex2d(300, 90)
    glVertex2d(-300, -300)
    glVertex2d(300, 90)
    glVertex2d(-300, 90)
    glEnd()

def drawRain():
    glPointSize(2)
    glBegin(GL_POINTS)
    glColor(0.5, 0.7, 1.0)
    for drop in rain_drops:
        glVertex2f(drop[0], drop[1])
    glEnd()

def updateRain():
    global rain_drops
    for drop in rain_drops:
        drop[0] += rain_bend
        drop[1] -= rain_speed
        if drop[1] < -280:
            drop[0] = random.randint(-250, 250)
            drop[1] = random.randint(100, 250)
    glutPostRedisplay()

def keyboard(key, x, y):
    global is_day, lightning_flash
    key = key.decode('utf-8')
    if key == 'd':
        is_day = True
        lightning_flash = 1.0
    elif key == 'n':
        is_day = False
        lightning_flash = 1.0

def specialKeys(key, x, y):
    global rain_bend
    if key == GLUT_KEY_LEFT:
        rain_bend -= 0.3
    elif key == GLUT_KEY_RIGHT:
        rain_bend += 0.3


def display():
    global bg_brightness, lightning_flash

    if is_day:
        bg_brightness = min(bg_brightness + 0.01, 1.0)
    else:
        bg_brightness = max(bg_brightness - 0.01, 0.0)

    if lightning_flash > 0:
        glClearColor(1.0, 1.0, 1.0, 1.0)
        lightning_flash -= 0.02
    else:
        glClearColor(0.0, 0.0, bg_brightness, 1.0)

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(0, 0, 200, 0, 0, 0, 0, 1, 0)

    drawWindows()
    drawRoof()
    drawDoorHandle()
    drawDoor()
    drawWall()
    drawRain()
    drawBackgroundTrees()
    drawBackground()

    glutSwapBuffers()
    glutPostRedisplay()

def init():
    glEnable(GL_DEPTH_TEST)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(104, 1, 1, 1000.0)

    for i in range(0, max_rain):
       x = random.randint(-250, 250)
       y = random.randint(0, 250)
       rain_drops.append([x, y])

    glutIdleFunc(updateRain)


def main():
    glutInit()
    glutInitWindowSize(500, 500)
    glutInitWindowPosition(50, 100)
    glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB)
    glutCreateWindow(b"Task 1 - House with Raindrop")
    init()
    glutDisplayFunc(display)
    glutKeyboardFunc(keyboard)
    glutSpecialFunc(specialKeys)
    glutMainLoop()

if __name__ == "__main__":
    main()