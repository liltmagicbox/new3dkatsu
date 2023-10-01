#mesh_data is dict, 'position' is nessasary. order is important.
mesh_data = {
'index':[0,1,2],
'position':[0,0,0, 0.5,0,0, 0,0.5,0],
'color':[1,0,0, 0,1,0, 0,0,1],
}


from vao import Vao
class Mesh:
	"is vao holder. communicates with Visual"
	# since mesh not that changed, and is vao creater, we decide to do this way.
	def __init__(self, mesh_data=None):
		self.vao = Vao(mesh_data)
		mesh_data = {} if mesh_data is None else mesh_data
		self.mesh_data = mesh_data.copy()
	def draw(self):
		self.vao.bind()
		self.vao.draw()
	def draw_instanced(self):
		self.vao.bind()
		self.vao.draw_instanced()
	def update(self, name,value):
		self.vao.update(name,value)
		self.mesh_data[name] = value
