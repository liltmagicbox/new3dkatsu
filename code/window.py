from glfw.GLFW import *
from OpenGL.GL import *
from time import perf_counter,time
#https://www.glfw.org/docs/latest/group__context.html

from window_keymap import keymap
#key_map = {    256:'esc',}


#this was way to window.callback_.. access.
def callback_key(self, key, scancode, action, mods):
    #print(key,scancode,action,mods)  # key a:65 1:49/ mods 0 1 2 4 "" shift ctrl alt
    if not key in keymap:
        return
    self.put_input( keymap[key] ,action)

def callback_button(self, button,action,mods):
    #print(button,action) #0 left 1 right , action 1 clicked.
    if not button in keymap:
        return
    if not self.cursor_locked:
        if action:
            self.activate()
        else:
            self.deactivate()
    self.put_input( keymap[button] ,action)

def callback_pos(self, xpos,ypos):
    if not self.active:
        return
    self.cursor_pos = xpos,ypos
    self.cursor_changed = True

def callback_fbsize(self, width,height):
    glViewport(0, 0, width, height)
    #print('fbsize',width,height)

def callback_enter(self, enter):
    if not enter:
        self.set_cursor_lock(False)

class Window:
    def __init__(self, size=(640,480), title='a window'):
        glfwInit()
        width,height = size
        window = glfwCreateWindow(width, height, title, None, None)
        glfwMakeContextCurrent(window) #for glfw?
        glfwSwapInterval(1)#x1 x2 x3.. 2 60hz->30hz. 0 fullspd.

        #glfwFocusWindow(window) mouse to be snached!
        glfwSetWindowSizeLimits(window, 100,100, GLFW_DONT_CARE,GLFW_DONT_CARE)

        glEnable(GL_DEPTH_TEST)
        #===
        self.window = window

        self.inputs = []
        #pos = glfwGetCursorPos(window)
        self.cursor_pos = 0,0
        self.cursor_before = 0,0
        self.cursor_changed = False
        self.keymap = {}
        self.active = False
        self.cursor_locked = False

        self.bind_callback('key',callback_key)
        self.bind_callback('pos',callback_pos)
        self.bind_callback('button',callback_button)
        self.bind_callback('fbsize',callback_fbsize)
        self.bind_callback('enter',callback_enter)



    def glClearColor(self,r,g,b,a):
        glClearColor(r,g,b,a)
    def glPointSize(self,size):
        glPointSize(size)
    def __getattr__(self,name):
        if name.startswith('gl'):
            return globals().get(name)
        raise AttributeError
    #===set family.
    def set_title(self, title):
        glfwSetWindowTitle(self.window, title)

    def set_size(self, size):
        width,height = size
        glfwSetWindowSize(self.window, width,height)
    def get_size(self):
        "for pixel-accuracy. see https://www.glfw.org/docs/latest/window_guide.html"
        #glfwGetWindowContentScale(self.window) #what if dpi?
        return glfwGetFramebufferSize(self.window)
    def set_ratio(self, width:int,height:int):
        if type(width) != int or type(height) != int:
            raise ValueError('width,height must be int!')
        glfwSetWindowAspectRatio(self.window, width,height)
    def set_resizable(self, state):
        glfwSetWindowAttrib(self.window, GLFW_RESIZABLE, state)
        #state = 1 if state else 0 #GLFW_TRUE is 1.

    def set_cursor_lock(self, state):
        if state:
            self.activate()
            self.cursor_locked = True
            glfwSetInputMode(self.window, GLFW_CURSOR, GLFW_CURSOR_DISABLED)
            if glfwRawMouseMotionSupported():
                glfwSetInputMode(self.window, GLFW_RAW_MOUSE_MOTION, GLFW_TRUE)
        else:
            self.deactivate()
            self.cursor_locked = False
            glfwSetInputMode(self.window, GLFW_CURSOR, GLFW_CURSOR_NORMAL)
    def activate(self):
        self.active = True
    def deactivate(self):
        self.cursor_before = 0,0
        self.active = False
        self.cursor_changed = False
    #======================
    def cursor_check(self):
        """ touch screen issue:
        if touch input, locked mouse, the window set the position by force.. dx=400 or -400.
        also ignores 2-N points input.
        https://github.com/glfw/glfw/issues/42

        issue2: too sensitive -> /10.
        issue3: touch click makes dx 0. ->  ...if touch device, floating cursor required.
        """
        #if self.floating:
        if not self.cursor_changed:
            return

        x,y = self.cursor_pos
        bx,by = self.cursor_before
        if bx == 0:
            bx,by = x,y
        dx,dy = x-bx,y-by
        w,h = self.get_size()#30->0.005 scaled. imagine 4k touch..

        vdx,vdy = (dx/w, dy/h)
        if self.cursor_locked:#mouse not drag but forward.
            vdx,vdy = -vdx,-vdy
        #self.inputs.append( ('MOUSE_DXDY', (vdx,vdy) ) )
        self.put_input('MOUSE_DXDY', (vdx,vdy) )
        self.cursor_before = x,y
        self.cursor_changed = False

    def put_input(self, name,value):
        # if not value:
        #     name += '_'
        if name in self.keymap:
            self.keymap[name](value)
        self.inputs.append( (name,value, time() )) #can add as you want.great.
    def bind_keymap(self, keymap):
        self.keymap = keymap

    def bind_input(self, input_func):
        self.input = input_func
    def bind_update(self, update_func):
        self.update = update_func
    def bind_draw(self, draw_func):
        self.draw = draw_func
    def input(self,inputmap):
        pass
    def update(self,dt):
        pass
    def draw(self):
        pass

    def run(self, fps=False):
        bt = perf_counter()
        while not glfwWindowShouldClose(self.window):

            #traditional input-update-draw
            self.cursor_check()
            self.input(self.inputs)

            t = perf_counter() #glfwGetTime()
            dt = t-bt
            bt = t
            self.update(dt)

            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            self.draw()

            
            self.inputs = []
            glfwSwapBuffers(self.window)
            glfwPollEvents()
        glfwTerminate()
    
    def close(self):
        glfwSetWindowShouldClose(self.window,True)


    def bind_callback(self, key, callback):
        """ callback keys :
        key,pos,button,drop,error,char,scroll,enter,winpos,framebuffersize,close
        """
        def self_callback(*args):
            "ignores glfw window, but self."
            glfwwindow,*args = args
            callback(self, *args)
        window = self.window
        if key == 'key':            
            glfwSetKeyCallback(window, self_callback)
        elif key == 'pos':
            glfwSetCursorPosCallback(window, self_callback)
        elif key == 'button':
            glfwSetMouseButtonCallback(window, self_callback)
        
        elif key == 'drop':
            glfwSetDropCallback(window, self_callback)
        elif key == 'error':
            glfwSetErrorCallback(self_callback)#instead glfwGetError()
        
        elif key == 'char':
            glfwSetCharCallback(window, self_callback)
        elif key == 'charmods':
            glfwSetCharModsCallback(window, self_callback)
        elif key == 'scroll':
            glfwSetScrollCallback(window, self_callback)
        elif key == 'enter':
            glfwSetCursorEnterCallback(window, self_callback)
        elif key == 'winpos':
            glfwSetWindowPosCallback(window, self_callback)
        elif key == 'fbsize':
            glfwSetFramebufferSizeCallback(window, self_callback)
        elif key == 'close':
            glfwSetWindowCloseCallback(window, self_callback)        
        #https://www.glfw.org/docs/3.3/group__input.html#ga1ab90a55cf3f58639b893c0f4118cb6e
        else:
            raise KeyError('NO key bind callback!')



# below inspired by pyglet, but too pythonic, so don't.
#@window.draw
#def draw():
    #gl kinds..
#world = World()
# @window.update
# def update(dt):
#   world.update(dt)
# @window.keyinput
# def keyinput(key):
#   if key == 'esc':
#       self.close()
#       return
#   world.input(key)

def main():
    window = Window()
    
    window.set_size([800,600])
    window.set_resizable(False) #window.resizable = True
    #window.set_cursor_lock(True)
    #window.glClearColor(1,1,0,1)

    def input_func(inputmap):
        if inputmap:
            print(inputmap)
            for i in inputmap:
                if i[0] == 'ESCAPE':
                    window.close()
                elif i[0] == 'MOUSE_M':
                    window.set_cursor_lock(True)#touch device cant' m click.
    window.bind_input(input_func)

    def update_func(dt):
        pass#print(dt)
    window.bind_update(update_func)

    def draw_func():
        pass
    window.bind_draw(draw_func)
    window.run()


if __name__ == '__main__':
    main()