class RotationType:
    RT_ZYX = 0
    RT_XZY = 1
    RT_XYZ = 2
    RT_YXZ = 3
    RT_YZX = 4
    RT_ZXY = 5

    ALL = [RT_ZYX, RT_XZY, RT_XYZ, RT_YXZ, RT_YZX, RT_ZXY]
    # un upright or un updown
    Notupdown = [RT_ZYX,RT_XZY]
 
class Axis:
    WIDTH = 0
    HEIGHT = 1
    LENGTH = 2

    ALL = [WIDTH, HEIGHT, LENGTH]

