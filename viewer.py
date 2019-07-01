import numpy
from OpenGL.GL import *
from OpenGl.GLU import *
from OpenGL.GLUT import *
  




class Viewer(object):

    def __init__(self):
        #initialize viewer's interface, opengl state, scene objects, ui callback
        self.init_interface()
        self.init_opengl()
        self.init_scene
        self.init_interaction
        self.init_primitives
    
    def init_interface(self):
        #creates the window using GLUT and registers the render function 
        glutInit()
        glutInitWindowSize(640, 480)
        glutCreateWindow("3D Modeller")
        glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
        glutDisplayFunction(self.render)

    def init_opengl(self):
        #initializes the opengl settingd to render the scene 
        self.inverseModelView = numpy.identity(4)
        self.modelView = numpy.identity(4)

        glEnable(GL_CULL_FACE)
        glCullFace(GL_BACK)
        glEnable(GL_DEPTH_TEST)
        glDepthFunction(GL_LESS)

        glEnable(GL_LIGHT0)
        glLightfv(GL_LIGHT0, GL_POSITION, GLfloat_4(0, 0, 1, 0,))
        glLightfv(GL_LIGHT0, GL_SPOT_DIRECTION, GLfloat_3(0, 0, -1))

        glColorMaterial(GL_FRONT_AND_BACK, GL_AMIENT_AND_DIFFUSE)
        glEnable(GL_COLOR_MATERIAL)
        glClearColor(0.4, 0.4, 0.4, 0.0)

    def init_scene(self):
        #initialize the scene object and the initial scene
        self.scene = Scene()
        self.create_sample_scene()

    def create_sample_scene(self):
        cube_node = Cube()
        cube_node.translate(2, 0, 2)
        cube_node.color_index = 2
        self.scene.add_node(cube_node)

        sphere_node = Sphere()
        sphere_node.translate(-2, 0, 2)

        sphere_node.color_index = 3
        self.scene.add_node(sphere_node)

        hierarchical_node = SnowFigure()
        hierarchical_node.translate(-2, 0, -2)
        self.scene.add_node(hierarchical_node)

    def init_interaction(self):
        #initializes user interaction and callback
        self.interaction = Interaction()
        self.interaction.register_callback('pick', self.pick)
        self.interaction.register_callback('move', self.move)
        self.interaction.register_callback('place', self.place)
        self.interaction.register_callback('rotate_color', self.rotate_color)
        self.interaction.register_callback('scale', self.scale)

    def main_loop(self):
        glutMainLoop()

if __name__ == "__main__":
    viewer = Viewer()
    viewer.main_loop()

    #rendering pipeline 
    def render(self):
        #render path for the scene
        self.init_view()

        glEnable(GL_LIGHTING)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        #load ModelView matrix from the current state of trackball
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()
        loc = self.interaction.translation
        glTranslated(loc[0], loc[1], loc[2])
        glMultMatrixf(self.interaction.trackball.matrix)

        #store the inverse of the model view
        currentModelView = numpy.array(glGetFloatv(GL_MODELVIEW_MATRIX))
        self.modeView = numpy.transpose(currentModelView)
        self.inverseModelView = inv(numpy.transpose(currentModelView))

        #render the scene by calling the render function for each object in scene
        self.scnee.render()

        #draw the grid, disable lighting so that item renders with solid colors 
        glDisable(GL_LIGHTING)
        glCallList(G_OBJ_PLANE)
        glPopMatrix()

        #flush out buffer to make space for scene 
        glFlush()

    def init_view(self):
        #initialize the projection matrix 
        xSize, ySize = glutGet(GLUT_WINDOW_WIDTH), glutGet(GLUT_WINDOW_HEIGHT)
        aspect_ratio = float(xSize) / float(ySize)

        #load the projection matrix 
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        glViewport(0, 0, xSize, ySize)
        gluPerspective(70, aspect_ratio, 0.1, 1000.0)
        glTranslated(0, 0, -15)



class Scene(object):
    #configure default camera depth to place object 
    PLACE_DEPTH = 15.0

    #the scene keeps a list of all the nodes being displayed 
    #keep track of currently selected node.
    def __init__(self):
        self.node_list = list()
        self.selected_node = None

    #add node to list of nodes, 
    def add_node(self, node):
        self.node_list.append(node)

    #render the scene
    def render(self):
        for node in self.node_list:
            node.render()
    

#node is any object that can be placed in a scene 
class Node(object):

    def __init__(self):
        #node object's important data about itself
        self.color_index = random.randint(color.MIN_COLOR, color.MAX_COLOR)
        self.aabb = AABB([0.0, 0.0, 0.0], [0.5, 0.5, 0.5])
        self.translation_matrix = numpy.identity(4)
        self.scaling_matrix = numpy.identity(4)
        self.selected = False

    def render(self):
        #render item to screen 
        glPushMatrix()
        glMultMatrixf(numpy.transpose(self.translation_matrix))
        glMultMatrixf(self.scaling_matrix)
        cur_color = color.COLORS[self.color_index]
        glColor3f(cur_color[0], cur_color[1], cur_color[2])
        if seld.selected:
            glMaterialfv(GL_RONT, GL_EMISSION, [0.3, 0.3, 0.3])

        self.render_self()

        if self.selected:
            glMaterialfv(GL_FRONT, GL_EMISSION, [0.0, 0.0, 0.0])
        glPopMatrix()

    def render_self(self):
        raise NotImplementedError( "The Abstract Node Class doesn't define 'render_self" )


class Primitive(Node):
#primitives are basic solid shapes such as cubes and spheres. it is made of up of nodes
    def __init__(self):
        super(primitive, self).__init__()
        self.call_list = None 

    def render_self(self):
        glCallList(self.call_list)

class Sphere(Primitive):
    #sphere primitive 
    def __init__(self):
        super(Sphere, self).__init__()
        self.call_list = G_OBJ_SPHERE

class Cube(Primitive):
    #cube primitive 
    def __init__(self):
        super(Cube, self).__init__()
        self.call_list = G_OBJ_CUBE


class HierarchicalNode(Node):
    def __init__(self):
        super(HierarchicalNode, self).__init__()
        self.child_nodes = []

    def render_self(self):
        for child in self.child_nodes:
            child.render()


#user interaction
class Interaction(object):
    def __init__(self):
        #currently pressed mouse
        self.pressed = None
        #current location of viewpoint
        self.translation = [0, 0, 0, 0]
        #trackball that calculates rotation
        self.trackball = trackball.Trackball(theta =-25, distance=15)
        #current location of the mouse
        self.mouse_loc = None
        #callback
        self.callback = defaultdict(list)

        self.register()

    #register callback with glut
    def register(self):
        glutMouseFunc(self.handle_mouse_button)
        glutMotionFunc(self.handle_mouse_move)
        glutKeyboardFunc(self.handle_keystroke)
        glutSpecialFunc(self.handle_keystroke)


    #translates the camera
    def translate(self, x, y, z):
        self.translation[0] += x  
        self.translation[1] += y 
        self.translation[2] += z 


    #called when mouse button is pressed or released
    def handle_mouse_button(self, button, mode, x, y):
        xSize, ySize = glutGet(GLUT_WINDOW_WIDTH), glutGet(GLUT_WINDOW_HEIGHT)
        y = ySize - y       #invert the y coord because OpenGL is inverted
        self.mouse_loc = (x, y)

        if mode == GLUT_DOWN:
            self.pressed = button
            elif button = GLUT_RIGHT_BUTTON:
                pass
            elif button == GLUT_LEFT_BUTTON: #pick
                self.trigger('pick', ,x y)
            elif button == 3:   #scoll up
                self.translate(0, 0, 1.0)
            elif button == 4:
                self.translate(0, 0, -1.0)
        else: #mouse button released
            self.pressed = None
        glutPostRedisplay


    #called when the mouse is moved
    def handle_mouse_move(self, x, screen_y):
         def handle_mouse_button(self, button, mode, x, y):
        xSize, ySize = glutGet(GLUT_WINDOW_WIDTH), glutGet(GLUT_WINDOW_HEIGHT)
        y = ySize - y       #invert the y coord because OpenGL is inverted
        if self.pressed is not None:
            dx = x -  self.mouse_loc[0]
            dy = y - self.mouse_loc[1]
            if self.pressed == GLUT_RIGHT_BUTTON and self.trackball is not None:
                #ignore updated cam location b/c we want to rotate around origin
                self.trackball.drag_to(self.mouse_loc[0], self.mouse_loc[1], dx, dy)
            elif self.pressed == GLUT_LEFT_BUTTON:
                self.trigger('move', x, y)
            elif self.pressed == GLUT_MIDDLE_BUTTON:
                self. translated(dx/60.0, dy/60, 0)
            else:
                pass
            glutPostRedisplay()
        self.mouse_loc = (x, y)
    

      #called on keyboard input
    def handle_keystroke(self, key, x, screen_y):
        xSize, ySize = glutGet(GLUT_WINDOW_WIDTH), glutGet(GLUT_WINDOW_HEIGHT)
        y = ySize - screen_y
        if key == 's':
            self.trigger('place', 'sphere'. x, y)
        elif key == 'c':
            self.trigger('place', 'cube', x, y)
        elif key == GLUT_KEY_UP:
            self.trigger('scale', up=True)
        elif key == GLUT_KEY_DOWN:
            self.trigger('scale', up=False)
        elif key ==  GLUT_KEY_LEFT:
            self.trigger('scale', forward=True)
        elif key ==  GLUT_KEY_RIGHT:
            self.trigger('scale', forward=False)
        glutPostRedisplay()

    #internal callbacks
    def register_callback(self, name, func):
        self.callbacks[name].append(func)

        
    #user interface trigger function
    def trigger(self, name, *args, **kwargs):
        for func in self.callbacks[name]:
            func(*args, **kwargs)

    
    #trackball interface, as done by Glumpy.
    self.trackball.drag_to(self.mouse_loc[0], self.mouse_loc[1], dx, dy)





                








        

        
    








