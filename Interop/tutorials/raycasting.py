import math

EPSILON = 0.0000001  # Error value

class Vec3:
    def __init__(self, *args):
        if args:
            self.x = args[0]
            self.y = args[1]
            self.z = args[2]
        else:
            self.x = 0.0
            self.y = 0.0
            self.z = 0.0

    def __add__(self, other):
        return Vec3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __mul__(self, other):
        """
        Dot product.
        :param other: Vec3
        :return: dot product
        """
        if isinstance(other, Vec3):
            return (self.x * other.x) + (self.y * other.y) + (self.z * other.z)
        else:
            return Vec3(self.x * other, self.y * other, self.z * other)


    def __sub__(self, other):
        return Vec3(self.x - other.x, self.y - other.y, self.z - other.z)


    def __xor__(self, other):
        """
        Calculate Cross Product between self and other.
        cross = a ^ b
        :type other: Ve3
        :return: cross product
        """
        a = (self.y * other.z) - (self.z * other.y)
        b = (self.z * other.x) - (self.x * other.z)
        c = (self.x * other.y) - (self.y * other.x)

        return Vec3(a,b,c)

    def normal(self):
        """
        :return: New normalized Vec3
        """
        if not self.length():
            raise Exception("Cannot normalize a vector of zero length")

        offset = 1.0 / self.length()
        return Vec3(self.x * offset, self.y * offset, self.z * offset)

    def normalize(self):
        """
        Normalize self.
        """
        if not self.length():
            raise Exception("Cannot normalize a vector of zero length")

        offset = 1.0 / self.length()

        self.x = self.x * offset
        self.y = self.y * offset
        self.z = self.z * offset

    def length(self):
        value = (self.x * self.x) + (self.y * self.y) + (self.z * self.z)
        return math.sqrt(value)

    def __str__(self):
        return "{}, {}, {}".format(self.x, self.y, self.z)



def ray_intersect_triangle(origin, ray, triangle):
    """
    Moller-Trumbore intersection algorithm
    :param origin: Vec3
    :param ray: Vec3
    :param triangle: List of 3 Vec3
    :return: Hit
    """

    vertex0 = triangle[0]
    vertex1 = triangle[1]
    vertex2 = triangle[2]

    edge1 = vertex1 - vertex0
    edge2 = vertex2 - vertex0
    h = ray ^ edge2
    a = edge1 * h

    if EPSILON * -1 < a < EPSILON:
        return # This ray is parallel to this triangle

    f = 1.0 / a
    s = origin - vertex0
    u = f * (s * h)

    if u < 0.0 or u > 1.0:
        return

    q = s ^ edge1
    v = f * (ray * q)

    if v < 0.0 or u + v > 1.0:
        return

    # It's in the triangle, let's find that hit!
    t = f * (edge2 * q)

    if t > EPSILON:
        return origin + ray * t


    # a = Vec3(1.0, 0.0, 0.0)
    # a.normalize()
    # b = Vec3(1.0, 0.0, 0.0)
    # print(a ^ b)
    #
    #
    # print(a.length())
    # print(b.length())
    #





    pass

if __name__ == '__main__':

    triangle = [Vec3(0.0, 0.0, 0.1), Vec3(0.5, 0.5, 0.0), Vec3(1.0, 0.0, 0.0)]
    ray = Vec3(0.1, 0.1, -1.0)
    origin = Vec3(0.5, 0.25, 0.5)

    print(ray_intersect_triangle(origin, ray, triangle))
