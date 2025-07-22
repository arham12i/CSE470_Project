from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from math import *
import random

W_Width, W_Height = 500, 500
ballx = bally = 0
speed = 0.01
ball_size = 2
create_new = False
points = []
blinking = False
frozen = False
blink_counter = 0

class MovablePoint:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.dx = random.choice([-1, 1])
        self.dy = random.choice([-1, 1])
        self.color = (random.random(), random.random(), random.random())
        self.visible = True

def crossProduct(a, b):
    result = point()
    result.x = a.y * b.z - a.z * b.y
    result.y = a.z * b.x - a.x * b.z
    result.z = a.x * b.y - a.y * b.x
    return result

def convert_coordinate(x, y):
    global W_Width, W_Height
    a = x - (W_Width / 2)
    b = (W_Height / 2) - y 
    return a, b

def draw_points(x, y, s):
    glPointSize(s)
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()

def animate():
    global points, blink_counter, frozen, blinking

    if frozen:
        glutPostRedisplay()
        return

    for p in points:
        if p.x + ball_size >= h or p.x - ball_size <= -h:
            p.dx *= -1
        if p.y + ball_size >= h or p.y - ball_size <= -h:
            p.dy *= -1
        p.x += p.dx * speed * 100
        p.y += p.dy * speed * 100

        if blinking:
            if blink_counter % 100 < 30:
                p.visible = True
            else:
                p.visible = False
        else:
            p.visible = True

    blink_counter = (blink_counter + 1) % 100
    glutPostRedisplay()

def drawBox():
    size = h
    glBegin(GL_LINE_LOOP)
    glColor3f(1.0, 1.0, 1.0)
    glVertex2f(-size, -size)
    glVertex2f(size, -size)
    glVertex2f(size, size)
    glVertex2f(-size, size)
    glEnd()

def display():
    global points
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(0, 0, 0, 1)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(0, 0, 500, 0, 0, 0, 0, 1, 0)
    glMatrixMode(GL_MODELVIEW)

    drawBox()

    if create_new:
        glColor3f(1, 0, 0)
        draw_points(create_new[0], create_new[1], ball_size)

    for p in points:
        if p.visible:
            glColor3f(*p.color)
        else:
            glColor3f(0, 0, 0)
        draw_points(p.x, p.y, ball_size)

    glutSwapBuffers()
    glutPostRedisplay()

def mouseListener(button, state, x, y):
    global ballx, bally, create_new, points, blinking

    if button == GLUT_LEFT_BUTTON:
        if state == GLUT_DOWN:
            c_X, c_Y = convert_coordinate(x, y)
            ballx, bally = c_X, c_Y
            blinking = not blinking

    if button == GLUT_RIGHT_BUTTON:
        if state == GLUT_DOWN:
            create_new = convert_coordinate(x, y)
            points.append(MovablePoint(create_new[0], create_new[1]))
            create_new = False

    glutPostRedisplay()

def specialKeyListener(key, x, y):
    global speed
    if key == GLUT_KEY_UP:
        speed *= 2
    elif key == GLUT_KEY_DOWN:
        speed /= 2
    glutPostRedisplay()

def keyboardListener(key, x, y):
    global frozen
    if key == b' ':
        frozen = not frozen
    glutPostRedisplay()

def init():
    global h
    glEnable(GL_DEPTH_TEST)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(104, 1, 1, 1000.0)

    d = 500
    half_fov_rad = radians(104 / 2)
    h = d * tan(half_fov_rad)

def main():
    glutInit()
    glutInitWindowSize(W_Width, W_Height)
    glutInitWindowPosition(100, 100)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutCreateWindow(b"Task 2 - Amazing Box")
    init()
    glutDisplayFunc(animate)
    glutIdleFunc(display)
    glutMouseFunc(mouseListener)
    glutKeyboardFunc(keyboardListener)
    glutSpecialFunc(specialKeyListener)
    glutMainLoop()

if __name__ == "__main__":
    main()
