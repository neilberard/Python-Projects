from python.libs import consts
reload(consts)


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
            # REGION and JOINT NAME
            if name in consts.ARM:
                self.joint_name = name
                self._region = consts.ALL['Arm']
            elif name in consts.LEG:
                self.joint_name = name
                self._region = consts.ALL['Leg']
            elif name in consts.TORSO:
                self.joint_name = name
                self._region = consts.ALL['Torso']
            elif name in consts.HAND:
                self.joint_name = name
                self._region = consts.ALL['Hand']

            # SIDE
            if name in consts.SIDE:
                self._side = name
            # TYPE
            if name in consts.TYPE:
                self._type.append(name)
            # BASENAME
            if name not in consts.ALL.values() and \
               name not in consts.INDEX:
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


def match_tagged_items(objects, tags):
    """
    Finds objects with matching attributes/values (tags) as tag_dictionary.
    :param objects: Any Maya object.
    :param tags: Type dict. Example {'Region': 'Arm', 'Side': 'R', 'Type': 'IK'}
    :return: list of matching objects.
    """

    object_list = []

    for obj in objects:
        output = obj
        for key in tags.keys():
            if obj.hasAttr(key) and obj.getAttr(key) == tags[key]:
                pass
            else:
                output = None  # Could not find attribute or attribute value did not match.
        if output:
            object_list.append(output)

    return object_list


def add_tags(obj, tags):
    """
    :param obj: Maya object to add string attributes to.
    :param tags: dict{'Region': 'Arm', 'Side': 'R', 'Type': 'IK'}
    """
    for key in tags.keys():
        if not obj.hasAttr(key):
            obj.addAttr(key, type='string', keyable=False)
            obj.setAttr(key, tags[key])


def list_tags(obj):
    obj_attributes = {}

    for attribute in obj.listAttr():
        if attribute.attrName() in consts.TAGS:
            obj_attributes[attribute.attrName()] = attribute.get()

    for tag in consts.TAGS:
        if tag not in obj_attributes.keys():
            obj_attributes[tag] = []

    return obj_attributes


def add_message_attr(obj, attributes):
    """
    :param obj: Maya object to add message multi attributes to. This will be used to connect objects.
    :param attributes: list['_IK', '_FK', _IKCTRL, _FKCTRL]
    """
    for attr in attributes:
        if not obj.hasAttr(attr):
            obj.addAttr(attr, type='message', multi=True)




"""test Code"""

if __name__ == '__main__':
    import pymel.core as pymel

    print list_tags(obj=pymel.PyNode('R_Shoulder_Constraint'))








    # string = 'L_Elbow_JNT'
    #
    # info = ItemInfo(string)
    #
    # print concatenate(['', 'Elbow', 'JNT'])
    #
    # print info.type




