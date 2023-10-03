from window import Window
window = Window(size=(1280,700))
window.set_title('engine!')

desc = """

..need Renderer
window glfw pyglet(that easy dist)
and three.js engine laser etc..

Viewmodel is dataholder
Renderer knows how to draw
Window has View / Controller

View is,,Renderer?? i think so.
view.draw(viewmodel), fine.
in game-engine,
implement viewmodel, has data.
and view, draw-class.


Controller sends data to the
engine.inputmanager

engine.inputmanger->engine.model


"""
def splitting_scenario():
	#from glfw_window import Window
	#from pyglet_window import Window

	window.close()
	#window.set_cursor_lock(True)
	window.lock_cursor()
	window.unlock_cursor()

	window.bind_keymap(keymap)
	window.bind_input(lambda x:print(x) if x else '')
	window.bind_update(update)
	window.bind_draw(draw)
	window.glPointSize(5)
	window.run()

	window.watch(model)
	view.watch(model)

	view = View()

	from controller import Controller
	controller = Controller()

	from network import SocketServer
	sock = SocketServer()
	#sock.bind_input(lambda x:controller.put(x))
	for i in sock.get():
		#window.put_input(i) #reversed..
		#window.controller.put(i) #no, controller is more like singleton, close to Model.
		#controller.put(i)
		model.put(i)
		world.put(i)
		engine.controller.put(i)


s = """

Window  Controller    - Model
        View          - Model


              Engine
Window   ->     Controller
Somewhat   ->     Controller
View      <-	  Model
WindowView      <-	  Model
Window-View      <-	  Model

Window    ->	  Controller
Userinput -> Window

[redefine controller as, input-sender. controller can be many.]
Userinput -> Window.controller ->||->  engine.inputmanager -> engine.model
data ->controller ->||->  engine.inputmanager -> engine.model

controller = Controller(address =192.1.1.7, port=26696)
controller = Controller()
controller.connect(address,port)
controller.put(data)

window <-View <-ViewModel <-||<- engine.visualcaster <- engine.model
window-is-View <-ViewModel <-||<- engine.visualcaster <- engine.model
viewmodel = ViewModel()
#viewmodel.watch(address,port) #same interface with controller.
viewmodel.connect(address,port)
data = viewmodel.get()
 or

#hopefully viewmodel is unit holder
#or lightweight, so three.js kinds?
think visual.draw() is required..?
viewmodel.draw() #has gl functions?

on update:
#Viewmodel sends i'm watching, don't abandon me msg.
#if 1 seconds kind after, visualcaster shuts down the connection.
viewmodel automatically updated,
draws as it was.


@window.on_draw
def draw():
	viewmodel.draw()

def draw():
	viewmodel.draw()
window.bind_draw(draw)


...semas viewmodel knows gl features.. not renderer.

Window - Renderer - Viewmodel
glfw      GPU func   data
pyglet
three.js 
unity

"""


from shader import Shader
shader = Shader()

from vao import Vao
vao = Vao()

from camera import Camera
cam = Camera()

from unit import Unit
unit = Unit()

keymap = {
	'ESCAPE':lambda v: window.close(),
	#'MOUSE_M':'set_cursor_lock',
	'MOUSE_R': lambda v:window.set_cursor_lock(True),

	'W':lambda v:cam.set_speed(v),
	'S':lambda v:cam.set_speed(-v),
	'MOUSE_DXDY': lambda v:cam.set_dxdy(*v) ,
}

def update(dt):
	cam.update(dt)

def draw():
	shader.bind()
	
	ProjectionView = cam.get_ProjectionView()
	shader.set_mat4('ProjectionView', (ProjectionView).to_list() )

	Model = unit.get_Model()
	shader.set_mat4('Model', Model.to_list() )

	vao.unbind()
	vao.bind()
	vao.draw(0)
	vao.draw(3)


window.bind_input(lambda x:print(x) if x else '')

window.bind_keymap(keymap)
window.bind_update(update)
window.bind_draw(draw)
window.glPointSize(5)
window.run()

exit()



from window import Window
window = Window(size=(1280,700))
window.set_title('engine!')


from shader import Shader
vertn = """
#version 410 core
layout (location = 0) in vec3 position3f;
//layout (location = 1) in vec3 color;
out vec3 out_color;

uniform mat4 Model;
//uniform mat4 View;
//uniform mat4 Projection;
uniform mat4 ProjectionView;

uniform vec3 color;

uniform float time;
uniform float timer = 1.0;
uniform float scale = 1.0;

void main() 
{
    //gl_Position = vec4(position, 1);
    //gl_Position = Projection * View * Model * vec4(position, 1);
    //vec4 Position = vec4(position , 1);
    
    // using dist
    vec4 Position = vec4(scale * position3f , 1);

    gl_Position = ProjectionView * Model * Position;


    //vec3 new_position = position;
    //new_position.y *= time;
    
    //vec3 white = vec3(1,1,1);
    //out_color = color*(1-position.y) + white*position.y; //upper snow.

    
    // using dist
    //float dist = distance( vec3(0,0,0), vec3(Position.xyz) );
    //dist = clamp(dist,0.0,1.0);
    //out_color = color*(dist) + vec3(1,1,1)*(1-dist);
    
    //out_color = color*(dist) + vec3(1,1,1)*(1-dist);
    out_color = color;
}

"""
shader = Shader(vertn)


#=========================future
fragn = """
#version 410 core

uniform vec3 unicolor; //has too?

//uniform sampler2D tex0;
//uniform sampler2D tex1;

in vec3 out_color;
out vec4 FragColor;
void main()
{
    FragColor = vec4(out_color,1);
    //FragColor = vec4(unicolor,1);

    //outcolor = texture2D(tex0, uvcord);
    //outcolor = mix(texture(tex0, uvcord), texture(tex1, uvcord), 0.4);

}
"""








from vao import Vao
#data = {'position':[0,0,0, 1,0,0, 1,1,0 ,0,1,0] ,'index':[0,1,2, 0,2,3] ,'color': [1,0,0, 0,1,0, 0,0,1, 1,0,1] }
#vao = Vao(data)
#data = {'position':[0,0,0, 1,0,0, 1,1,0 ,0,1,0,    1,0,-1, 1,1,-1, 0,1,-1] ,'index':[0,1,2, 0,2,3,  1,4,5, 1,5,2, 3,2,5, 3,5,6] }
#data = {'position':[-0.5,-0.5,0.5, 0.5,-0.5,0.5, 0.5,0.5,0.5 ,-0.5,0.5,0.5,    0.5,-0.5,-0.5, 0.5,0.5,-0.5, -0.5,0.5,-0.5] ,'index':[0,1,2, 0,2,3,  1,4,5, 1,5,2, 3,2,5, 3,5,6] }

from sphere import make_floor, shape_ring, flatten, make_floors, make_band, make_wall, curve_tree, curve_sphere

#x = make_floor(shape_ring(8))

#x = make_floors(shape_ring(8), height=5, radius=0.3)
#x = make_band(x[0],x[1])

#make tree
x = make_floors(shape_ring(14), height=2, radius=1, stack=18, curve = curve_tree)
x = make_wall(x)
x = flatten(x)


#add base
xx = make_floors(shape_ring(6), height=2, radius=0.3, stack=4)
xx = make_wall(xx)
xx = flatten(xx)
for idx,i in enumerate(xx):
	if idx%3==1:#means y
		i -=2
	x.append(i)

data = {'position3f':x}
vao = Vao(data)









from camera import Camera
cam = Camera()

#looking down
cam.position = (0,0,5)
cam.look(0,2,0)

#looking up
#cam.position = (0,-5,0)
#cam.look(0,0,0)




keymap = {
	'ESCAPE_':lambda:window.close(),
	#'MOUSE_M':'set_cursor_lock',
	'MOUSE_R': lambda:window.set_cursor_lock(True),

	'W':lambda:cam.set_speed(1),
	'S':lambda:cam.set_speed(-1),
	'W_':lambda:cam.set_speed(0),
	'S_':lambda:cam.set_speed(0),
	
	'F':lambda:make_unit(),
}

#need value for axis input..
inputmap = {
	'MOUSE_DXDY': lambda v:cam.set_dxdy(*v) ,
	'D': lambda v:cam.set_dxdy(0.1,0) ,
	'A': lambda v:cam.set_dxdy(-0.1,0) ,
}


def inputfunc(inputs):
	for i in inputs:
		name,value = i
		func = inputmap.get(name, lambda x:1)
		func(value)

from unit import Unit

import random
units = []
def make_unit():
	unit = Unit()
	
	unit.transform.rvel.set(0,0.1,0) #x->y->z order.
	k = 100
	x,z = random.randint(-k,k) , random.randint(-k,k)
	unit.transform.pos.set(x,0,-100)
	unit.transform.vel.set(0,40,0) #10m/s is 36000m/hr, 36km.
	unit.transform.acc.set(0,-10,0)

	unit.uniforms['color'] = random.random(),random.random(),random.random()
	unit.uniforms['timer'] = 3
	unit.uniforms['time'] = 0
	unit.uniforms['time_remove'] = 5
	#unit.uniforms['color'] = (1,0,1)

	# def update_lock_height(self,dt):
	# 	if self.transform.pos.z<-40:
	# 		self.transform.pos.z = -2
	#unit.bind_update(update_lock_height)
	#unit.add_update(update_lock_height)
	def update_time(self,dt):
		self.uniforms['time'] += dt
		if self.uniforms['time_remove'] < self.uniforms['time']:
			#self.destroy()
			#unit.set_func('destroy',destroy)
			units.remove(self)
	unit.add_update(update_time)
	
	units.append(unit)


[make_unit() for i in range(20)]

def update(dt):
	cam.update(dt)
	for unit in units:
		unit.update(dt)
		#if unit.transform.pos.y>40:
		#	unit.transform.pos.y = -2
		#--> unit.update





import math

import time

t = time.time()

def draw():
	shader.bind()
	
	ProjectionView = cam.get_ProjectionView()
	shader.set_mat4('ProjectionView', (ProjectionView).to_list() )

	for unit in units:
		Model = unit.get_Model()
		shader.set_mat4('Model', Model.to_list() )
		shader.set_vec3('color', unit.uniforms['color'] )

		
		#shader.set_vec3('timer', unit.uniforms['timer'] )
		#shader.set_float('time', time.time()-t )
		#shader.set_float('scale', time.time()*0.2%1 )  #time * frequency % Hz
		tafter = unit.uniforms['time'] - unit.uniforms['timer']
		if tafter > 0:
			#velocity = tafter
			#scale is not vel but pos. inv.x**2 is acceptable.. which is log.
			#https://www.mathportal.org/math-tests/tests-in-exponents-and-logarithms/logarithms.php?testNo=5
			#math.log(0)=-inf / math.log(1)=0 / math.log(2.7) = 1
			#y=5*log(x+1)
			f = lambda x:5*math.log(x+1)

			shader.set_float('scale', (1.0+ f(tafter*50) )  )
			#shader.set_vec3('color', ()  )
		else:
			shader.set_float('scale', (1.0)  )


		vao.unbind()
		vao.bind()
		vao.draw(0)
		#vao.draw(1)

window.bind_keymap(keymap)
window.bind_input(inputfunc)
window.bind_update(update)
window.bind_draw(draw)
window.glPointSize(2)


window.run()
