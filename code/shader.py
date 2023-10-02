from OpenGL.GL import *
from OpenGL.GL import shaders

default_vertex_str = """
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

default_fragment_str = """
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


cache = {}
#like tuple..recent input ->



def _too_complicated_get_fragment(shader_str, shader_type = 0):
    #match shader_type:
    if shader_type == 0:
        shader_type = GL_FRAGMENT_SHADER
    elif shader_type == 0:
        shader_type = GL_FRAGMENT_SHADER
    
    #default_shader_str[]
    shader = shaders.compileShader( shader_str , shader_type )
    return shader
        

#what if without window simulating, Visual created, and window open later?
#when required, shader is created..right? or visual.
#but what about texture?

_shader_holder = {}
#this kinds eats memory. need most-recent etc..

def _bad_dream():
    def get_vertex(shader_str):
        shader = _shader_holder.get(shader_str)
        if shader is None:
            shader = shaders.compileShader( shader_str, GL_VERTEX_SHADER)
            _shader_holder[shader_str] = _shader_holder
        return shader
        if shader_str is None:
            shader_str = default_vertex_str
    def get_fragment(shader_str):
        if shader_str is None:
            shader_str = default_vertex_str
        return shaders.compileShader( shader_str, GL_FRAGMENT_SHADER)
    def get_geometry(vertex_str):
        raise NotImplementedError('geomtry not yet!')

    def get_program(vertex_str, fragment_str, geometry_str=None):
        #compile error occurs, before window() 
        if bool(glCreateShader):
            program = shaders.compileProgram( vshader,fshader)
            glDeleteShader(vshader)
            glDeleteShader(fshader)
        else:
            program = -1






def _another__bad_dream():
    #so complex, since 'user' is None-> delete program.
    _shader_holder = {}


    def get_program(v_str, f_str, g_str=None):
        key = (v_str, f_str, g_str)
        program = _shader_holder.get(key,0)
        #compile error occurs, before window() 
        if program == 0:
            if bool(glCreateShader):  # do not try->return default here.
                vshader = shaders.compileShader( v_str, GL_VERTEX_SHADER)
                fshader = shaders.compileShader( f_str, GL_FRAGMENT_SHADER)
                program = shaders.compileProgram( vshader,fshader)
                glDeleteShader(vshader)
                glDeleteShader(fshader)
                _shader_holder[key] = program
        
        return program






class Shader:
    "is program holder. communicates with Material"
    last = 0
    def __init__(self, v_str=None, f_str=None):
        v_str = default_vertex_str if v_str is None else v_str
        f_str = default_fragment_str if f_str is None else f_str
        program = 0
        
        if bool(glCreateShader):  # do not try->return default here.
            vshader = shaders.compileShader( v_str, GL_VERTEX_SHADER)
            fshader = shaders.compileShader( f_str, GL_FRAGMENT_SHADER)
            program = shaders.compileProgram( vshader,fshader)
            glDeleteShader(vshader)
            glDeleteShader(fshader)

        self.program = program
        self.locations = {}

    def bind(self):
        if Shader.last == self.program:
            return
        Shader.last = self.program
        if bool(glUseProgram):  # seems py no need to bool..
            glUseProgram(self.program)
    def unbind(self): # do we need it? -> we need it, like create/update, bound lasts.
        Shader.last = 0
        if glUseProgram:
            glUseProgram(0)

    def __del__(self):
        Shader.last = 0  #don't forget it!
        #glCheckError? when window closed..
        if glDeleteProgram:
            #self.bind()
            try:
                glDeleteProgram(self.program)
            except GLError:
                pass
                #err = 1282   baseOperation = glDeleteProgram,    cArguments = (3,)
            
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

    #===requires bound.
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



