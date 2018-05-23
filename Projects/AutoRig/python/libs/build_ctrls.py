import logging
import pymel.core as pymel
import maya.OpenMaya as om
from python.libs import consts, naming_utils
from python.libs import shapes
from python.libs import joint_utils
from python.libs import lib_network
from python.libs import virtual_classes
reload(shapes)
reload(naming_utils)
reload(consts)
reload(joint_utils)
reload(lib_network)

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


def create_ctrl(jnt=None,
                network=None,
                attr=None,
                tags=None,
                axis='z',
                shape='Circle',
                size=1.0,
                name=None,
                offset=False,
                mirrored=False):

    if not name and jnt:
        info = naming_utils.ItemInfo(jnt)
        name = naming_utils.concatenate([info.side, info.base_name, info.joint_name, 'CTRL'])

    elif not name:
        name = 'Ctrl'

    ctrl = virtual_classes.CtrlNode()
    pymel.rename(ctrl, name)
    ctrl.set_shape(shape)
    ctrl.set_axis(axis)

    if mirrored:
        ctrl.setScale((-1, -1, 1))
    ctrl.freeze_transform()

    if tags:
        naming_utils.add_tags(ctrl, tags)

    if network:
        naming_utils.add_tags(ctrl, {'Network': network})

    naming_utils.add_tags(ctrl, {'Type': 'CTRL'})

    if jnt:
        ctrl.rotateOrder.set(jnt.rotateOrder.get())
        ctrl.setMatrix(jnt.getMatrix(worldSpace=True), worldSpace=True)

    ctrl.setScale((size, size, size))
    pymel.makeIdentity(apply=True, scale=True)

    if offset:
        joint_utils.create_offset_groups(ctrl, name=naming_utils.concatenate([ctrl.name(), 'Offset']))

    if attr:
        idx = attr.getNumElements()
        ctrl.message.connect(attr[idx])

    return ctrl


class CreateCtrl(object):
    """
    Create a controller that can be manipulated by class properties.
    """
    def __init__(self,
                 jnt=None,
                 network=None,
                 tags=None,
                 axis='z',
                 shape='Circle',
                 size=1.0,
                 name='ctrl'):
        """
        :param jnt:
        :param network:
        :param tags:
        :param axis: 'X', 'Y', 'Z', Use Z to align with limb, Y to align to world
        """

        # Ctrl Object
        self.object = None
        self.network = network
        self.tags = tags
        self.axis = axis
        self.shape = shape
        self.size = size
        self.jnt = jnt
        self.matrix = [1.0, 0.0, 0.0, 0.0,
                       0.0, 1.0, 0.0, 0.0,
                       0.0, 0.0, 1.0, 0.0,
                       0.0, 0.0, 0.0, 1.0]
        self.name = name

        if self.jnt:
            self.ctrl_type = None
            self.children = jnt.getChildren()
            self.parent = jnt.getParent()
            self.matrix = jnt.getMatrix(worldSpace=True)
            self.make_object()

        else:
            self.make_object()

        if self.object and self.network:
            naming_utils.add_tags(self.object, {'Network': self.network.name()})


    @property
    def message(self):
        return self.object.message

    def make_object(self):
        if not self.shape:
            log.warning('no type specified')
        # Object

        self.object = shapes.make_shape(self.shape, self.name, self.axis)

        if not self.object:
            log.warning('Make Object: No object was returned')
            return None
        # Matrix
        if self.matrix:
            self.object.setMatrix(self.matrix, worldSpace=True)
        # Tags
        if self.tags:
            naming_utils.add_tags(self.object, self.tags)

        self.object.scale.set(self.size, self.size, self.size)
        self.freeze_transforms()

        return self.object

    def get_ctrl_distance(self):
        """Retun average distance"""

        jnt_vector = om.MVector(self.jnt.getTranslation(space='world'))
        distance_tally = []

        if self.parent:
            parent_vector = om.MVector(self.parent.getTranslation(space='world')) - jnt_vector
            distance_tally.append(parent_vector.length())

        if self.children:
            child_vector = om.MVector(self.children[0].getTranslation(space='world')) - jnt_vector
            distance_tally.append(child_vector.length())

        if len(distance_tally) > 0:
            return sum(distance_tally)/len(distance_tally)

        else:
            return None

    def freeze_transforms(self):
        pymel.makeIdentity(self.object, apply=True, scale=True)
        pymel.delete(self.object, constructionHistory=True)

    def delete(self):
        try:
            pymel.delete(self.object)
            self.object = None
        except:
            pass


class ControlBuilder(object):
    """
    This class is intended to iterate on a dict of CreateCtrl class instances and values.
    """

    def __init__(self, joints=None, network=None, ctrl_type=None):
        self.joints = joints
        self.network = network
        self.parent_constraint = True
        self.ctrls = []
        self.offsets = []
        self.set_ctrl_list()

    def set_ctrl_list(self):
        self.ctrls = []

        # If nothing is selected, will return a single instance.
        if not self.joints:
            self.ctrls.append(virtual_classes.CtrlNode())
        else:
            for jnt in self.joints:
                ctrl = virtual_classes.CtrlNode()
                grp = ctrl.create_offset()
                grp.setMatrix(jnt.getMatrix(worldSpace=True), worldSpace=True)
                self.ctrls.append(ctrl)
                self.offsets.append(grp)

    def set_ctrl_types(self, shape):
        for ctrl in self.ctrls:
            ctrl.set_shape(shape)

    def set_ctrl_sizes(self, size=10):
        for ctrl in self.ctrls:
            ctrl.setScale((size, size, size))

    def set_ctrl_axis(self, axis):
        for ctrl in self.ctrls:
            ctrl.set_axis(axis)

    def set_ctrl_matrices(self):
        for idx, jnt in enumerate(self.joints):
            pass

    def set_ctrl_names(self):
        for ctrl_instance in self.ctrls:
            info = naming_utils.ItemInfo(ctrl_instance)  # Grabbing the object base and or jnt name.
            log.info(info.base_name)
            name = naming_utils.concatenate([info.side,
                                             info.base_name,
                                             info.joint_name,
                                             info.index,
                                             consts.ALL['CTRL']])

    def delete_ctrls(self):
        if not self.ctrls:
            return

        pymel.delete(self.ctrls)
        pymel.delete(self.offsets)

        self.ctrls = []  # resetting the dict


"""TEST CODE"""

if __name__ == '__main__':

    ctrls = CreateCtrl(jnt=pymel.selected()[0])
    print ctrls.get_ctrl_distance()









