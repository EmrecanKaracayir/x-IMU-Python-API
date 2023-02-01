from dataclasses import dataclass
import math

@dataclass
class EulerAngles:
    roll: float
    pitch: float
    yaw: float

class Queternion():

    def __init__(self, w = 1.0, x = 0.0, y = 0.0, z = 0.0):
        self.w = w
        self.x = x
        self.y = y
        self.z = z
    
    def getConjugate(self):
        return Queternion(self.w, - self.x, - self.y, - self.z)
    
    def getEulerAngles(self):
        roll = Queternion.radiansToDegrees(math.atan2(
            2.0 * (self.y * self.z - self.w * self.x), 
            2.0 * self.w * self.w - 1.0 + 2.0 * self.z * self.z
            ))
        pitch = Queternion.radiansToDegrees(-math.atan(
            (2.0 * (self.x * self.z - self.w * self.y)) / 
            math.sqrt(1.0 - math.pow((2.0 * self.x * self.z + 2.0 * self.w * self.y), 2.0))
            ))
        yaw = Queternion.radiansToDegrees(math.atan2(
            2.0 * (self.x * self.y - self.w * self.z), 
            2.0 * self.w * self.w - 1.0 + 2.0 * self.x * self.x
            ))
        return EulerAngles(roll, pitch, yaw)
    
    @staticmethod
    def radiansToDegrees(radians: float):
        return 57.2957795130823 * radians