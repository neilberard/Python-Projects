from Projects.HacknSlash.python.project.libs import consts


class ItemInfo(object):
    def __init__(self, str_name):
        """
        Object names should only contain no more than one of each property.
        :param str_name: Name of the object to gather info.
        """
        self.name_list = str_name.split('_')
        self._base_name = []
        self._side = []
        self._type = []

    @property
    def side(self):
        for name in self.name_list:
            if name in consts.SIDE:
                self._side = name
        return self._side

    @side.setter
    def side(self, str):
        self._side = str

    @property
    def type(self):
        for name in self.name_list:
            if name in consts.TYPE:
                self._type = name
        return self._type

    @type.setter
    def type(self, str):
        self._type = string

    @property
    def base_name(self):
        for name in self.name_list:
            if name in consts.TORSO or \
                 name in consts.ARM or \
                 name in consts.LEG:
                    self._base_name = name
        return self._base_name

    @base_name.setter
    def base_name(self, str):
        self._base_name = str


def concatenate(str_list):
    string = '_'.join(str_list)
    return string


"""Test Code"""

if __name__ == '__main__':

    string = 'L_Elbow_JNT'

    info = ItemInfo(string)

    print concatenate(['L', 'Elbow','JNT'])

    print info.type




