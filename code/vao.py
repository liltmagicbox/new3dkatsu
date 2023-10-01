from OpenGL.GL import *
import numpy as np
import ctypes

#maxvec4 = glGetIntegerv(GL_MAX_VERTEX_UNIFORM_VECTORS)
#for instanced

#vertex_data is dict, 'position' is nessasary.
default_mesh_data = {
'index':[0,1,2],
'position':[0,0,0, 0.5,0,0, 0,0.5,0],
'color':[1,0,0, 0,1,0, 0,0,1],
}


# NOTE: line width is deprecated. core remained. ..know why.
#https://www.glprogramming.com/red/chapter02.html
draw_kinds = {
0:GL_POINTS,
1:GL_LINE_STRIP,
2:GL_LINE_LOOP,
3:GL_TRIANGLES
}


class Vao:
    last = None
    "is vao holder. communicates with Mesh."
    def __init__(self, mesh_data = None):
        if mesh_data is None:
            mesh_data = default_mesh_data
        
        points = len(mesh_data['position'])//3

        indices = mesh_data.get('index', tuple(range(points))  )
        indices = np.array(indices).astype('uint32')

        lengths = { key:len(value) for key,value in mesh_data.items() if key != 'index'}
        arr2d = [value for key,value in mesh_data.items() if key != 'index']
        vertices = np.concatenate(arr2d).astype('float32')  # [ p,p,p, n,n,n, u,u,u ]
        
        #--------
        if not bool(glCreateShader):
            return
        VAO = glGenVertexArrays(1) # Vertex Array. n=>VA[n]. errs if not window yet.
        VBO = glGenBuffers(1) #Buffer Object. for data of vao.
        EBO = glGenBuffers(1) #indexed, requires EBO.
        glBindVertexArray(VAO) #gpu to bind VAO
        glBindBuffer(GL_ARRAY_BUFFER, VBO) #gpu bind VBO in VAO
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)
        #dynamic draw?? says little faster..but..

        
        replacer = {}  # for update. stores offset, bytes.
        #--------vert_data is without indices.
        float_size = np.float32(0.0).nbytes
        offset = ctypes.c_void_p(0)  # is bytes offset
        loc = 0  # NOTE:opengl core no attr 0-what this mean?
        for name, data_len in lengths.items():
            size = data_len//points  # size is 2,3,4
            byte_len = data_len * float_size
            replacer[name] =  (offset, byte_len)
            
            glVertexAttribPointer(loc, size, GL_FLOAT, GL_FALSE, 0, offset)  #(index, size, dtype, normalized, stride, offset)
            glEnableVertexAttribArray(loc)
            offset = ctypes.c_void_p( byte_len )
            loc+=1


        self.vao = VAO
        self.vbo = VBO
        self.ebo = EBO
        self.points = len(indices)
        self.replacer = replacer
    #========================
    def bind(self):
        if Vao.last != self:
            glBindVertexArray(self.vao)
            Vao.last = self    
    # def unbind(self):
    #     glBindVertexArray(0)

    def draw(self, kind=3):
        "0:point 1:line 2:lineloop 3:tri"
        draw_kind = draw_kinds.get(kind, GL_TRIANGLES)
        glDrawElements(draw_kind, self.points, GL_UNSIGNED_INT, None)
    #=================
    def update(self, name, data):
        "only changes vertex's data."
        #vao.update('position' , [ 0,0,0,   1,1,1,   1,0,0, ] )
        VAO = self.vao
        VBO = self.vbo
        #vertices = self.vertices
        #slicer = self.slices[name]
        #vertices[slicer] = value

        glBindVertexArray(VAO) #gpu bind VAO
        glBindBuffer(GL_ARRAY_BUFFER, VBO) #gpu bind VBO in VAO
        
        # replace whole VBO
        #glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
        
        # in-place
        #https://gamedev.stackexchange.com/questions/58417/how-to-modify-vbo-data
        #https://stackoverflow.com/questions/4854565/opengl-vbo-updating-data
        #https://registry.khronos.org/OpenGL-Refpages/gl4/html/glBufferSubData.xhtml
        offset,size = self.replacer[name]
        offset = 0 if offset.value is None else offset.value

        if type(data) != np.ndarray:
            data = np.array(data,dtype='float32')
        if len(data.shape) != 1:
            data = np.concatenate(data).astype('float32')  # [ p,p,p, n,n,n, u,u,u ]
        if data.dtype != np.float32:
            data = data.astype('float32')
        glBufferSubData(GL_ARRAY_BUFFER, offset, size, data)  # target offset size data


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



"""