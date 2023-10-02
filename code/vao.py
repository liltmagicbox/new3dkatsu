streamcopytrest = """
#https://registry.khronos.org/OpenGL-Refpages/es3.1/
#https://registry.khronos.org/OpenGL-Refpages/gl4/html/glBufferData.xhtml
#stream copy!  es3.1 stream-able. while 1.1 not.




from OpenGL.GL import *
from glfw.GLFW import *

glfwInit()
window = glfwCreateWindow(300,200,'w', None, None)
glfwMakeContextCurrent(window)

vao = glGenVertexArrays(1) # make (1) of Vertex Array. errs if not window/glfwinit yet.
vbo = glGenBuffers(1) #Buffer Object. for data of vao.
ebo = glGenBuffers(1) #indexed, requires EBO.

glBindVertexArray(vao) #gpu to bind VAO
#gl_bind_write_vertices(vbo,vertices)
glBindBuffer(GL_ARRAY_BUFFER, vbo) #gpu bind VBO in VAO.
#glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

#gl_bind_write_indices(ebo,indices)

#https://pyopengl.sourceforge.net/ctypes/pydoc/OpenGL.GL.VERSION.GL_1_5.html
usage = GL_STATIC_DRAW
usage = GL_DYNAMIC_DRAW
usage = GL_STREAM_DRAW

import numpy as np
vertices = np.array( [1,2,3,4,5,6],dtype='float32')
glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, usage)
x=glGetBufferParameteriv(GL_ARRAY_BUFFER,GL_BUFFER_SIZE)
print(x)
#24, 4Byte* 6
x =glGetBufferParameteriv(GL_ARRAY_BUFFER,GL_BUFFER_USAGE)
print(x,usage.real)
#0
#[35044     0     0     0]

#glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, usage)
glBufferSubData(GL_ARRAY_BUFFER, 0, vertices.nbytes, vertices)

#cant sub larger len!
#vertices = np.array( [1,2,3,4,5,6, 7,8,9],dtype='float32')
#glBufferSubData(GL_ARRAY_BUFFER, 0, vertices.nbytes, vertices)

exit()




"""


numpytobytesfinally = """



import numpy as np
v1 = np.array( [0,1,0,2],dtype='float32')
v2 = np.array( [0,3,0,4],dtype='int32')
#https://numpy.org/doc/stable/reference/generated/numpy.stack.html
#x = np.stack( [v1,v2] ,casting='safe')

x = np.rec.fromarrays( [v1,v2] )
#x=x.reshape(3,2)
x=x.flatten()

print(x.dtype)
print(x.shape)


x=x.tobytes()
b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x80?\x03\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00@\x04\x00\x00\x00'
#0 0 1 1 0 0 2 2 kinds.
x = v1.tobytes()+v2.tobytes()
b'\x00\x00\x00\x00\x00\x00\x80?\x00\x00\x00\x00\x00\x00\x00@\x00\x00\x00\x00\x03\x00\x00\x00\x00\x00\x00\x00\x04\x00\x00\x00'
#0 1 0 1 kindns.finally,so simple. since we don't need to have nparray, but bytes to GPU.
print(x)

exit()




"""

from OpenGL.GL import *
import numpy as np
import ctypes

#maxvec4 = glGetIntegerv(GL_MAX_VERTEX_UNIFORM_VECTORS)
#for instanced

#vertex_data is dict, 'position' is nessasary.
default_mesh_data = {
'position3f':[0,0,0, 0.5,0,0, 0.5,0.5,0],
'color3i':[255000,0,0, 0,255000,0, 0,0,255000],
}
#color3b, 1 is 1, 2 is 2. position.y you can see high building.  255 is so 255,but overflow. 256 is 0, 257 is 1.
#somehow, it's safe to color3b/20 , but not /128? seems int8,notuint8. ->GL_BYTE!

#'color3f':[0.5,0,0, 0,0.5,0, 0,0,0.5],
#'position3f':[0,0,0, 0.5,0.5,0, 0,0.5,0, 0,0,0,  0.5,0,0, 0.5,0.5,0 ],
#'color3b':[1,0,0, 0,1,0, 0,0,1],


# NOTE: line width is deprecated. core remained. ..know why.
#https://www.glprogramming.com/red/chapter02.html
DRAWMODE = {
0:GL_POINTS,
1:GL_LINE_STRIP,
2:GL_LINE_LOOP,
3:GL_TRIANGLES
}

USAGE = {
0: GL_STATIC_DRAW,
1: GL_DYNAMIC_DRAW,
2: GL_STREAM_DRAW,
}


class Vao:
    last = 0
    "is vao holder. communicates with Mesh."
    def __init__(self, attr_data_map = None, indices=None, usage=0):
        "usage 0:static,dynamic,stream"
        if attr_data_map is None:
            attr_data_map = default_mesh_data
        
        #ensure ordered
        #attr_data_map = {k:v for k,v in sorted(attr_data_map.items())}
        #this requires : shader.get_loc_attribute('position3f') finally.

        
        

        #points = len(mesh_data['position'])//3
        #indices = mesh_data.get('index', tuple(range(points))  )
        #indices = np.array(indices).astype('uint32')
        
        #https://stackoverflow.com/questions/30362391/how-do-you-find-the-first-key-in-a-dictionary
        if indices is None:
            first_attr = next(iter(attr_data_map))
            vertex_count = len(attr_data_map[first_attr]) // int(first_attr[-2]) #position3f
            indices = tuple(range(vertex_count))
        indices = make_data_flat_dtype(indices,'uint32')
        
        
        #lengths = { key:len(value) for key,value in mesh_data.items() if key != 'index'}
        #arr2d = [value for key,value in mesh_data.items() if key != 'index']
        
        #arr2d = [i for i in attr_data_map.values()]
        #vertices = np.concatenate(arr2d).astype('float32')  # [ p,p,p, n,n,n, u,u,u ]
        
        arr2d = [  make_data_flat_dtype(data,get_dtype(name)) for name,data in attr_data_map.items()]
        #https://stackoverflow.com/questions/11309739/store-different-datatypes-in-one-numpy-array
        #vertices = np.concatenate(arr2d).astype('float32')  # [ p,p,p, n,n,n, u,u,u ]
        
        #try1:  rec is .. xyz rgb  -> xr yg zb.
        #vertices = np.rec.fromarrays( arr2d, names = tuple(attr_data_map.keys()) )
        #print(vertices.shape)
        #print(vertices.dtype)
        #print(vertices.nbytes)
        #print(vertices)
        #[(0. , 1.) (0. , 0.) (0. , 0.) (0.5, 0.) (0. , 1.) (0. , 0.) (0.5, 0.) (0.5, 0.) (0. , 1.)]
        
        #try2: bytes!!!
        #https://www.guyrutenberg.com/2020/04/04/fast-bytes-concatenation-in-python/
        #says b+= slow, join or use bytearray().
        #i.tobytes() for i in arr2d join ->bytearray.
        # vertices = np.concatenate(arr2d).astype('float32')  # [ p,p,p, n,n,n, u,u,u ]
        # vertices_bytedata = bytearray()
        # [vertices_bytedata.extend(i.tobytes()) for i in arr2d]
        # print(len(vertices_bytedata), vertices.nbytes)
        # print(vertices_bytedata)
        # print(vertices)
        

        #try3 : fianlly working
        # vertices = np.concatenate(arr2d).astype('float32')  # [ p,p,p, n,n,n, u,u,u ]
        # print(vertices.tobytes())

        # vertices = bytearray()
        # [vertices.extend(i.tobytes()) for i in arr2d]
        # print(vertices)
        # print(bytes(vertices))
        # vertices = bytes(vertices)
        #but somehow, gl don't want to draw via bytearray, even data is same.

        vertices = b''.join([i.tobytes() for i in arr2d])
        indices = indices.tobytes()


        usage = USAGE[usage]
        #--------
        if bool(glGenVertexArrays):
            vao = glGenVertexArrays(1) # make (1) of Vertex Array. errs if not glfwMakeContextCurrent(win) yet.
            vbo = glGenBuffers(1) #Buffer Object. for data of vao.
            ebo = glGenBuffers(1) #indexed, requires EBO.

            glBindVertexArray(vao) #gpu to bind VAO
            #gl_bind_write_vertices(vbo,vertices)
            glBindBuffer(GL_ARRAY_BUFFER, vbo) #gpu bind VBO in VAO.
            glBufferData(GL_ARRAY_BUFFER, len(vertices), vertices, usage) #allocating buffer,here.
    
            #gl_bind_write_indices(ebo,indices)
            glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ebo)# is storing int data
            glBufferData(GL_ELEMENT_ARRAY_BUFFER, len(indices), indices, usage)
            #write once or keep the data kinds. not that important!

            set_vertex_attrib_pointer(attr_data_map)

        else:
            vao,vbo,ebo = 0,0,0

        self.vao = vao
        self.vbo = vbo
        self.ebo = ebo
        
        self.points = len(indices)
        self.usage = usage
        self.subdatainfo = get_buffer_sub_data(attr_data_map)
    #========================
    def bind(self):
        if Vao.last == self.vao:
            return
        Vao.last = self.vao
        if glBindVertexArray:
            glBindVertexArray(self.vao)
    def unbind(self):
        Vao.last = 0
        if glBindVertexArray:
            glBindVertexArray(0)

    def draw(self, kind=3):
        "0:point 1:line 2:lineloop 3:tri"
        #draw_kind = DRAWMODE.get(kind, GL_TRIANGLES)
        mode = DRAWMODE[kind]  #so errors. user need to know what's happening.
        glDrawElements(mode, self.points, GL_UNSIGNED_INT, None) #overflow safe. not use int,but uint.
    #=================
    def update(self, name, data):
        "only changes vertex's data."
        #vao.update('position' , [ 0,0,0,   1,1,1,   1,0,0, ] )
        #vertices = self.vertices
        #slicer = self.slices[name]
        #vertices[slicer] = value
        
        data = make_data_flat_dtype(data, get_dtype(name) )
        #glBindVertexArray(VAO) #gpu bind VAO
        self.bind()
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo) #gpu bind VBO in VAO
        
        # replace whole VBO
        #glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
        
        # in-place
        #https://gamedev.stackexchange.com/questions/58417/how-to-modify-vbo-data
        #https://stackoverflow.com/questions/4854565/opengl-vbo-updating-data
        #https://registry.khronos.org/OpenGL-Refpages/gl4/html/glBufferSubData.xhtml
        

        #offset,size = self.replacer[name]
        #offset = 0 if offset.value is None else offset.value
        offset,bsize = self.subdatainfo[name]

        #lets assume data is clear. use prepare_data.
        # if type(data) != np.ndarray:
        #     data = np.array(data,dtype='float32')
        # if len(data.shape) != 1:
        #     data = np.concatenate(data).astype('float32')  # [ p,p,p, n,n,n, u,u,u ]
        # if data.dtype != np.float32:
        #     data = data.astype('float32')
        #print(offset,bsize,data,name, data.dtype)#..since bsize is, it's safe.
        glBufferSubData(GL_ARRAY_BUFFER, offset, bsize, data)  # target offset size data

        """
        When replacing 
        the entire data store,
        consider using glBufferSubData
        rather than completely recreating the data store with glBufferData.
         This avoids the cost of reallocating the data store.
        """

    #=====of vertices is not done. attr_data_tobytes
    #1:attr update/2:idxupdate 3: extend/shrink(by replace)  4?change only attrs-datas???

    def replace_vertices(self, vertices):
        "for diffreent size. use with indices."
        vertices = make_data_flat_dtype(vertices, get_dtype('float32') )
        self.bind()
        #gl_bind_write_vertices(self.vbo,vertices)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo) #gpu bind VBO in VAO.
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, self.usage)
        #glBufferSubData(GL_ARRAY_BUFFER, 0, vertices.nbytes, vertices)

    def replace_indices(self, indices):
        "indices is ui32 np array."
        indices = make_data_flat_dtype(indices, get_dtype('uint32') )
        self.bind()
        #gl_bind_write_indices(self.ebo,indices)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.ebo)# is storing int data
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, self.usage)
        #glBufferSubData(GL_ELEMENT_ARRAY_BUFFER, 0, indices.nbytes, indices)

    def update_vertices(self, vertices):
        "requires exact length.."
        vertices = make_data_flat_dtype(vertices, get_dtype('float32') )
        self.bind()
        #gl_bind_write_vertices(self.vbo,vertices)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo) #gpu bind VBO in VAO.
        #glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
        glBufferSubData(GL_ARRAY_BUFFER, 0, vertices.nbytes, vertices)

    def update_indices(self, indices):
        "indices is ui32 np array."
        indices = make_data_flat_dtype(indices, get_dtype('uint32') )
        self.bind()
        #gl_bind_write_indices(self.ebo,indices)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.ebo)# is storing int data
        #glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)
        glBufferSubData(GL_ELEMENT_ARRAY_BUFFER, 0, indices.nbytes, indices)

    
    @staticmethod
    def prepare_data(data, dtype):
        "to not import vao.make_data_flat_dtype"
        return make_data_flat_dtype(data, dtype)




#dynamic draw?? says little faster..but..
# def gl_bind_write_indices(ebo,indices):
#     glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ebo)# is storing int data
#     glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)

# def gl_bind_write_vertices(vbo,vertices):
#     """
#     VAO has buffers, VBO is one of Buffer.
#     """
#     glBindBuffer(GL_ARRAY_BUFFER, vbo) #gpu bind VBO in VAO.
#     glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)




FLOAT32_BYTES = np.float32(0.0).nbytes

attr_size_map = {
0:3,
1:2,
2:3,
}

#ah,pyglet!
attr_data_map = {
'position3f':'data1',
'uv2f':'data2',
'color3b':'data3',
'color3f':'data3',
'somewhat2i':'data3',
'time1f':'data3',
'mass1f':'data3',
'mass3f':'data3',
}
#...and fianlly 3vf. ah... no, 1:not v else:v.
#https://pyglet.readthedocs.io/en/latest/programming_guide/graphics.html
#https://pythonhosted.org/pyglet/programming_guide/vertex_lists.html
# position/static dynamic stream
# i I b B f d. not short.

batch="""
v1=vl(batch)
v1=vl(batch)
batch.draw()#..wow.
"""

# program.vertex_list(3, pyglet.gl.GL_TRIANGLES,
# position=('f', (200, 400, 300, 350, 300, 450)),
# colors=('Bn', (255, 0, 0, 255,  0, 255, 0, 255,  75, 75, 255, 255),)
#normaalize.

after_looking_pyglet="""
accept:
only 32. not 64.
i I ,great.
/static

not accept:
n
attr_name = (dtype,data)
pixed draw type.

future:
split indices  from aattrs.

batch,wonderful...but bad, since reversed approach. (human need very intended)
"""



BYTES_before_looking_pyglet = {
    'f': np.float32(0.0).nbytes,
    'f32': np.float32(0.0).nbytes,
    'f64': np.float64(0.0).nbytes,
    
    'i': np.int32(0.0).nbytes,
    'i32': np.int32(0.0).nbytes,
    'i64': np.int64(0.0).nbytes,
    
    'ui': np.uint32(0.0).nbytes,
    'ui32': np.uint32(0.0).nbytes,
    'ui64': np.uint64(0.0).nbytes,

    'b': np.uint8(0.0).nbytes,
}

BYTES = {
    'f': np.float32(0.0).nbytes,
    'i': np.int32(0).nbytes,#for minus
    'b': np.uint8(0).nbytes,#only 255!
}

DTYPE = {
    'b': np.uint8,#only 255!
    'f': np.float32,
    'i': np.int32,#for minus
    'I': np.uint32,#for indices
    
    'uint8': np.uint8,
    'float32': np.float32,
    'int32': np.int32,
    'uint32': np.uint32,
}


GLTYPE = {
    #np.uint8 : GL_BYTE,
    np.uint8 : GL_UNSIGNED_BYTE,
    np.float32 : GL_FLOAT,
    np.int32 : GL_INT,
    np.uint32 : GL_UNSIGNED_INT,
}

def get_buffer_sub_data(attr_data_map):
    "size :int, offset:byte."
    offsets = {}
    offset = 0
    for name,data in attr_data_map.items():
        #dtype = DTYPE[name[-1]]
        dtype = get_dtype(name)
        bsize = len(data) * dtype(0).nbytes
        
        offsets[name] = offset,bsize
        offset = bsize
    return offsets



#dictgetitemswht enumuerate
# for idx, kv in enumerate(attr_data_map.items()):
#     print(kv[0])

def set_vertex_attrib_pointer(attr_data_map):
    """
    must done after binding vao, vbo,ebo.. maybe vao only? 
    no stride
    data = [ xyzxyzxyz, uvuvuv, rgbrgbrgb].
    
    channel 0: position3 -> size 3, offset 0
    channel 1: uv2 -> size 2, offset  len(position3)*bytes
    """
    # idx, NOTE:opengl core no attr 0-what this mean?
    offset = ctypes.c_void_p(0)  # is bytes offset
    for idx, kv in enumerate(attr_data_map.items()):
        name, data = kv
        #attr_size = int(name[-2])
        attr_size = get_size(name)
        dtype = get_dtype(name)
        gltype = GLTYPE[dtype]

        #loc = glGetAttribLocation(self.program, attribute_name) #detatch sader from vao

        glVertexAttribPointer(idx, attr_size, gltype, GL_FALSE, 0, offset)  #(index, size, gldtype, normalized, stride, offset)
        glEnableVertexAttribArray(idx)
        offset = ctypes.c_void_p( len(data) * dtype(0).nbytes )



def get_size(name):
    return int(name[-2])
def get_dtype(name):
    "position3f"
    return DTYPE[name[-1]]


def make_data_flat_dtype(data, dtype):
    
    # if dtype == 'f':
    #     dtype = np.float32
    # elif dtype == 'i':
    #     dtype = np.int32
    # elif dtype == 'b':
    #     dtype = np.uint8
    #and else is np.  great!
    dtype = DTYPE.get(dtype,dtype)
    
    if type(data) != np.ndarray:
        data = np.array(data,dtype=dtype)
    if len(data.shape) != 1:
        data = np.concatenate(data) # [[123][456]] ->[123456]
        #why not np.flaatten?
    if data.dtype != dtype:
        data = data.astype(dtype)
    return data

def attr_data_tobytes(attr_data_map):
    arr2d = [  make_data_flat_dtype(data,get_dtype(name)) for name,data in attr_data_map.items()]
    vertices = b''.join([i.tobytes() for i in arr2d])
    return vertices
        

desc = """

vao , is for gpu, bound. draw-able.

vao has  vbo,veo..   data, indices.

float32/int32 is little faster, even for 64x pc.

mesh_data is 
position is specially required.
indices automatically created by //3.

stride/offset
[aaaaaa,bbb,cccccc] is created by np.concatenate.
[aa,b,cc, aa,b,cc , aa,b,cc] requires strid.
contionous load, little faster..?
but hard to update, we didn't.


to update,
'position',values
is replacing numpy array, by slice.
-> changed partial-update , using glBufferSubData.


Vao has.. no nparr,  nor origin mesh_data.


2023.10.03
MAJOR change:
as the rule: keep simple GPU elements,
we assume all data np, not list.
data_attrs  is more higher level.

"""

def main():
    from glfw.GLFW import glfwInit,glfwCreateWindow,glfwMakeContextCurrent
    glfwInit()
    window = glfwCreateWindow(300,200,'w', None, None)
    glfwMakeContextCurrent(window)
    vao = Vao()
    vao.update('position3f',[1,2,3,4,5,6,7,8,9])
    vao.update('position3f',[1,2,3,4,5,6,7])
    vao.update('position3f',[1,2,3,4,5,6,7,9,9,9,9])


if __name__ == '__main__':
    main()