class Vec3(object):
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
        :param other: Vec3
        :return: dot product
        """
        return (self.x * other.x) + (self.y * other.y) + (self.z * other.z)

    def __xor__(self, other):
        """

        :param other:
        :return: cross product
        """
        a = (self.y * other.z) - (self.z * other.y)
        b = (self.z * other.x) - (self.x * other.z)
        c = (self.x * other.y) - (self.y * other.x)

        return Vec3(a,b,c)

    def normal(self):
        return None

        pass

    def __str__(self):
        return "{}, {}, {}".format(self.x, self.y, self.z)

def ray_intersect_triangle():

    a = Vec3(1.0, 0.0, 0.0)
    b = Vec3(0.5, 0.0, 0.0)
    c = a ^ b

    print(c)





    pass

if __name__ == '__main__':
    ray_intersect_triangle()
