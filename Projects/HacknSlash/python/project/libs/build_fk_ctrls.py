import pymel.core as pymel
from Projects.HacknSlash.python.project.libs import naming_utils
from Projects.HacknSlash.python.project.libs import shapes
reload(shapes)
import logging

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


class CreateCtrl(object):
    """
    Create a controller that can be manipulated by class properties.
    """
    def __init__(self):

        self._name = 'Placeholder'
        self._type = None
        self._object = None
        self._size = 1
        self._matrix = None

    def make_object(self):
        try:
            pymel.delete(self._object)
            self._object = None
        except:
            pass

        self._object = shapes.make_shape(self._type, self._name)
        if not self._object:
            log.warning('no type specified')
            return None

        if self._matrix:
            self._object.setMatrix(self._matrix, worldSpace=True)

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, value):
        self._type = value

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, value):
        self._size = value
        try:
            self._object.setScale([value, value, value])
        except:
            pass

    @property
    def matrix(self):
        return self._matrix

    @matrix.setter
    def matrix(self, matrix):
        self._matrix = matrix

    def delete(self):
        try:
            pymel.delete(self._object)
            self._object = None
        except:
            pass


class ControlBuilder(object):
    def __init__(self, joints=None):

        self._joints = joints
        self._ctrls = {}
        self._joint_info = {}

        # Get info
        self.get_ctrl_dict()
        self.get_joint_info_dict()
        self.set_ctrl_matrix()

    @property
    def joints(self):
        return self.joints()

    @joints.setter
    def joints(self, joints):
        self._joints = joints

    def get_ctrl_dict(self):

        # If nothing is selected, will return a single instance.
        if not self._joints:
            self._ctrls['base'] = CreateCtrl()
        else:
            for jnt in self._joints:
                self._ctrls[jnt.name()] = CreateCtrl()

    def get_joint_info_dict(self):
        """
        :return: skeleton_info{jnt_info:{'jnt_matrix': list, 'jnt_children': list,'jnt_parent': parent}}
        """
        self._joint_info = {}

        for jnt in self._joints:
            jnt_info = {'jnt_matrix': jnt.getMatrix(worldSpace=True),
                        'jnt_children': jnt.getChildren(),
                        'jnt_parent': jnt.getParent()}
            self._joint_info[jnt.name()] = jnt_info

    def create_ctrls(self):
        for ctrl_instance in self._ctrls.values():
            ctrl_instance.make_object()

    def set_ctrl_size(self, size):
        for ctrl_instance in self._ctrls.values():
            ctrl_instance.size = size

    def set_ctrl_type(self, ctrl_type):
        for ctrl_instance in self._ctrls:
            self._ctrls[ctrl_instance].type = ctrl_type

    def set_ctrl_matrix(self):
        for ctrl_instance in self._ctrls:
            self._ctrls[ctrl_instance].matrix = self._joint_info[ctrl_instance]['jnt_matrix']


def build_fk_ctrls(joints, ctrl_type='circle', ctrl_name='Fk', ctrl_size=1):
    """

    :param joints:
    :param ctrl_type:
    :param ctrl_name:
    :param ctrl_size:
    :return:
    """
    fk_ctrls = []
    hierarchy = {}

    for jnt in joints:
        ctrl_name = jnt.name() + '_FK'  # todo: add a naming function.
        # Getting joint info.
        jnt_matrix = jnt.getMatrix(worldSpace=True)
        jnt_children = jnt.getChildren()
        jnt_parent = jnt.getParent()

        # Making controller.
        ctrl = create_ctrl(ctrl_type, ctrl_size, ctrl_name=ctrl_name)
        ctrl.setMatrix(jnt_matrix, worldSpace=True)
        pymel.parentConstraint([ctrl, jnt])
        fk_ctrls.append(ctrl)

        # Rebuild hierarchy

        if jnt_parent:
            parent_ctrl_name = ctrl_name.replace(jnt.name(), jnt_parent.name())  # Trying to find name of parent ctrl
            try:
                parent_ctrl = pymel.PyNode(parent_ctrl_name)
                ctrl.setParent(parent_ctrl)
            except pymel.MayaNodeError:
                pass

        if jnt_children:
            for jnt_child in jnt_children:
                child_ctrl_name = ctrl_name.replace(jnt.name(), jnt_child.name())  # Trying to find name of child ctrl
                try:
                    child_ctrl = pymel.PyNode(child_ctrl_name)
                    child_ctrl.setParent(ctrl)
                except pymel.MayaNodeError:
                    pass

        return fk_ctrls



"""TEST CODE"""

if __name__ == '__main__':
    print 'test'

    ctrl_builder = ControlBuilder(pymel.selected())
    ctrl_builder.set_ctrl_type('Circle')

    ctrl_builder.create_ctrls()
    ctrl_builder.set_ctrl_size(5)


    # jnt_dict = get_joint_hierarchy(joints=pymel.selected())
    # ctrls = build_ctrls(joints=pymel.selected())
    #
    # for obj in ctrls:
    #     print jnt_dict[obj]['jnt_matrix']
    #
    #     ctrls[obj].type = 'Diamond'
    #     ctrls[obj].matrix = jnt_dict[obj]['jnt_matrix']
    #     ctrls[obj].make_object()

        # obj.type = 'Circle'
        # obj.make_object()










