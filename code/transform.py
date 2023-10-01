#from rotation import Rotation
from vector import vec
from matrix import Matrix

class Transform:
	"is pos,vel,scl ..etc holder. communicates with Unit."
	def __init__(self):
		self.pos = vec(0,0,0)
		self.vel = vec(0,0,0)
		self.acc = vec(0,0,0)
		
		#NOTE: order matters. roll first/last.. thats why we prefer quat. now x->y->z screen coords.
		self.rpos = vec(0,0,0)
		self.rvel = vec(0,0,0)
		self.racc = vec(0,0,0)

		self.scale = vec(1,1,1)

		#self.rotation = Rotation()

	def update(self, dt):
		self.vel += self.acc * dt
		self.pos += self.vel * dt
		self.rvel += self.racc * dt
		self.rpos += self.rvel * dt


	#last one stored?
	@property
	def rot(self):
		return self.rpos
		# if type(self.rotation) == 'quat':
		# 	return self.rotation.get_euler()
	@rot.setter
	def rot(self,value):
		self.rpos.set(*value)

	def get_Model(self):
		pos,rot,scale = self.pos, self.rot, self.scale
		Model = Matrix.Model(pos,rot,scale)
		return Model

	def look_dir(self,direction):
		self
	def look_pos(self,position):
		self

if __name__ == '__main__':
	t = Transform()
	#t.rot = vec(0,0,0)
	t.rot.set(0.1,0,0)
	x = t.get_Model()
	print(x)
