from math import cos,sin,radians, asin


def flatten(data):
	if type(data[0]) in (int,float):
		return data
	else:
		temp = []
		for i in data:
			temp.extend(i)
		return flatten(temp)
	#print(flatten( [[[1]],[[2]],[[3]]] ))


#basic 2d shape.
def shape_ring(slice=8):
	shape = []
	for i in range(slice):
		th = radians( 360/slice*i )
		x,y = cos(th),sin(th)
		shape.append( (x,y) )
	return shape


def make_floor(shape, z=0.0,   radius=1.0, zup=False):
	floor = []
	for x,y in shape:
		x,y = x*radius, y*radius
		if zup:
			point = (x, y, z)
		else:
			point = (x, z, -y)
		floor.append(point)
	return floor


def _base_make_floors(shape, stack=4, height=1.0, radius=1.0, zup=False):
	floors = []
	for i in range(stack):
		z = i/(stack-1)*height
		floor = make_floor(shape,z, radius,zup)
		floors.append(floor)
	return floors
#by curve? here sphere,curved,cone,cyl.

#sphere
def make_floors(shape, stack=4, height=1.0, radius=1.0, zup=False, curve = None):
	curve = curve_constant if curve is None else curve
	floors = []
	for i in range(stack):
		ratio = i/(stack-1)
		z = ratio*height
		floor = make_floor(shape,z, radius*curve(ratio) ,zup)
		floors.append(floor)
	return floors
#by curve? here sphere,curved,cone,cyl.

def curve_constant(ratio):
	return 1
def curve_inv_cone(ratio):
	return ratio
def curve_cone(ratio):
	return 1-ratio

def curve_bullet(ratio):
	return cos(ratio*1.57)
def curve_almond(ratio):
	x = 2*(ratio-0.5) #[0-1]->[-1-1]
	return cos( x*1.57 )
#finally,
def curve_sphere(ratio):
	y = 2*(ratio-0.5) #[0-1]->[-1-1]
	angle = asin(y)
	return cos(angle)
"""
  /
 / y
/
---
 ^cos(angle)
"""

def curve_tree(ratio):
	return (sin(ratio*6.28*5)/2 +1) * (1-ratio)




# x = shape_ring()
# x = make_floor(x,0)
# def make_sphere():
# 	make_ring()


#=========================================================================

def get_face(p00,p10,p11,p01):
	"2d screen x,y, RH, 2 triangle indices. upper first, so that line_strip looks great."
	#return [p00,p10,p11, p00,p11,p01]
	return [p00,p11,p01, p00,p10,p11]

def make_band(floor1, floor2):
	#floor [(xyz),]
	band = []
	assert len(floor1) == len(floor2)
	for i in range( len(floor1) ):
		p00 = floor1[0+i]
		try:
			p10 = floor1[1+i]
		except IndexError:
			p10 = floor1[0]
		try:
			p11 = floor2[1+i]
		except IndexError:
			p11 = floor2[0]
		p01 = floor2[0+i]

		face = get_face(p00,p10,p11,p01)
		band.append(face)
	return band


def make_wall(floors):
	"floors is [floor,]"
	bands = []
	stack = len(floors)
	for i in range(stack-1):
		floor1, floor2 = floors[i], floors[i+1]
		band = make_band(floor1,floor2)
		bands.append(band)
	return bands

#x = make_wall( make_floors(shape_ring(4)) )
#x = flatten(x)
#print(x)












#===================== indices, seems bad approach. merge, get indices last.

def get_indices(floor_s):
	x = flatten(floor_s)
	x = len(x)
	x = x//3
	x = [i for i in range(x)]
	return x
	# x = get_indices( make_floors(shape_ring()) )
	# x = get_indices( make_floor(shape_ring()) )
	# print(x)






def make_volume(shape,       stack=4, height=1.0, radius=1.0, zup=False):
	floors = make_floors(shape, stack,height,radius,zup)




def get_face_indices(p00,p10,p11,p01):
	"2d screen x,y, RH, 2 triangle indices."
	return (p00,p10,p11, p00,p11,p01)


def get_wall_indices(floor1_idx, floor2_idx):
	wall_indices = []
	#don't worry, we will make rect->5 when uv/normal.
	floor1_idxE = floor1_idx + [floor1_idx[0]]
	floor2_idxE = floor2_idx + [floor2_idx[0]]
	for i in range( len(floor1_idx) ):
		p00 = floor1_idxE[0+i]
		p10 = floor1_idxE[1+i]
		p11 = floor2_idxE[1+i]
		p01 = floor2_idxE[0+i]

		face_indices = get_face_indices(p00,p10,p11,p01)
		#print(face_indices)
		wall_indices.append(face_indices)
	return wall_indices
	# x = get_indices( make_floors(shape_ring(4)) ) #20s because 1-layer has 5points.
	# x = get_wall_indices(x[:4],x[4:8])
	# print(x)

def _idxused_make_wall(floors):
	wall = []
	indices = get_indices(floors)
	points = len(floors[0])
	offset = 0

	stack = len(floors)
	for i in range(stack-1):
		floor1_idx = indices[offset : offset+points]
		floor2_idx = indices[offset+points : offset+points+points]
		offset += points
		wall_indices = get_wall_indices(floor1_idx, floor2_idx)
		#print(wall_indices)
		wall.append(wall_indices)
	return wall












#def connect_nearest
#connect_identical( make_floors(shape_ring()) )



