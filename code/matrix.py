from vecops import *

class Matrix:
    def __init__(self, *args):
        if len(args) == 0:
            data = (0.0,0.0,0.0,0.0, 0.0,0.0,0.0,0.0, 0.0,0.0,0.0,0.0, 0.0,0.0,0.0,0.0)
        elif len(args) == 16:
            data = args
        else:
            raise ValueError('Matrix requires 16s!')
        self.data = data
    def __repr__(self):
        return str(self.data)

    def __imul__(self, other):
        self.data = mul4x4(self.data, other.data)
    def __mul__(self, other):
        mat = Matrix()
        mat.data = mul4x4(self.data, other.data)
        return mat

    def to_list(self):
        return list(self.data)
    def to_tuple(self):
        return tuple(self.data)

    @classmethod
    def Perspective(cls, fov,ratio,near,far):
        return cls(*gl_perspective(fov,ratio,near,far))
    @classmethod
    def Ortho(cls, left, right, bottom, top, near, far):
        return cls(*gl_ortho(left, right, bottom, top, near, far))
    @classmethod
    def View(cls, eye, center, up):
        return cls(*gl_lookAt(eye,center,up))

    @classmethod
    def Translate(cls, xyz):
        return cls(*gl_translate(xyz) )
    @classmethod
    def Scale(cls, xyz):
        return cls(*gl_scale(xyz) )
    @classmethod
    def Rotate(cls, angle,axis):
        return cls(*gl_rotate(angle,axis) )
    
    @classmethod
    def translate(cls, matrix, xyz):
        t = gl_translate(xyz)
        data = mul4x4(matrix.data, t)
        return cls( *data )

        # T = cls.Translate(xyz)
        # return matrix * T

        # x,y,z = xyz
        # data = matrix.to_list()
        # data[12] += x
        # data[13] += y
        # data[14] += z
        # return cls(*data)
    @classmethod
    def scale(cls, matrix, xyz):
        s = gl_scale(xyz)
        data = mul4x4(matrix.data, s)
        return cls( *data )

        # S = cls.Scale(xyz)
        # return matrix * S

        #since first M meets, fine.
        # x,y,z = xyz
        # data = matrix.to_list()
        # data[0] *= x
        # data[5] *= y
        # data[10] *= z
        # return cls(*data)
    @classmethod
    def rotate(cls, matrix, angle,axis):
        r = gl_rotate(angle,axis)
        data = mul4x4(matrix.data, r)
        return cls( *data )

        # R = cls.Rotate(angle,axis)
        # return matrix * R

    @classmethod
    def Model(cls, pos, rot, scale):
        #M = cls.translate(M, pos)
        #M = cls.rotate(M, )
        #M = cls.scale(M, scale)
        return make_Model(pos,rot,scale)

    
#deprecated by quat->rot.
# #original. 20000s took 1 seconds.
# def make_Model(pos,rot,scale):
#     T = Matrix.Translate(pos)
#     R = Matrix.Rotate(rot)
#     S = Matrix.Scale(scale)
#     M = T*R*S
#     return M

# #.84 to .60
# def make_Model(pos,rot,scale):
#     R = Matrix.Rotate(rot)
#     S = Matrix.Scale(scale)
#     M = R*S
#     data = M.to_list()
#     data[12],data[13],data[14] = pos
#     M.data = tuple(data)
#     return M


#.60 to .50, x2 faster.
#40000 to 1seconds, 400 to 10ms, acceptable.
def make_Model(pos,rot,scale):
    rot = quat_from_euler(rot)
    r = quat_to_matrix(rot)
    s = gl_scale(scale)
    m = mul4x4(r,s)
    data = list(m)
    data[12],data[13],data[14] = pos
    return Matrix(*data)



def glm_matrix_rot_test():
    import glm
    R = glm.rotate(1, glm.vec3(1,2,3) )
    print(R.to_list())
    R = gl_rotate(1, (1,2,3))
    print(R)
    R = Matrix.Rotate(1, (1,2,3))
    print(R)

    print('roll')
    R = glm.rotate(1, glm.vec3(1,0,0) )
    print(R.to_list())
    RR = gl_rotate(1, (1,0,0))
    print(RR)
    RR = Matrix.Rotate(1, (1,0,0))
    print(RR)

    print('pitch')
    P = glm.rotate(1, glm.vec3(0,0,1) )
    print(P.to_list())
    PP = gl_rotate(1, (0,0,1))
    print(PP)
    PP = Matrix.Rotate(1, (0,0,1))
    print(PP)

    print('yaw')
    Y = glm.rotate(1, glm.vec3(0,1,0) )
    print(Y.to_list())
    YY = gl_rotate(1, (0,1,0))
    print(YY)
    YY = Matrix.Rotate(1, (0,1,0))
    print(YY)

    print("mix")
    print( (Y*P*R).to_list() )
    print(YY*PP*RR)


#==============reference.. for rotation matrix
# rotate by xaaxis is ..roll. z is pitch. gl-coord.system.
# import glm
# def make_Model(pos,rot,scale):
#     x,y,z = rot
#     R = glm.rotate(x, glm.vec3(1,0,0)) #x to roll
#     Y = glm.rotate(y, glm.vec3(0,1,0)) #y to yaw
#     P = glm.rotate(z, glm.vec3(0,0,1)) #z to pitch.
#     #RR = R*P*Y #this not correct.
#     #RR = P*Y*R #why this correct?? , yes, this is winner. R is last-ed.,
#     #RR = Y*P*R fail yaw test.
    
#     RR = Y*P*R #is what i want. roll-finally,   yaw is first... as it looks like. great! finally!
#     #AH, it should be reversed, roll-first. so it be.
#     #turn on drill,roll,   head up, pitch,   turn to enemy, yaw.
#     return RR

#confirm.
# def make_Model(pos,rot,scale):
#     x,y,z = rot
#     R = Matrix.Rotate(x, (1,0,0)) #x to roll
#     Y = Matrix.Rotate(y, (0,1,0)) #y to yaw
#     P = Matrix.Rotate(z, (0,0,1)) #z to pitch.
#     RR = Y*P*R #is what i want.
#     #turn on drill,roll,   head up, pitch,   turn to enemy, yaw.
#     return RR



#================================================================== test
#================================================================== test
#================================================================== test
#================================================================== test
#================================================================== test
#================================================================== test
#================================================================== test
#================================================================== test
#================================================================== test
#================================================================== test
#================================================================== test
#================================================================== test
def _operator_test():
    #[[1.0, 2.0, 3.0, 4.0], [4.0, 3.0, 2.0, 1.0], [1.0, 3.0, 2.0, 4.0], [1.0, 1.0, 2.0, 3.0]]
    x = glm.mat4x4(1,2,3,4,5,6,7,8, 1,2,3,4, 1,2,3,4)
    print(x.to_list())
    y = glm.mat4x4(9,8,7,6,5,4,3,2, 4,3,2,1, 4,3,2,1)
    print( (x*y).to_list() )

    x = Matrix(1,2,3,4,5,6,7,8, 1,2,3,4, 1,2,3,4)
    print(x)
    y = Matrix(9,8,7,6,5,4,3,2, 4,3,2,1, 4,3,2,1)
    print(x*y)

    #col major, Projection View Model Position.
    r = Matrix(2,4,6,0, 0,1,0,0, 0,0,1,0, 0,0,0,1)
    t = Matrix(1,0,0,0, 0,1,0,0, 0,0,1,0, 1,2,3,1)
    print(t)
    print(t*r)
    #...glm is T R S








def _glmat_test():
    #=== vp test
    import glm
    #finally!!!!!
    Projection = glm.perspective( 1, 1.96,0.1,200)
    View = glm.lookAt( glm.vec3(1,3,4),glm.vec3(0,0,0), glm.vec3(0,1,0))
    #print((Projection).to_list())
    #print((View).to_list())
    print((Projection*View).to_list())

    Projection = Matrix.Perspective( 1, 1.96,0.1,200)
    View = Matrix.View( (1,3,4),(0,0,0), (0,1,0))
    #print((Projection).to_list())
    #print((View).to_list())
    print((Projection*View).to_list())



    T = glm.translate( glm.vec3(1,2,3) )
    print(T.to_list())
    T = gl_translate( (1,2,3) )
    print(T)
    T = Matrix.Translate( (1,2,3) )
    print(T.to_list())


    #=== T R S each test
    import glm
    M = glm.mat4x4(1,0,0,0, 0,1,0,0, 0,0,1,0, 0,0,0,1)
    M = glm.translate(M, glm.vec3(10,100,1000))
    print(M.to_list())

    M = glm.mat4x4(1,0,0,0, 0,1,0,0, 0,0,1,0, 0,0,0,1)
    T = glm.translate(glm.vec3(10,100,1000))
    print( (M*T).to_list())

    M = Matrix(1,0,0,0, 0,1,0,0, 0,0,1,0, 0,0,0,1)
    M = Matrix.translate(M, (10,100,1000))
    print(M.to_list())


    M = glm.mat4x4(1,0,0,0, 0,1,0,0, 0,0,1,0, 0,0,0,1)
    M = glm.scale(M, glm.vec3(10,100,1000))
    print(M.to_list())

    M = glm.mat4x4(1,0,0,0, 0,1,0,0, 0,0,1,0, 0,0,0,1)
    S = glm.scale(glm.vec3(10,100,1000))
    print( (M*S).to_list())

    M = Matrix(1,0,0,0, 0,1,0,0, 0,0,1,0, 0,0,0,1)
    M = Matrix.scale(M, (10,100,1000))
    print(M.to_list())


    R = glm.rotate( 0.1, glm.vec3(0,0,1) )
    R = glm.rotate( 0.1, glm.vec3(1,2,3) )
    print(R.to_list())

    R = gl_rotate( 0.1, (0,0,1) )
    R = gl_rotate( 0.1, (1,2,3) )
    print(R)


    #=== TRS test
    #glm is stacking. so last one is recent.
    import glm
    M = glm.mat4x4(1,0,0,0, 0,1,0,0, 0,0,1,0, 0,0,0,1)
    M = glm.translate(M, glm.vec3(11,22,33))
    M = glm.rotate(M, 0.1, glm.vec3(1,2,3))
    M = glm.scale(M, glm.vec3(10,100,1000))
    print(M.to_list())

    M = Matrix(1,0,0,0, 0,1,0,0, 0,0,1,0, 0,0,0,1)
    M = Matrix.translate(M, (11,22,33))
    M = Matrix.rotate(M, 0.1, (1,2,3))
    M = Matrix.scale(M, (10,100,1000))
    print(M.to_list())

    #while multiplying,, works as expected.
    M = Matrix(1,0,0,0, 0,1,0,0, 0,0,1,0, 0,0,0,1)
    T = Matrix.Translate((11,22,33))
    R = Matrix.Rotate(0.1, (1,2,3))
    S = Matrix.Scale((10,100,1000))
    M = T*R*S*M
    print(M.to_list())


    quat = quat_angleaxis( 0.1, (0,0,1) )
    M = Matrix.Model( (11,22,33), quat, (100,100,100))
    print(M)





def glmvstimetest():
    import time
    tt=time.time

    t=tt()
    import glm

    for i in range(200000):
        M = glm.mat4x4(1,0,0,0, 0,1,0,0, 0,0,1,0, 0,0,0,1)
        M = glm.translate(M, glm.vec3(11,22,33))
        M = glm.rotate(M, 0.1, glm.vec3(1,2,3))
        M = glm.scale(M, glm.vec3(10,100,1000))
    print(M.to_list())
    print(tt()-t)

    # quat
    #200 -> 1ms
    #20 -> 1ms

    M = Matrix(1,0,0,0, 0,1,0,0, 0,0,1,0, 0,0,0,1)
    M = Matrix.translate(M, (11,22,33))
    M = Matrix.rotate(M, 0.1, (1,2,3))
    M = Matrix.scale(M, (10,100,1000))
    print(M.to_list())

if __name__ == '__main__':
    glmvstimetest()
    #main()






