from uuid import uuid4

from transform import Transform
from visual import Visual

from vecops import *
from matrix import Matrix
#Model = Matrix.Model( (0,0,0), quat_from_aa(0.9,(0,0,1) ),  (1,1,1) )

class Unit:
	"is data holder. communicates with World."
	def __init__(self):
		self.id = str(uuid4())

		#self.transform = Transform() # from unity. unit don't need to know def get_Model.

		#self.material
		#self.mesh
		self.visual = Visual()  # finally absctracted! unit knows too much about draw thing.

		self.uniforms = {}
		self.updates = []

		#===ECS?
		self.components = {'transform':Transform()}
	def __getattr__(self,name):
		try:
			return self.components[name]
		except KeyError:
			raise KeyError( f'Unit has no attribute of :{name}')

	def draw(self, ViewProjection):
		Model = self.get_Model()
		self.visual.draw(ViewProjection,Model)
	def get_Model(self):
		return self.transform.get_Model()
	
	def update(self,dt):
		#self.transform.update(dt)
		for comp in self.components.values():
			if hasattr(comp,'update'):
				comp.update(dt)  # comp no need to know unit, as usually designed.
		
		for update in self.updates:
			update(self,dt)
	def add_update(self, update):
		self.updates.append(update)
		#self.somewhat['update'].append(update)
	def add_component(self, comp):
		self.components[comp.name] = comp


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


if __name__ == '__main__':
	u = Unit()
	x = u.get_Model()
	print(x)
