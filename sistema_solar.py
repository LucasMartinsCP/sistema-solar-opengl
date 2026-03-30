from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from PIL import Image
import random
import sys
import math

width, height = 800, 600
saturn_ring_angle = 0.0

planet_data = [
    {"name": "Mercúrio", "distance": 2, "size": 0.2, "speed": 4.15},
    {"name": "Vênus",    "distance": 3, "size": 0.3, "speed": 1.62},
    {"name": "Terra",    "distance": 4, "size": 0.35, "speed": 1.0},
    {"name": "Marte",    "distance": 5, "size": 0.25, "speed": 0.53},
    {"name": "Júpiter",  "distance": 7, "size": 0.7, "speed": 0.08},
    {"name": "Saturno",  "distance": 9, "size": 0.6, "speed": 0.03},
    {"name": "Urano",    "distance": 11, "size": 0.5, "speed": 0.012},
    {"name": "Netuno",   "distance": 13, "size": 0.5, "speed": 0.006}
]

# Controle de rotação
planet_angles = [0.0 for _ in planet_data]
planet_self_rotation = [0.0 for _ in planet_data]
moon_orbit_angle = 0.0
moon_self_rotation = 0.0

textures = {}

# Geração de estrelas
num_stars = 2000
stars = [(random.uniform(-50, 50), random.uniform(-50, 50), random.uniform(-50, 50)) for _ in range(num_stars)]

def encerrar(value):
    print("Encerrando a simulação após 50 segundos.")
    glutLeaveMainLoop()


def load_texture(filename):
    image = Image.open(filename)
    image = image.transpose(Image.FLIP_TOP_BOTTOM)
    img_data = image.convert("RGB").tobytes()
    width, height = image.size

    texture_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture_id)

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, img_data)
    return texture_id

def draw_stars():
    glPushAttrib(GL_ALL_ATTRIB_BITS)
    glDisable(GL_LIGHTING)
    glDisable(GL_TEXTURE_2D)
    glPointSize(2.0)
    glColor3f(1.0, 1.0, 1.0)  # Branco
    glBegin(GL_POINTS)
    for star in stars:
        glVertex3f(*star)
    glEnd()
    glPopAttrib()

def draw_ring(inner_radius, outer_radius, texture_id, segments=100):
    glPushAttrib(GL_ALL_ATTRIB_BITS)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glColor4f(1.0, 1.0, 1.0, 1.0)

    glBegin(GL_QUAD_STRIP)
    for i in range(segments + 1):
        angle = 2.0 * math.pi * i / segments
        cos_a = math.cos(angle)
        sin_a = math.sin(angle)

        x_inner = inner_radius * cos_a
        z_inner = inner_radius * sin_a
        x_outer = outer_radius * cos_a
        z_outer = outer_radius * sin_a

        tex_coord = i / segments  # valor de 0 a 1 ao longo do círculo

        glTexCoord2f(tex_coord, 0.0)
        glVertex3f(x_inner, 0.0, z_inner)

        glTexCoord2f(tex_coord, 1.0)
        glVertex3f(x_outer, 0.0, z_outer)
    glEnd()
    glPopAttrib()

def draw_sphere(radius, texture_id):
    glPushMatrix()
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glRotatef(-90, 1, 0, 0)
    quad = gluNewQuadric()
    gluQuadricTexture(quad, GL_TRUE)
    gluQuadricNormals(quad, GLU_SMOOTH)
    gluSphere(quad, radius, 30, 30)
    gluDeleteQuadric(quad)
    glPopMatrix()

def init():
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_COLOR_MATERIAL)
    glEnable(GL_NORMALIZE)
    glShadeModel(GL_SMOOTH)
    glEnable(GL_TEXTURE_2D)

    global textures
    textures = {
        "Sol":      load_texture("img/sol.jpg"),
        "Mercúrio": load_texture("img/mercurio.jpg"),
        "Vênus":    load_texture("img/venus.jpg"),
        "Terra":    load_texture("img/terra.jpg"),
        "Lua":      load_texture("img/lua.jpg"),
        "Marte":    load_texture("img/marte.jpg"),
        "Júpiter":  load_texture("img/jupiter.jpg"),
        "Saturno":  load_texture("img/saturno.jpg"),
        "Urano":    load_texture("img/urano.jpg"),
        "Netuno":   load_texture("img/netuno.jpg"),
        "Aneis":    load_texture("img/aneis_saturno.png"),
    }

def draw_scene():
    global planet_angles, moon_orbit_angle, moon_self_rotation, planet_self_rotation
    global saturn_ring_angle
    saturn_ring_angle += 0.3

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    gluLookAt(0, 5, 25, 0, 0, 0, 0, 1, 0)

    draw_stars()

    # Sol
    glPushMatrix()
    draw_sphere(1.0, textures["Sol"])
    glPopMatrix()

    # Planetas
    for i, planet in enumerate(planet_data):
        glPushMatrix()
        planet_angles[i] += planet["speed"] * 3.0
        planet_self_rotation[i] += 5.0

        # Translação
        glRotatef(planet_angles[i], 0.0, 1.0, 0.0)
        glTranslatef(planet["distance"], 0.0, 0.0)

        # Rotação própria
        glRotatef(planet_self_rotation[i], 0.0, 1.0, 0.0)

        draw_sphere(planet["size"], textures[planet["name"]])

        # Lua da Terra
        if planet["name"] == "Terra":
            glPushMatrix()
            moon_orbit_angle += 8.0
            moon_self_rotation += 6.0
            glRotatef(moon_orbit_angle, 0.0, 1.0, 0.0)
            glTranslatef(0.8, 0.0, 0.0)
            glRotatef(moon_self_rotation, 0.0, 1.0, 0.0)
            draw_sphere(0.1, textures["Lua"])
            glPopMatrix()

        # Anéis de Saturno
        if planet["name"] == "Saturno":
            glPushMatrix()
            glRotatef(saturn_ring_angle, 0.0, 1.0, 0.0)
            glRotatef(20, 1.0, 0.0, 0.0)  
            draw_ring(0.8, 1.3, textures["Aneis"])
            glPopMatrix()

        glPopMatrix()

    glutSwapBuffers()

def update(value):
    glutPostRedisplay()
    glutTimerFunc(33, update, 0)

def reshape(w, h):
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, w / h, 1, 100)
    glMatrixMode(GL_MODELVIEW)

def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(width, height)
    glutCreateWindow("Sistema Solar com Texturas - PyOpenGL")
    init()
    glutDisplayFunc(draw_scene)
    glutReshapeFunc(reshape)
    glutTimerFunc(33, update, 0)
    glutTimerFunc(50000, encerrar, 0)  # Encerra após 50 segundos
    glutMainLoop()

if __name__ == "__main__":
    main()
