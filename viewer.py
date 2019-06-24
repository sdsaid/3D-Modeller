import numpy
import OpenGL.GL 
import OpenGl.GLU 



class Viewer(object):

    def __init__(self):
        #initialize viewer's interface, opengl state, scene objects, ui callback
        self.init_interface()
        self.init_opengl()
        self.init_scene
        self.init_interaction
        self.init_primitives()
    
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

    def init_scene():
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
        self.interaction = Interactio()
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


#primitives are basic solid shapes such as cubes and spheres. it is made of up of nodes
class Primitive(Node):
    def __init__(self):
        super(primiitive, self).__init__()
        self.call_list = Nine 

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
        super(Sphere, self).__init__()
        self.call_list = G_OBJ_CUBE

        







