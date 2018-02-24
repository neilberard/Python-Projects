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
        self._base_name = []
        self.name_list = str_name.split('_')

        # Gather name info from str_name.
        for name in self.name_list:
            # SIDE
            if name in consts.SIDE:
                self._side = name
            # TYPE
            if name in consts.TYPE:
                self._type = name
            # JOINT
            if name in consts.TORSO or \
                name in consts.ARM or \
                name in consts.LEG and \
                    name not in consts.IK:
                self._joint_name = name
            # BASENAME
            if name not in itertools.chain(consts.LEG,
                                           consts.ARM,
                                           consts.TORSO,
                                           consts.SIDE,
                                           consts.TYPE,
                                           consts.IK):
                self._base_name = name

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



def concatenate(str_list):
    string = '_'.join([x for x in str_list if x])
    return string


"""Test Code"""

if __name__ == '__main__':

    name_info = ItemInfo('newthing_Elbow_JNT')

    print concatenate([name_info.base_name, name_info.joint_name])
    print name_info.type




    # string = 'L_Elbow_JNT'
    #
    # info = ItemInfo(string)
    #
    # print concatenate(['', 'Elbow', 'JNT'])
    #
    # print info.type




