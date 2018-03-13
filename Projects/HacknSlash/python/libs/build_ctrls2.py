import pymel.core as pymel
from python.libs import shapes
import logging

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


class CreateCtrl():
    """
    Create a controller that can be manipulated by class properties.
    """
    def __init__(self):

        self._name = 'Placeholder'
        self._jnt = None
        self._children = None
        self._parent = None
        self._type = None
        self._object = None
        self._size = 1
        self._matrix = None
        self._axis = 'x'

        try:
            self._matrix = self._jnt.getMatrix()
        except:
            pass

    def make_object(self):
        if not self._type:
            log.warning('no type specified')

        self._object = shapes.make_shape(self._type, self._name, self._axis)
        if not self._object:
            log.warning('No object was returned')
            return None

        if self._matrix:
            self._object.setMatrix(self._matrix, worldSpace=True)

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