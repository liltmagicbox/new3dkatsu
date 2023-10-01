from math import sqrt , acos, sin,cos, atan2, asin , radians, tan

desc = """
not using Quat/Vec3, but functions. for functional.

returns tuple, better.

"""

#=== vector
#=== vector
#=== vector
#=== vector
#=== vector

def dot(x1,y1,z1, x2,y2,z2):
    return x1*x2 + y1*y2 + z1*z2
def cross(ax,ay,az, bx,by,bz):
    #xyzzy
    cx = ay*bz-az*by
    cy = az*bx-ax*bz
    cz = ax*by-ay*bx
    return cx,cy,cz
def normalize(x,y,z):
    mag = sqrt(x**2+y**2+z**2)
    if mag == 0:
        return 0,0,0
    return x/mag, y/mag, z/mag

def mag(x,y,z):
    "is norm, also."
    return sqrt(x**2+y**2+z**2)
def mag2(x,y,z):
    return x**2+y**2+z**2


def angle(a,b,c,  d,e,f):
    "between directions."
    #costh = _dot(a,b,c, d,e,f) / ( _mag(a,b,c) * _mag(d,e,f) )
    costh = (a*d + b*e + c*f) / sqrt( (a**2+b**2+c**2)*(d**2+e**2+f**2)  )
    return acos(costh)

def axis(a,b,c, d,e,f):
    axis = cross(a,b,c, d,e,f)
    return normalize(*axis)

def vv_to_aa(v1,v2):
    """v1,v2 -> axis,th
    """
    front = normalize(*v1)
    facing = normalize(*v2)
    
    #---qv
    axis = cross(*front, *facing)#result not unit vector
    axis = normalize(*axis)
    #---qs    
    th = acos( dot(*front,*facing) )
    return axis,th
    # v1 = (1.1,2.2,2.5)
    # v2 = (1,2,3)
    # x = quataxis(v1,v2)
    # print(x)
    # x = axis(*v1,*v2)
    # print(x)
    # x = angle(*v1,*v2)
    # print(x)




#====================================matrix
#====================================matrix
#====================================matrix
#====================================matrix


def dot4(A,B):
    A0,A1,A2,A3 = A
    B0,B1,B2,B3 = B
    return A0*B0 + A1*B1 + A2*B2 + A3*B3

def mul4x4(A,B):
    "extreamly ineff."
    A,B = B,A #for glm.mat4x4.
    a0,a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12,a13,a14,a15 = A
    b0,b1,b2,b3,b4,b5,b6,b7,b8,b9,b10,b11,b12,b13,b14,b15 = B
    
    row0 = a0,a1,a2,a3
    row1 = a4,a5,a6,a7
    row2 = a8,a9,a10,a11
    row3 = a12,a13,a14,a15
    
    col0 = b0,b4,b8,b12
    col1 = b1,b5,b9,b13
    col2 = b2,b6,b10,b14
    col3 = b3,b7,b11,b15

    mat = (
    dot4(row0,col0), dot4(row0,col1), dot4(row0,col2), dot4(row0,col3), 
    dot4(row1,col0), dot4(row1,col1), dot4(row1,col2), dot4(row1,col3), 
    dot4(row2,col0), dot4(row2,col1), dot4(row2,col2), dot4(row2,col3), 
    dot4(row3,col0), dot4(row3,col1), dot4(row3,col2), dot4(row3,col3), )
    return mat








#==============================gl matrix
#==============================gl matrix
#==============================gl matrix
#==============================gl matrix
#==============================gl matrix
#==============================gl matrix
#==============================gl matrix

def gl_ortho(left, right, bottom, top, near,far):
    a = right - left
    b = top - bottom
    c = far - near
    mat = ( 
        2/a, 0,0,0,
        0, 2/b, 0,0,
        0,0, -2/c, 0,0,
        -(right+left)/a, -(top+bottom)/b, -(far+near)/c ,1.0
        )
    return mat

def gl_perspective(fov, ratio, near, far):
    "fov=radians, perspective list is platten col-major mat."
    f = 1/tan(fov/2)
    mat = ( f/ratio, 0, 0, 0,
      0,   f,  0, 0, 
      0,   0,  (far+near)/(near-far), -1,
      0,  0,   (2*far*near)/(near-far),  0)
    return mat


def gl_lookAt(eye,center,up):
    """
    https://www.khronos.org/opengl/wiki/GluLookAt_code
    https://registry.khronos.org/OpenGL-Refpages/gl2.1/xhtml/gluLookAt.xml
    side: both lh,rh same.
    https://learnopengl.com/Getting-started/Camera
    has bad explaination, name direction is actually..
    """
    tx,ty,tz = center
    ex,ey,ez = eye

    forward = tx-ex, ty-ey, tz-ez
    forward = normalize(*forward)
    if forward == up:
        forward = up[0],up[1],up[2]+0.01
    side = cross(*forward, *up)
    side = normalize(*side)
    up = cross(*side, *forward)
    up = normalize(*up)
    
    fx,fy,fz = forward
    sx,sy,sz = side
    ux,uy,uz = up

    #traditional. v1 is rev.R, v2 is rev.T..?
    #https://registry.khronos.org/OpenGL-Refpages/gl2.1/xhtml/gluLookAt.xml
    # v1 = (
    # sx,ux,-fx,0,
    # sy,uy,-fy,0,
    # sz,uz,-fz,0,
    # 0,0,0,1)
    # v2 = (1,0,0,0, 0,1,0,0, 0,0,1,0, -ex,-ey,-ez,1)
    # return mul4x4(v1,v2)

    #mixed,faster
    #px,py,pz = eye.dot(side), eye.dot(up), eye.dot(forward)#simulates M1*M2..
    #px,py,pz = -eye.dot(side), -eye.dot(up), eye.dot(forward)#not right, side-effected.
    #why -,-,+?
    px = -dot(*eye,*side)
    py = -dot(*eye,*up)
    pz = dot(*eye,*forward)
    mixed = (
    sx,ux,-fx,0,
    sy,uy,-fy,0,
    sz,uz,-fz,0,
    px,py,pz, 1.0
    )
    return mixed



def gl_translate(xyz):
    x,y,z = xyz
    return (1,0,0,0, 0,1,0,0, 0,0,1,0, x,y,z,1)

def gl_scale(xyz):
    x,y,z = xyz
    return (x,0,0,0, 0,y,0,0, 0,0,z,0, 0,0,0,1)

#since glm's is so.
def gl_rotate(angle, axis):
    quat = quat_from_aa(angle,axis)
    return quat_to_matrix(quat)





#================================ euler
#================================ euler
#================================ euler
#================================ euler
#================================ euler
#================================ euler
#================================ euler
#================================ euler
#================================ euler
#================================ euler


#https://learnopengl.com/Getting-started/Camera
#https://learnopengl.com/code_viewer.php?type=header&code=camera
#original code is yup, LH rule. x is pitch.
#https://stackoverflow.com/questions/1568568/how-to-convert-euler-angles-to-directional-vector
#this explains really well.

def _cam_euler_to_front(roll,pitch,yaw):
    """angle:radians/front:1,0,0/yup-RH/x:roll/z:pitch/y:yaw
    gl screen coords,  y is up, x is to pitch. while z is roll.
    but i prefer roll-pitch-yaw x,y,z notation.
    """
    #this is tuned for scrren dxdy. dir.y should be -sin(pitch), pitch = -pitch, (since it is LH.) originally.
    yaw = -yaw #for RH rotation.
    r89 = radians(89.0)
    if pitch > r89:
        pitch = r89
    if pitch < -r89:
        pitch = -r89

    direction_x = cos(yaw) * cos(pitch)
    direction_z = sin(yaw) * cos(pitch)
    direction_y = sin(pitch)
    front = normalize(direction_x,direction_y,direction_z)
    return front


def safe_pitch(pitch):
    "prevents gimbal lock"
    r89 = radians(89.0)
    if pitch > r89:
        pitch = r89
    if pitch < -r89:
        pitch = -r89
    return pitch

"""RH yup
https://stackoverflow.com/questions/1568568/how-to-convert-euler-angles-to-directional-vector

the code ws little not correct,
from chatgpt
Total Rotation Matrix:
c(yaw)*c(pitch), -s(yaw)*c(roll) + c(yaw)*s(pitch)*s(roll)     s(yaw)*s(roll) + c(yaw)*s(pitch)*c(roll)]
s(yaw)*c(pitch),  c(yaw)*c(roll) + s(yaw)*s(pitch)*s(roll)    -c(yaw)*s(roll) + s(yaw)*s(pitch)*c(roll)]
-s(pitch)                          c(pitch)*s(roll)                                      c(pitch)*c(roll)

we only did z-y swap,  LH->RH.
"""

def euler_to_front(roll,pitch,yaw):
    pitch = -pitch
    yaw = -yaw
    roll = -roll
    x = cos(yaw) * cos(pitch)
    z = sin(yaw) * cos(pitch)
    y = -sin(pitch)
    return x,y,z

def euler_to_right(roll,pitch,yaw):
    pitch = -pitch
    yaw = -yaw
    roll = -roll
    x = cos(yaw)*sin(pitch)*sin(roll) - sin(yaw)*cos(roll)
    z = sin(yaw)*sin(pitch)*sin(roll) + cos(yaw)*cos(roll)
    y = cos(pitch)*sin(roll)
    return x,y,z

def euler_to_up(roll,pitch,yaw):
    pitch = -pitch
    yaw = -yaw
    roll = -roll
    x = cos(yaw)*sin(pitch)*cos(roll) + sin(yaw)*sin(roll)
    z = sin(yaw)*sin(pitch)*cos(roll) - cos(yaw)*sin(roll)
    y =  cos(pitch)*cos(roll)
    return x,y,z


def front_to_euler(front):
    return euler




def mview_rotation(eye,target,upV):
    """input each vector..4! no tuple."""
    front = target - eye
    front = front/norm(front)

    right = cross(upV, front)
    right = right/norm(right)

    up = cross(front, right)
    up = up/norm(up)
    
    view1 = [
    [right[0],right[1],right[2],0],
    [up[0],up[1],up[2],0],
    [front[0],front[1],front[2],0],
    [0,0,0,1]]

def euler_to_matrix(euler):
    return mat




#**********this is the result of discuss.
def front_rotate(front, angle,axis):
    quat = quat_from_aa(angle,axis)
    xyz = quat_rotate_xyz(quat, front)
    return xyz







#================================ quaternion
#================================ quaternion
#================================ quaternion
#================================ quaternion
#================================ quaternion
#================================ quaternion
#================================ quaternion
#================================ quaternion
#================================ quaternion
#x,y,z,w radians


#def quat_look(quat, target):
#use front- cross-method. axis angle

discuss = """
euler->front(low cost)
front,target -> aa
rotate( aa, front) -> front
front->euler
euler->mat4


fine, but we use quat.

quat_to_current
quat_1,0,0, to target

quat toward target * -quat_to_current
front = normalize(*target)
xyz = front_to_euler(front)
quat = quat_from_euler(xyz)



finally,
xyz euler to store rotation.
for physical-simulation, vel,acc of rotation.

use quat to angle-axis rotation.

set rotation by front , up, too.
new_front = target - pos

we not that chage xyz, directly.
front-right-up is stored, dynamically,
easy to rotation matrix!

flow:

1.physically accurate
physical simulation:
xyz vel, acc.
 xyz -> front,up,right

2.override
front-up kinds. rotate front, using quat_rotate_xyz.

3.front-up-right to Rotation.

quat only used for angle-axis rotation.
"""




def quat_from_target(target):
    "1,0,0 looking target"
    angle,axis = vv_to_aa( (1,0,0), target)
    quat = quat_from_aa(angle*ratio, axis)
    return quat


def _quat_from_target(target, ratio = 1.0):
    "1,0,0 to target, see how inefficient it is."
    direction = quat_to_direction(quat)
    angle,axis = vv_to_aa(direction, target)
    quat = quat_from_aa(angle*ratio, axis)
    new_front = quat_rotate_xyz(quat,direction)
    return new_front

#need: rotate by self.front.. to UP.


#https://math.stackexchange.com/questions/40164/how-do-you-rotate-a-vector-by-a-unit-quaternion
def quat_from_aa(angle,axis):
    #https://danceswithcode.net/engineeringnotes/quaternions/quaternions.html
    #"axis should be normalized.. since x*[0-1.0].."
    axis = normalize(*axis)

    w = cos(angle/2)  # scalar

    #x,y,z = axis *sin(th/2) #vector
    sin_th2 = sin(angle/2)
    ax,ay,az = axis
    x = ax * sin_th2
    y = ay * sin_th2
    z = az * sin_th2
    return x,y,z,w


def quat_to_aa(quat):
    """
    https://danceswithcode.net/engineeringnotes/quaternions/quaternions.html
    It is worth noting that there are several ways to conv..
    """
    x,y,z,w = quat

    angle = 2*acos(w)

    sin_th2 = sin(angle/2)
    if sin_th2 <0.001:#0.06deg
        return 0, 1,0,0
    ax = x/sin_th2
    ay = y/sin_th2
    az = z/sin_th2
    return angle, ax,ay,az

def quat_to_matrix(quat):
    """col-major. downward.
    https://en.wikipedia.org/wiki/Quaternions_and_spatial_rotation"""
    x,y,z,w = quat
    mat = (
    1 - 2*y**2 - 2*z**2,  2*x*y + 2*z*w,  2*x*z - 2*y*w, 0,
    2*x*y - 2*z*w,  1 - 2*x**2 - 2*z**2,  2*y*z + 2*x*w, 0,
    2*x*z + 2*y*w,  2*y*z - 2*x*w,  1 - 2*x**2 - 2*y**2, 0,
    0,0,0,1
    )
    return mat






def quat_rotate_xyz(quat, xyz):
    """
    rotate position x,y,z
    returns not normalized. #1.5-8x faster than qpq way.
    https://en.wikipedia.org/wiki/Conversion_between_quaternions_and_Euler_angles
    
    history is below,there were times v*v -> v.
    v + qw*tv +qv*tv
    rx = x + qw*tx +qx*tx
    ry = y + qw*ty +qy*ty
    rz = z + qw*tz +qz*tz
    """

    qx,qy,qz,qw = quat
    x,y,z = xyz
    #qhat requires normlized?
    # mag = sqrt(qw**2+ qx**2+ qy**2+ qz**2)
    # qw /= mag
    # qx /= mag
    # qy /= mag
    # qz /= mag

    # v=xyz  v'= rotated xyz
    # quat ->  qw, qv
    # t = 2* (q X v)
    # v' = v + qw*t + (qv X t)
    
    #tx,ty,tz = _cross(qx,qy,qz, x,y,z)
    #tx *=2
    #ty *=2
    #tz *=2
    #cross acts like this..
    tx,ty,tz = cross(qx*2,qy*2,qz*2, x,y,z)
    
    ctx,cty,ctz = cross(qx,qy,qz, tx,ty,tz)
    rx = x + qw*tx + ctx
    ry = y + qw*ty + cty
    rz = z + qw*tz + ctz
    return rx,ry,rz


def quat_to_direction(quat):
    return quat_rotate_xyz(quat, (1,0,0) )





#================================ with euler
#================================ with euler
#================================ with euler
#from here, input xyz is roll,yaw,pitch, as glcoords.

def quat_from_euler(xyz):
    #https://en.wikipedia.org/wiki/Conversion_between_quaternions_and_Euler_angles
    #Euler angles to quaternion conversion
    #says 3,2,1 , yaw->pitch->roll
    #...was the suspect. took 30mins.
    #syas y:pitch z:yaw.ah.

    #by each axis. orignally zup.
    #so we can't say simply, yis yaw-axis. it depends.
    roll,pitch,yaw = xyz
    cr = cos(roll/2)
    sr = sin(roll/2)
    cp = cos(pitch/2)
    sp = sin(pitch/2)
    cy = cos(yaw/2)
    sy = sin(yaw/2)

    w = cr * cp * cy + sr * sp * sy
    x = sr * cp * cy - cr * sp * sy
    y = cr * sp * cy + sr * cp * sy
    z = cr * cp * sy - sr * sp * cy
    return x,y,z,w


def quateulermaker():

    import glm
    #pitch yaw roll = xyz
    x = glm.quat( glm.vec3(3,2,1) )
    print(x)
    xx = quat_from_euler(3,2,1)
    print(xx)
    #Returns euler angles, pitch as x, yaw as y, roll as z. The result is expressed in radians.
    #why? the only not agree-able.

    print('m')
    #quat_to_matrix()
    x = glm.mat4_cast(x)
    print(x.to_list())
    print('my')
    xx = quat_to_matrix(xx)
    print(xx)


    print('rotmat')
    P = glm.rotate(3, glm.vec3(1,0,0)) #x to pitch
    Y = glm.rotate(2, glm.vec3(0,1,0)) #y to yaw
    R = glm.rotate(1, glm.vec3(0,0,1)) #z to roll.
    #RR = Y*P*R #is what i want. roll-finally,   yaw is first... as it looks like. great! finally!
    RR = R*Y*P
    print(RR.to_list())
    #...this is screen coord.! x is pitch.
#quateulermaker()


def quat_to_euler(quat):
    "roll pitch yaw"
    #https://en.wikipedia.org/wiki/Conversion_between_quaternions_and_Euler_angles
    x,y,z,w = quat
    #roll (x-axis rotation)
    sinr_cosp = 2 * (w * x + y * z)
    cosr_cosp = 1 - 2 * (x * x + y * y)
    roll = atan2(sinr_cosp, cosr_cosp)

    #pitch (y-axis rotation)
    sinp = 2 * (w * y - z * x)
    if abs(sinp) >= 1:
        pitch = 1.57 #use 90 degrees if out of range
    else:
        pitch = asin(sinp)

    #yaw (z-axis rotation)
    siny_cosp = 2 * (w * z + x * y)
    cosy_cosp = 1 - 2 * (y * y + z * z)
    yaw = atan2(siny_cosp, cosy_cosp)
    return roll,pitch,yaw


def rotate_is_the_boss():
    """
    seems glm's is T-ed. while quat-to-from is great.
    why??
    R*P*Y* Position
    Roll is the last, right?
    as like Projection * View.

    fine, but somewhat reason, it is T-ed. why?

    """
    #https://learnopengl.com/Getting-started/Transformations

    #quat = quat_from_euler(1,3,2)
    quat = quat_from_euler(1,2,3)
    x = quat_to_matrix(quat)
    print(x)
    #Y 0> P 0> R

    import glm
    R = glm.rotate(1, glm.vec3(1,0,0)) #x to roll
    P = glm.rotate(2, glm.vec3(0,0,1)) #z to pitch.
    Y = glm.rotate(3, glm.vec3(0,1,0)) #y to yaw

    RR = R*P*Y
    print(RR.to_list())
    #print(RR.to_list())
    #RR = P*Y*R#winner!


    #glm.rotate(0.1, glm.vec3(0,0,1) )
    #mat4x4(( 0.995004, 0.0998334, 0, 0 ), ( -0.0998334, 0.995004, 0, 0 ), ( 0, 0, 1, 0 ), ( 0, 0, 0, 1 ))

def rotmattest2():
    quat = quat_from_euler(1,2,3)
    x = quat_to_matrix(quat)
    print(x)
    #Y 0> P 0> R

    import glm
    R = glm.rotate(1, glm.vec3(1,0,0)) #x to roll
    Y = glm.rotate(2, glm.vec3(0,1,0)) #y to yaw
    P = glm.rotate(3, glm.vec3(0,0,1)) #z to pitch.

    #RR = P*Y*R #why this correct??
    RR = R*P*Y
    print(RR.to_list())
    #print(RR.to_list())


#quat = quat_from_euler(1,2,3)
#x = quat_to_matrix(quat)
#print(x)


#operations input args..?
def normalize_quat(qx, qy, qz, qw):
    magnitude = sqrt(qw**2 + qx**2 + qy**2 + qz**2)
    normalized_qw = qw / magnitude
    normalized_qx = qx / magnitude
    normalized_qy = qy / magnitude
    normalized_qz = qz / magnitude
    return normalized_qw, normalized_qx, normalized_qy, normalized_qz

def mul_quat(w1,x1,y1,z1, w2,x2,y2,z2):
    """https://en.wikipedia.org/wiki/Quaternion
    hamilton product, q1->q2.
    ..and it was grassman!
    """
    # grassman
    # cx,cy,cz = _cross(x1,y1,z1, x2,y2,z2)
    # w = w1*w2 - _dot(x1,y1,z1, x2,y2,z2)
    # x = w1*x2+ w2*x1 + cx
    # y = w1*y2+ w2*y1 + cy
    # z = w1*z2+ w2*z1 + cz

    w = w1*w2 - x1*x2 - y1*y2 - z1*z2
    x = w1*x2 + x1*w2 + y1*z2 - z1*y2
    y = w1*y2 - x1*z2 + y1*w2 + z1*x2
    z = w1*z2 + x1*y2 - y1*x2 + z1*w2
    return w,x,y,z

def inverse_quat(w,x,y,z):
    """
    conjugation is -q.
    -q / mag2(q)
    https://en.wikipedia.org/wiki/Quaternion
    """
    mag2 = w**2+x**2+y**2+z**2
    w /= mag2
    x /= -mag2
    y /= -mag2
    z /= -mag2
    return w,x,y,z





















#============================ test
#============================ test
#============================ test
#============================ test
#============================ test
#============================ test
#============================ test
#============================ test
#============================ test





def operatior_test():
    import glm
    x= glm.dot( glm.vec3(1,2,3) , glm.vec3(6,7,8))
    print(x)
    x= glm.dot( glm.vec3(6,7,8) , glm.vec3(1,2,3))
    print(x)
    x = dot( 1,2,3, 6,7,8)
    print(x)
    x = dot( 6,7,8,1,2,3)
    print(x)

    x= glm.cross( glm.vec3(1,2,3) , glm.vec3(6,7,8))
    print(x)
    x= glm.cross( glm.vec3(6,7,8) , glm.vec3(1,2,3))
    print(x)
    x = cross( 1,2,3, 6,7,8)
    print(x)
    x = cross( 6,7,8,1,2,3)
    print(x)

    x= glm.normalize( glm.vec3(1,2,3))
    print(x)
    x= glm.normalize( glm.vec3(6,7,8) )
    print(x)
    x = normalize( 1,2,3)
    print(x)
    x = normalize( 6,7,8)
    print(x)


def matrix_test():
    #=== projection test
    import glm
    print( glm.perspective(radians(40), 1.96,0.1,200).to_list() )
    x = gl_perspective( radians(40) , 1.96, 0.1, 200)
    print(x)

    print('-=--ortho---')

    print( glm.ortho( 0,1,0,1,0,1 ).to_list() )
    x = gl_ortho( 0,1,0,1,0,1 )
    print(x)
    print( glm.ortho( 1,3,5,7,9,2 ).to_list() )
    x = gl_ortho( 1,3,5,7,9,2 )
    print(x)





def eulertotest():
    print('roll')
    for i in range(10):
        x = euler_to_up(i/10,0,0)
        print(x)
    print('pitch')
    for i in range(10):
        x = euler_to_up(0,i/10,0)
        print(x)
    print('yaw')
    for i in range(10):
        x = euler_to_up(0,0,i/10)
        print(x)
    





#===========================================================technical
#===========================================================technical
#===========================================================technical
#===========================================================technical
#===========================================================technical
#===========================================================technical
#===========================================================technical
#===========================================================technical
#===========================================================technical
def _mul4x4(A,B):
    "for easy understanding"
    A,B = B,A #for glm.mat4x4.
    a0,a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12,a13,a14,a15 = A
    b0,b1,b2,b3,b4,b5,b6,b7,b8,b9,b10,b11,b12,b13,b14,b15 = B
    
    row0 = a0,a1,a2,a3
    row1 = a4,a5,a6,a7
    row2 = a8,a9,a10,a11
    row3 = a12,a13,a14,a15
    
    col0 = b0,b4,b8,b12
    col1 = b1,b5,b9,b13
    col2 = b2,b6,b10,b14
    col3 = b3,b7,b11,b15

    m0 = dot4(row0,col0)
    m1 = dot4(row0,col1)
    m2 = dot4(row0,col2)
    m3 = dot4(row0,col3)
    
    m4 = dot4(row1,col0)
    m5 = dot4(row1,col1)
    m6 = dot4(row1,col2)
    m7 = dot4(row1,col3)
    
    m8 = dot4(row2,col0)
    m9 = dot4(row2,col1)
    m10 = dot4(row2,col2)
    m11 = dot4(row2,col3)
    
    m12 = dot4(row3,col0)
    m13 = dot4(row3,col1)
    m14 = dot4(row3,col2)
    m15 = dot4(row3,col3)
    return (m0,m1,m2,m3,m4,m5,m6,m7,m8,m9,m10,m11,m12,m13,m14,m15)




def _gllookat(eye,center,up):
    """
    https://www.khronos.org/opengl/wiki/GluLookAt_code
    https://registry.khronos.org/OpenGL-Refpages/gl2.1/xhtml/gluLookAt.xml
    """
    #forawrd = center-eye
    forward = (center-eye).normalize()    
    side = forward.cross(up).normalize()# lh,rh, both fine. thats why side..
    up = side.cross(forward).normalize()
    
    sx,sy,sz = side
    ux,uy,uz = up
    fx,fy,fz = forward
    ex,ey,ez = eye
    #px,py,pz = eye.dot(side), eye.dot(up), eye.dot(forward)#simulates M1*M2
    px,py,pz = -eye.dot(side), -eye.dot(up), eye.dot(forward)#not right, side-effected.
    
    mixed = [
    sx,ux,-fx,0,
    sy,uy,-fy,0,
    sz,uz,-fz,0,
    px,py,pz, 1.0
    ]
    return mixed

