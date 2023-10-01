from unit import Unit

#we need mediator.. Engine/System.
from camera import Camera
#ViewProjection = self.camera.get_ViewProjection()

class World:
	"is unit manager. communicates with Window."
	def __init__(self):
		self.units = {}
		
	def create(self):
		unit = Unit()
		self.units[unit.id] = unit
	
	def draw(self, ViewProjection):
		for unit in self.units.values():
			unit.draw(ViewProjection)



















# class SphereMesh(Mesh):
# 	data = {
# 	'indices':(0,1,2),
# 	'position':( (0,0,0), ),
# 	}
#no init ! data is only the difference.
#..too bad, too many classes.
#mesh = meshfactory.get('sphere')
#is better.

class MeshFactory:
	def __init__(self):
		self.designs = {}
	def get(self, name):
		mesh_data = self.designs.get(name)
		return Mesh(mesh_data)


#=====core graphics


