import pymel.core as pymel
from Projects.HacknSlash.python.project.libs import naming_utils
from Projects.HacknSlash.python.project.libs import shapes
reload(shapes)
import logging

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


def create_ctrl(ctrl_type='circle', ctrl_size=3, ctrl_name='FK'):

    if ctrl_type == 'circle':
        return pymel.circle(radius=ctrl_size, normal=(1, 0, 0), name=ctrl_name)[0]


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


def set_ctrl_radius(ctrls, size):
    pass


class CreateCtrl(object):
    def __init__(self):

        self._name = 'Placeholder'
        self._type = None
        self._object = None
        self._size = 1

    def make_object(self):
        try:
            pymel.delete(self._object)
            self._object = None
        except:
            pass

        self._object = shapes.make_shape(self._type, self._name)

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







