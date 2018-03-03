from Projects.HacknSlash.python.project.libs import consts
reload(consts)
import itertools


class ItemInfo(object):
    def __init__(self, str_name):
        """
        Object names should only contain no more than one of each property.
        :param str_name: Name of the object to gather info.
        """
        self._joint_name = []
        self._side = []
        self._type = []
        self._region = []  # Arm, Leg, Torso
        self._base_name = []  # Any name that is not in consts.
        self.name_list = str_name.split('_')
        self._index = []

        # Gather name info from str_name.
        for name in self.name_list:
            # REGION
            if name in consts.ARM:
                self._region = consts.ALL['Arm']
            elif name in consts.LEG:
                self._region = consts.ALL['Leg']
            elif name in consts.TORSO:
                self._region = consts.ALL['Torso']
            elif name in consts.HAND:
                self._region = consts.ALL['Hand']

            # SIDE
            if name in consts.SIDE:
                self._side = name
            # TYPE
            if name in consts.TYPE:
                self._type = name
            # JOINT
            if self._region and \
               name not in consts.IK:
                self._joint_name = name
            # BASENAME
            if name not in consts.ALL.values() and name not in consts.INDEX:
                self._base_name = name

            # INDEX
            if name in consts.INDEX:  # This could be single letters up to 'K' or numbers.
                self._index = name
            try:  # If name is a number, set index to name.
                self._index = int(name)
            except:
                pass

    @property
    def region(self):
        return self._region

    @region.setter
    def region(self, str):
        self._region = str

    @property
    def side(self):
        return self._side

    @side.setter
    def side(self, str):
        self._side = str

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, str):
        self._type = str

    @property
    def joint_name(self):
        return self._joint_name

    @joint_name.setter
    def joint_name(self, str):
        self._joint_name = str

    @property
    def base_name(self):
        return self._base_name

    @base_name.setter
    def base_name(self, str):
        self._base_name = str

    @property
    def index(self):
        return self._index

    @index.setter
    def index(self, str):
        self._index = str




def concatenate(str_list):
    string = '_'.join([x for x in str_list if x])
    return string


"""Test Code"""

if __name__ == '__main__':
    import pymel.core as pymel

    info = ItemInfo(pymel.selected()[0])
    print info.region







    # string = 'L_Elbow_JNT'
    #
    # info = ItemInfo(string)
    #
    # print concatenate(['', 'Elbow', 'JNT'])
    #
    # print info.type




