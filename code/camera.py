from math import cos,sin,radians, sqrt, atan2

from matrix import Matrix

def normalize(vx,vy,vz):
    norm = sqrt(vx**2 + vy**2 + vz**2)
    if norm <0.0001:
        norm = 100000
    return (vx/norm,vy/norm,vz/norm)


class Camera:
    def __init__(self, fov=60, ratio=1.66, near=0.01, far=1000):
        self.fov = fov
        self.ratio = ratio
        self.near = near
        self.far = far

        self.position = (0,0,1)
        self.front = (0,0,-1)
        self.up = (0,1,0)
        
        self.speed = 0.0

        # self.eye = (0,0,1)
        # self.center = (0,0,0)
        # self.up = (0,1,0)

        self.sensitivity = 1.0
        self.yaw = radians(90)
        self.pitch = 0.0

    def look(self, x,y,z):
        px,py,pz = self.position
        self.front = normalize(x-px,y-py,z-pz)
        fx,fy,fz = self.front
        #tan(th) = fz/fx
        self.yaw = atan2(-fz,fx)
        self.pitch = atan2( fy , sqrt(fx**2+fz**2) )
        #print(self.yaw,self.pitch, self.front)
        #seems, finally works.

    @property
    def eye(self):
        return self.position
    # @eye.setter
    # def eye(self,value):
    #     self.position = value
    #     #need to set yaw,pitch.
    @property
    def center(self):
        px,py,pz = self.position
        fx,fy,fz = self.front
        return px+fx,py+fy,pz+fz
    # @center.setter
    # def center(self,value):
    #     x,y,z = value
    #     px,py,pz = self.position
    #     self.front = (x-px,y-py,z-pz)
    #     #need yaw,pitch..
    
    def get_ProjectionView(self):
        Projection = self.get_Projection()
        View = self.get_View()
        ProjectionView = Projection * View
        return ProjectionView

    def get_Projection(self):
        return Matrix.Perspective( radians(self.fov), self.ratio,self.near,self.far)
    def get_Ortho(self):
        return Matrix.Ortho(self.left, self.right, self.bottom, self.top, self.near, self.far)
    def get_View(self):
        return Matrix.View(self.eye, self.center, self.up)


    def set_dxdy(self, dx,dy):
        "dx,dy range -1~1. y+up."
        yaw = self.yaw
        pitch = self.pitch
        mag = self.sensitivity
        yaw += dx * mag
        pitch += dy * mag
        #dy is positive if cursor to up. imagine joystick.. up is 1.0.
        #touch, not drag but simulate joystick.
        r89 = radians(89)
        if pitch > r89:
            pitch = r89
        elif pitch < -r89:
            pitch = -r89
        #maybe it'sLH.. sin affected.
        vx = cos(yaw) * cos(pitch)
        vz = -sin(yaw) * cos(pitch) #it happened.don't ask. maybe z is depth?
        vy = sin(pitch)  #pitch +, to up.
        
        direction = normalize(vx,vy,vz)
        self.front = direction
        self.yaw = yaw
        self.pitch = pitch

    def set_speed(self,spd):
        self.speed = spd
    def update(self,dt):
        speed = self.speed * dt
        vx,vy,vz = self.front
        px,py,pz = self.position
        self.position = px+vx*speed, py+vy*speed, pz+vz*speed


if __name__ == '__main__':
    cam = Camera()
    print(cam.front)
    cam.set_dxdy(0,0)
    print(cam.front)
    cam.set_dxdy(0.01, 0.00001)
    print(cam.front)


