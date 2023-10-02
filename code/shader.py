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
    last = 0
    def __init__(self, v_str=None, f_str=None):
        v_str = vertn if v_str is None else v_str
        f_str = fragn if f_str is None else f_str
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
                #happens window close.. why?
                #need someday log here and check.
            
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



