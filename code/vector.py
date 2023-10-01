from vecops import *

class vec:
    __slots__ = ('x','y','z')
    EPS = 1e-6#0.000001 EPSILON
    DEFAULT_AXIS = (0,1,0)
    def __init__(self, x,y,z):
        self.x = x
        self.y = y
        self.z = z
    def set(self,x,y,z):
        self.x = x
        self.y = y
        self.z = z
    def copy(self):
        return self.__class__(self.x,self.y,self.z)

    def __str__(self):
        return f"{self.__class__.__name__} {self.x:.6f} {self.y:.6f} {self.z:.6f}"
    def __getitem__(self,idx):
        if idx == 0:
            return self.x
        elif idx == 1:
            return self.y
        elif idx == 2:
            return self.z
        else:
            raise IndexError('Vec idx 2 max')
    
    #=== operands
    def __add__(self, other):
        return self.__class__(self.x+other.x,self.y+other.y,self.z+other.z)
    def __sub__(self, other):
        return self.__class__(self.x-other.x,self.y-other.y,self.z-other.z)
    def __iadd__(self, other):
        self.set(self.x+other.x, self.y+other.y, self.z+other.z)
        return self
    def __isub__(self, value):
        self.set(self.x-other.x, self.y-other.y, self.z-other.z)    
        return self
    
    def __mul__(self, value):
        return self.__class__(self.x*value, self.y*value, self.z*value)
    def __truediv__(self, value):
        return self.__class__(self.x/value, self.y/value, self.z/value)
    def __floordiv__(self, value):
        return self.__class__(self.x//value, self.y//value, self.z//value)
    def __imul__(self, value):
        self.set(self.x*value, self.y*value, self.z*value)
        return self
    def __itruediv__(self, value):
        self.set(self.x/value, self.y/value, self.z/value)
        return self
    def __ifloordiv__(self, value):
        self.set(self.x//value, self.y//value, self.z//value)
        return self
    #=================    
    
    #=== additional
    def __neg__(self):
        return self * -1
    def equal(self, other):
        "sef Vec.EPS if needed. 1e-6 0.000_001"
        return (self-other).mag < self.EPS
    def __eq__(self, other):
        return self.equal(other)
    def __ne__(self, other):
        return not self.equal(other)

    def __len__(self):
        #print('getting len to *vec')
        return self.mag
    def __bool__(self):#simple fast 0 checker.
        return self.mag > EPS

    #=== vector property
    #NOTE: norm = mag = len
    #normalized = hat
    def normalize(self):
        try:
            return self / self.mag
        except ZeroDivisionError:
            return 0
    @property
    def hat(self):
        return self.normalized
    @property
    def norm(self):
        return self.mag
        
    @property
    def mag2(self):
        "before sqrt-ed"
        return self.x**2+self.y**2+self.z**2
    @property
    def mag(self):
        "magnitude =norm =length"
        return sqrt(self.x**2+self.y**2+self.z**2)

    #=== vector operations
    def dot(self,other):
        "sum( x1x2, y1y2, z1z2 )"
        return dot(self.x,self.y,self.z,  other.x,other.y,other.z)
    def cross(self,other):
        "RH NON-normalized"
        cx,cy,cz = cross(self.x,self.y,self.z,  other.x,other.y,other.z)
        return self.__class__(cx,cy,cz)
    
    #=== vector calculations
    def angle(self, other):
        "angle between vecs[0-pi]. cos() = a.b/|a||b|"
        #return _angle(self.x,self.y,self.z, other.x,other.y,other.z)
        return angle(self.x,self.y,self.z, other.x,other.y,other.z)
        
    def lookat(self,other):
        axis = self.cross(other)
        angle = self.angle(other)
        self.rotate(angle, axis)


# def rotate(self, rad, axis=None):
#     "pos vector shall rotated"
#     #https://gaussian37.github.io/vision-concept-axis_angle_rotation/
#     #https://en.wikipedia.org/wiki/Category:Rotation_in_three_dimensions
#     #https://en.wikipedia.org/wiki/Quaternions_and_spatial_rotation
#     #https://danceswithcode.net/engineeringnotes/quaternions/quaternions.html
#     if axis is None:
#         x,y,z = self.DEFAULT_AXIS
#     else:
#         x,y,z = axis.x,axis.y,axis.z

#     #easy and safe..
#     #mag = _mag(x,y,z)
#     #x,y,z = x/mag, y/mag, z/mag
#     x,y,z = _normalize(x,y,z)
#     #get quat
#     qw,qx,qy,qz = _angle_axis_to_quat(rad, x,y,z)
#     #get xyzdir
#     rx,ry,rz = _quat_rotate_xyz(qw, qx,qy,qz,  self.x,self.y,self.z)
#     self.x = rx
#     self.y = ry
#     self.z = rz
