import pymel.core as pymel
from python.libs import shapes
from python.libs import lib_network
import logging

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


class CreateCtrl(object):
    """
    Create a controller that can be manipulated by class properties.
    """
    def __init__(self, jnt=None, network=None):

        # Ctrl Object
        self._object = None
        self._network = network

        if jnt:
            self._name = 'Placeholder'
            self._ctrl_type = None
            self._jnt = jnt
            self._children = jnt.getChildren()
            self._parent = jnt.getParent()
            self._matrix = jnt.getMatrix(worldSpace=True)
            self._shape = None
            self._size = 1
            self._axis = 'z'

    def make_object(self):
        if not self._shape:
            log.warning('no type specified')

        self._object = shapes.make_shape(self._shape, self._name, self._axis)
        if not self._object:
            log.warning('No object was returned')
            return None

        if self._matrix:
            self._object.setMatrix(self._matrix, worldSpace=True)

    def get_network(self):
        pass



    @property
    def object(self):
        return self._object

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def type(self):
        return self._shape

    @type.setter
    def type(self, value):
        self._shape = value

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

    @property
    def axis(self):
        return self._axis

    @axis.setter
    def axis(self, axis):
        self._axis = axis

    def freeze_transforms(self):
        pymel.makeIdentity(self._object, apply=True, scale=True)
        pymel.delete(self._object, constructionHistory=True)

    def delete(self):
        try:
            pymel.delete(self._object)
            self._object = None
        except:
            pass


def build_ctrls(joints):
    return [CreateCtrl(jnt()) for jnt in joints]


"""USAGE EXAMPLE"""
if __name__ == '__main__':
    net = lib_network.create_network_node(name='temp',
                                          tags={'Type': 'IKFK', 'Region': 'Arm', 'Side': 'Left'},
                                          attributes=['IK', 'FK', 'IK_CTRL', 'FK_CTRL', 'OrientConstraint', 'PointConstraint'])
    ctrls = [CreateCtrl(jnt=jnt, network=net) for jnt in pymel.selected()]

    for ctrl in ctrls:
        ctrl.type = "Circle"
        ctrl.make_object()






