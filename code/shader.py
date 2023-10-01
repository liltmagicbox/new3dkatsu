from OpenGL.GL import *
from OpenGL.GL import shaders

vertn = """
#version 410 core
layout (location = 0) in vec3 position;
layout (location = 1) in vec3 color;
out vec3 out_color;

uniform mat4 Model;
//uniform mat4 View;
//uniform mat4 Projection;
uniform mat4 ProjectionView;

void main() 
{
    //gl_Position = ViewProjection * Model * vec4(pos, 1);
    
    //gl_Position = vec4(position, 1);
    //gl_Position = Projection * View * Model * vec4(position, 1);
    gl_Position = ProjectionView * Model * vec4(position, 1);
    out_color = vec3(1,0,1);
}

"""

fragn = """
#version 410 core

uniform vec3 unicolor; //has too?

in vec3 out_color;
out vec4 FragColor;
void main()
{
    FragColor = vec4(out_color,1);
    //FragColor = vec4(unicolor,1);
}
"""


class Shader:
    "is program holder. communicates with Material"
    last = None
    def __init__(self, vertex=None, fragment=None):
        if vertex is None:
            vertex = vertn
        if fragment is None:
            fragment = fragn

        #compile error occurs, before window() 
        if not bool(glCreateShader):
            return
        vshader = shaders.compileShader( vertex, GL_VERTEX_SHADER)
        fshader = shaders.compileShader( fragment, GL_FRAGMENT_SHADER)
        program = shaders.compileProgram( vshader,fshader)
        glDeleteShader(vshader)
        glDeleteShader(fshader)
        self.program = program
        self.locations = {}

    def bind(self):
        if Shader.last != self:
            Shader.last = self
            glUseProgram(self.program)
    # def unbind(self): # do we need it?
    #     glUseProgram(0)

    def __del__(self):
        if hasattr(self,'program'):
            glDeleteProgram(self.program)

    def get_loc_attribute(self, attribute_name):
        loc = glGetAttribLocation(self.program, attribute_name)
        return loc

    def get_loc_uniform(self, uniform_name):
        return glGetUniformLocation(self.program, uniform_name)
        # try:
        #     return self.locations[uniform_name]
        # except KeyError:
        #     location = glGetUniformLocation(self.program, uniform_name)
        #     if location == -1:
        #         raise KeyError(f'{uniform_name}is not found in the shader program.')
        #     self.locations[uniform_name] = location
        #     return location

    def set_int(self, uniform_name, value):
        loc = self.get_loc_uniform(uniform_name)
        glUniform1i(loc,value)
    def set_float(self, uniform_name, value):
        loc = self.get_loc_uniform(uniform_name)
        glUniform1f(loc,value)
    def set_vec2(self, uniform_name, vec2):
        loc = self.get_loc_uniform(uniform_name)
        glUniform2f(loc, *vec2)
    def set_vec3(self, uniform_name, vec3):
        loc = self.get_loc_uniform(uniform_name)
        glUniform3f(loc, *vec3)
    def set_mat4(self, uniform_name, mat4):
        loc = self.get_loc_uniform(uniform_name)
        glUniformMatrix4fv(loc,1,False, mat4)  # location count transpose data(nparr), transpose for row major..[1,2,3,4, ,]
    
    #not yet
    def set_mat4s(self, uniform_name, mat4s):
        loc = self.get_loc_uniform(uniform_name)
        glUniformMatrix4fv(loc, len(mat4s) ,False, mat4s)  # location count transpose data(nparr), transpose for row major..[1,2,3,4, ,]



