from uuid import uuid4
from pymatrix import vec3 as vec

class Unit:
	def __init__(self):
		self.id = str(uuid4())
		self.pos = vec(0,0,0)
		self.vel = vec(0,0,0)
		self.acc = vec(0,0,0)

		self.scl = vec(1,1,1)
		self.rot = vec(0,0,0) #quaternion? x,y,z,w
	def update(self, dt):
		self.vel += self.acc * dt
		self.pos += self.vel * dt

class Dragon(Unit):
	def update(self,dt):
		super().update(dt)
		print('im dragon!')


class DrawUnit(Unit):
	def __init__(self):
		super().__init__()
		self.material = 'default'
		self.mesh = 'default'
		self.uniform = {'color':'hp','opacity':'mp'} # uniform_name : self.attr
		
	def draw(self, view_projection_matrix):
		"""
		draw sequence:
		bind shader
		bind view matrix
		bind model matrix
		bind vao
		draw vao
		"""
		
		#model matrix is from translate, rotation, scale.
		model_matrix = mat4_get_model(self.pos, self.rot, self.scl) #float[16]
		
		self.material.shader.bind()
		self.material.shader.set_mat4('ViewProjection', view_projection_matrix)
		self.material.shader.set_mat4('Model', model_matrix)
		self.mesh.vao.bind()
		self.mesh.vao.draw()







