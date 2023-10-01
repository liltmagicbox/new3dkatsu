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

