from camera import Camera
from unit import Unit

class World:
	"is unit manager. communicates with Window."
	def __init__(self):
		self.units = {}
		self.camera = Camera()

	def create(self):
		unit = Unit()
		self.units[unit.id] = unit
	
	def draw(self):
		ViewProjection = self.camera.get_ViewProjection()
		
		for unit in self.units.values():
			unit.draw(ViewProjection)


from matrix import Mat4
class Camera:
	def __init__(self):
		self.eye
		self.up
		self.right

		self.fov
		self.near
		self.far

	def get_ViewProjection(self):
		Projection = self.get_Projection()
		View = self.get_View()
		ViewProjection = Projection * View
		return ViewProjection
	
	def get_Projection(self):
		return Mat4.Perspective()
		#orthogonal
	def get_View(self):
		return Mat4.View()


from uuid import uuid4

from transform import Transform
from visual import Visual

class Unit:
	"is data holder. communicates with World."
	def __init__(self):
		self.id = str(uuid4())

		self.transform = Transform() # from unity. unit don't need to know def get_Model.

		#self.material
		#self.mesh
		self.visual = Visual()  # finally absctracted! unit knows too much about draw thing.
	def draw(self, ViewProjection):
		Model = self.transform.get_Model()
		self.visual.draw(ViewProjection,Model)


class ConvenientUnit(Unit):
	#===
	@property
	def pos(self):
		return self.transform.position
	@pos.setter
	def pos(self, value):
		self.transform.position.set(value)
	@property
	def vel(self):
		return self.transform.velocity
	@vel.setter
	def vel(self, value):
		self.transform.velocity.set(value)
	@property
	def scl(self):
		return self.transform.scale
	@scl.setter
	def scl(self, value):
		self.transform.scale.set(value)


from rotation import Rotation
from vector import vec3
from matrix import Mat4

class Transform:
	"is pos,vel,scl ..etc holder. communicates with Unit."
	def __init__(self):
		self.position = vec3(0,0,0)
		self.velocity = vec3(0,0,0)
		self.acc = vec3(0,0,0)

		self.rotation = Rotation()

		self.scale = vec3(1,1,1)
		
	def get_Model(self):
		pos,rot,scale = self.position, self.rotation.get_euler(), self.scale
		Model = Mat4.Model(pos,rot,scale)
		return Model

	def look_dir(self,direction):
		self.rotation
	def look_pos(self,position):
		self.rotation


class Rotation:
	"is quaternion, communicates with Transform."
	def __init__(self):
		self.data = [0,0,0,1]  # unity: x,y,z,w blender:w,x,y,z.
	def get_euler(self):
		return x,y,z






from material import Material
from mesh import Mesh

class Visual:
	"is material, mesh holder. communicates with Unit."
	def __init__(self):
		self.material = Material()
		self.mesh = Mesh()
	def draw(self, ViewProjection, Model):
		self.material.ready(ViewProjection,Model)
		self.mesh.draw()
	def draw_instanced(self, ViewProjection, Models):
		self.material.ready_instanced(ViewProjection,Models)
		self.mesh.draw_instanced()




from shader import Shader
from texture import Texture

class Material:
	"is shader, images holder. communicates with Visual."
	def __init__(self):
		self.shader = Shader()
		self.textures = {}
	def ready(self, ViewProjection, Model):
		self.shader.bind()
		self.shader.set_mat4('ViewProjection', ViewProjection)
		self.shader.set_mat4('Model', Model)
	def ready_instanced(self, ViewProjection, Models):
		self.shader.bind()
		self.shader.set_mat4('ViewProjection', ViewProjection)
		self.shader.set_mat4_array('Model', Models)  # so shader have Models. ....?? if not supported, draw-each?? make shader dynamically?


from vao import Vao
class Mesh:
	"is vao holder. communicates with Visual"
	def __init__(self):
		self.vao = Vao()
	def draw(self):
		self.vao.bind()
		self.vao.draw()



#=====core graphics

class Shader:
	"if vert/frag holder. communicates with Material"
	def bind(self):
		1
	def set_float(self,name,value):
		1
	def set_mat4(self,name,value):
		1
	def get_name(self, uniform_name):
		1


from PIL import Image
class Texture:
	"is Image holder. communicates with Material"
	def __init__(self):
		self.image = Image
	def bind(self):#channel?
		1
