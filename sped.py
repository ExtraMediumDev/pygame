import time
from pyexpat.errors import XML_ERROR_SUSPENDED
from opensimplex import *
import pygame
from pygame.locals import *
import random
import math

from OpenGL.GL import *
from OpenGL.GLU import *

# global variables list: FOV, display, Xposition, Yposition, Zposition

# functions list: Line2D, Line3D, Cuboid3D, render, controls, main, Cuboid3D.


# constants and variable init
display = (1200,700)
FOV = 500
Xposition = 0
Yposition = 0
Zposition = -100
YZangle = 0
XZangle = 0
XYangle = 0
YZSine = 0
XZSine = 0
XYSine = 0
YZCosine = 0
XZCosine = 0
XYCosine = 0
NewX = 0
NewY = 0
NewZ = 0
speed = 0.025
friction = 0.925
Xvelocity = 0
Yvelocity = 0
Zvelocity = 0
turnspeed = 0.01
gravity = 0.1
# Base functions
def controls():

    global Zposition
    global Xposition
    global Yposition
    global YZSine
    global XZSine
    global XYSine
    global YZCosine
    global XZCosine
    global XYCosine
    global YZangle
    global XZangle
    global XYangle
    global turnspeed
    global speed
    global friction
    global Xvelocity
    global Yvelocity
    global Zvelocity
    global gravity

    YZSine = math.sin(YZangle)
    XZSine = math.sin(XZangle)
    XYSine = math.sin(XYangle)
    YZCosine = math.cos(YZangle)
    XZCosine = math.cos(XZangle)
    XYCosine = math.cos(XYangle)
    
    

    
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        Xvelocity += speed * XZSine
        Zvelocity += speed * XZCosine
    if keys[pygame.K_a]:
        Xvelocity -= speed * XZCosine
        Zvelocity += speed * XZSine
    if keys[pygame.K_s]:
        Xvelocity -= speed * XZSine
        Zvelocity -= speed * XZCosine
    if keys[pygame.K_d]:
        Xvelocity += speed * XZCosine
        Zvelocity -= speed * XZSine
    if keys[pygame.K_e]:
        Yvelocity += speed
    if keys[pygame.K_q]:
        Yvelocity -= speed
    if keys[pygame.K_UP]:
        YZangle += turnspeed
        if YZangle > 1.5:
            YZangle = 1.5
    if keys[pygame.K_DOWN]:
        YZangle -= turnspeed
        if YZangle < -1.5:
            YZangle = -1.5
    if keys[pygame.K_RIGHT]:
        XZangle += turnspeed
    if keys[pygame.K_LEFT]:
        XZangle -= turnspeed
    if keys[pygame.K_EQUALS]:
        XYangle += turnspeed
    if keys[pygame.K_MINUS]:
        XYangle -= turnspeed

    Xposition += Xvelocity
    Yposition += Yvelocity
    Zposition += Zvelocity
    Xposition *= friction
    Zposition *= friction
    Yposition *= friction
    

def Line2D(x1, y1, x2, y2):
    glBegin(GL_LINES )
    glVertex2f(x1/display[0], y1/display[1]);
    glVertex2f(x2/display[0], y2/display[1]);
    glEnd()

def Transform(x,y,z):
    global NewX
    global NewY
    global NewZ
    NewX = x * XZCosine - z * XZSine
    NewZ = x * XZSine + z * XZCosine
    NewY = y * YZCosine - NewZ * YZSine
    NewZ = y * YZSine + NewZ * YZCosine
    temp = NewX
    NewX = NewX * XYCosine - NewY * XYSine
    NewY = temp * XYSine + NewY * XYCosine

def Line3D(x1, y1, z1, x2, y2, z2):
    global NewX
    global NewY
    global NewZ
# Determine Position
    Transform(x1 - Xposition, y1 - Yposition, z1 - Zposition)
    x_coord1 = NewX
    y_coord1 = NewY
    z_coord1 = NewZ
    Transform(x2 - Xposition, y2 - Yposition, z2 - Zposition)
    x_coord2 = NewX
    y_coord2 = NewY
    z_coord2 = NewZ
# Check if pass Z-clipping plane
    z_boolean1 = z_coord1 <= 0
    z_boolean2 = z_coord2 <= 0

# Simple Z-clip
    if z_boolean1 == True or z_boolean2 == True:
        if z_boolean1 == True:
                z_coord1 = 0.1
        if z_boolean2 == True:
                z_coord2 = 0.1

# Converts to 2D and draws
    Line2D(FOV*x_coord1/z_coord1, FOV*y_coord1/z_coord1, FOV*x_coord2/z_coord2, FOV*y_coord2/z_coord2)

# 3D Shapes
def Cuboid3D(x, y, z, sizeX, sizeY, sizeZ, xzrot):

    def vertice(xyz, sign, sizeXYZ, trig): return xyz + sign*(sizeXYZ/2)*trig


# Vertical Edges for Y-plane
    Line3D(vertice(x,1,sizeX,math.cos(xzrot)), 
           vertice(y,1,sizeY,1), 
           vertice(z,1,sizeZ,math.sin(xzrot)), 
           vertice(x,1,sizeX,math.cos(xzrot)), 
           vertice(y,-1,sizeY,1), 
           vertice(z,1,sizeZ,math.sin(xzrot)))

    Line3D(vertice(x,-1,sizeX,math.sin(xzrot)), 
           vertice(y,1,sizeY,1), 
           vertice(z,1,sizeZ,math.cos(xzrot)), 
           vertice(x,-1,sizeX,math.sin(xzrot)), 
           vertice(y,-1,sizeY,1), 
           vertice(z,1,sizeZ,math.cos(xzrot)))

    Line3D(vertice(x,-1,sizeX,math.cos(xzrot)), 
           vertice(y,1,sizeY,1), 
           vertice(z,-1,sizeZ,math.sin(xzrot)), 
           vertice(x,-1,sizeX,math.cos(xzrot)), 
           vertice(y,-1,sizeY,1), 
           vertice(z,-1,sizeZ,math.sin(xzrot)))

    Line3D(vertice(x,1,sizeX,math.sin(xzrot)), 
           vertice(y,1,sizeY,1), 
           vertice(z,-1,sizeZ,math.cos(xzrot)), 
           vertice(x,1,sizeX,math.sin(xzrot)), 
           vertice(y,-1,sizeY,1), 
           vertice(z,-1,sizeZ,math.cos(xzrot)))

# Horizontal Edges for Z-plane
    Line3D(vertice(x,1,sizeX,math.sin(xzrot)), 
           vertice(y,1,sizeY,1), 
           vertice(z,-1,sizeZ,math.cos(xzrot)), 
           vertice(x,1,sizeX,math.cos(xzrot)), 
           vertice(y,1,sizeY,1), 
           vertice(z,1,sizeZ,math.sin(xzrot)))
    
    Line3D(vertice(x,-1,sizeX,math.cos(xzrot)), 
           vertice(y,1,sizeY,1), 
           vertice(z,-1,sizeZ,math.sin(xzrot)), 
           vertice(x,-1,sizeX,math.sin(xzrot)), 
           vertice(y,1,sizeY,1), 
           vertice(z,1,sizeZ,math.cos(xzrot)))

    Line3D(vertice(x,1,sizeX,math.sin(xzrot)), 
           vertice(y,-1,sizeY,1), 
           vertice(z,-1,sizeZ,math.cos(xzrot)), 
           vertice(x,1,sizeX,math.cos(xzrot)), 
           vertice(y,-1,sizeY,1), 
           vertice(z,1,sizeZ,math.sin(xzrot)))
    
    Line3D(vertice(x,-1,sizeX,math.cos(xzrot)), 
           vertice(y,-1,sizeY,1), 
           vertice(z,-1,sizeZ,math.sin(xzrot)), 
           vertice(x,-1,sizeX,math.sin(xzrot)), 
           vertice(y,-1,sizeY,1), 
           vertice(z,1,sizeZ,math.cos(xzrot)))       
    
# Horizontal Edges for X-plane

    Line3D(vertice(x,-1,sizeX,math.cos(xzrot)), 
           vertice(y,1,sizeY,1), 
           vertice(z,-1,sizeZ,math.sin(xzrot)), 
           vertice(x,1,sizeX,math.sin(xzrot)), 
           vertice(y,1,sizeY,1), 
           vertice(z,-1,sizeZ,math.cos(xzrot)))

    Line3D(vertice(x,-1,sizeX,math.cos(xzrot)), 
           vertice(y,-1,sizeY,1), 
           vertice(z,-1,sizeZ,math.sin(xzrot)), 
           vertice(x,1,sizeX,math.sin(xzrot)), 
           vertice(y,-1,sizeY,1), 
           vertice(z,-1,sizeZ,math.cos(xzrot)))

    Line3D(vertice(x,-1,sizeX,math.sin(xzrot)), 
           vertice(y,1,sizeY,1), 
           vertice(z,1,sizeZ,math.cos(xzrot)), 
           vertice(x,1,sizeX,math.cos(xzrot)), 
           vertice(y,1,sizeY,1), 
           vertice(z,1,sizeZ,math.sin(xzrot)))

    Line3D(vertice(x,-1,sizeX,math.sin(xzrot)), 
           vertice(y,-1,sizeY,1), 
           vertice(z,1,sizeZ,math.cos(xzrot)), 
           vertice(x,1,sizeX,math.cos(xzrot)), 
           vertice(y,-1,sizeY,1), 
           vertice(z,1,sizeZ,math.sin(xzrot)))


# Main Render Function

mapx = 10
mapy = 10

seed(1234)
map = []
for x in range(mapx):
    new = []
    for y in range(mapy):
        n = noise2(x=x, y=y)
        new.append(abs(n))
    map.append(new)

def render():
    for x in range(mapx):
        for y in range(mapy):
            Cuboid3D(x*10,map[x][y]*10,y*5,7,map[x][y]*20,7,0)



# Master loop
def main():
    pygame.init()
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        controls()
        render()
        glLineWidth(2)

        pygame.display.flip()
        pygame.time.wait(1)



# Program Run
main()
