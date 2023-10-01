from shader import Shader
from texture import Texture


material_data = {
    'color':1 #or rgb or texture
}

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

future="""

texture holds origin img?
-dynamic texture, need out-source-getter?

where to put uniforms, if needed? unit??

texture-loader, where?? hopefully not the texture.py.

asset manager is required, for both mesh,material.


"""