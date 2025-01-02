class GUI:
	1



#like NDC, [0-1] area. yup=1.
#we need 2d screen.

# line = Line()
# point = Point(0,0)

# window = ?
# screen?
# rect?
# area?


3

#ui-> texture.
#vector-> pixel.
#line coords shall be [0-1]

#ui.line(0,0,1,1)

3

def line(target,x,y,x2,y2):
	l = Line(x,y,x2,y2)
	target.add(l)

class Ui:
	def __init__(self):
		self.objs = []
	def line(self, x,y,x2,y2):
		#line = Line(x,y,x2,y2)
		#self._add(line)
		line(self,x,y,x2,y2)
	def _add(self, obj):
		self.objs.append(obj)
