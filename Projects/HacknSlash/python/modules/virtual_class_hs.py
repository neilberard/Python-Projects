import pymel.all as pymel
from python.libs import naming_utils
import logging

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


def attach_class(node):

    if node.hasAttr('_class'):
        node.deleteAttr('_class')

    if isinstance(node, pymel.nodetypes.Joint):
        node.addAttr('_class', dt='string')
        node._class.set('_JointNode')
        return pymel.PyNode(node)

    if isinstance(node, pymel.nodetypes.Transform):
        node.addAttr('_class', dt='string')
        node._class.set('_TransformNode')
        return pymel.PyNode(node)

    if isinstance(node, pymel.nodetypes.Network):
        node.addAttr('_class', dt='string')
        node._class.set('_LimbNode')
        return pymel.PyNode(node)



    log.warning('Could not find class for: '.format(node))


class BaseNode():
    """
    Subclass must also inherit leaf class with pymel.nodetype.dagnode as it's hierarchy. IE: pymel.nodetypes.Joint
    This class contains some basic properties that are used for accessing other nodes
    """

    @property
    def network(self):
        return self.message.connections()[0]

    @property
    def jnts(self):
        return self.network.JOINTS.connections()

    @property
    def fk_jnts(self):
        return self.network.FK_JOINTS.connections()

    @property
    def ik_jnts(self):
        return self.network.IK_JOINTS.connections()

    @property
    def name_info(self):
        return naming_utils.ItemInfo(self)

    @property
    def get_class(self):
        return self._class.get()

    @property
    def side(self):
        return self.Side.get()

    @property
    def region(self):
        return self.Region.get()


    def add_tags(self, tags):
        try:
            naming_utils.add_tags(self, tags)
        except Exception as ex:
            log.warning('Failed to add tags: {}, {}, {}'.format(self, tags, ex))


class JointNode(pymel.nodetypes.Joint, BaseNode):
    """ this is an example of how to create your own subdivisions of existing nodes. """

    NODE_TYPE = 'JointNode'

    @classmethod
    def list(cls, *args, **kwargs):
        """ Returns all instances the node in the scene """

        kwargs['type'] = cls.__melnode__
        return [node for node in pymel.ls(*args, **kwargs) if isinstance(node, cls)]

    @classmethod
    def _isVirtual(cls, obj, name):
        """PyMEL code should not be used inside the callback, only API and maya.cmds. """
        fn = pymel.api.MFnDependencyNode(obj)
        try:
            if fn.hasAttribute('_class'):
                plug = fn.findPlug('_class')
                if plug.asString() == '_JointNode':
                    return True
                return False
        except:
            pass
        return False

    @classmethod
    def _preCreateVirtual(cls, **kwargs):
        """This is called before creation. python allowed."""
        return kwargs

    @classmethod
    def _postCreateVirtual(cls, newNode):
        print newNode
        """ This is called before creation, pymel/cmds allowed."""

        pymel.addAttr(newNode, longName='_class', dt='string')
        newNode._class.set('_JointNode')


class TransformNode(pymel.nodetypes.Transform, BaseNode):
    """ this is an example of how to create your own subdivisions of existing nodes. """

    @classmethod
    def list(cls, *args, **kwargs):
        """ Returns all instances the node in the scene """

        kwargs['type'] = cls.__melnode__
        return [node for node in pymel.ls(*args, **kwargs) if isinstance(node, cls)]

    @classmethod
    def _isVirtual(cls, obj, name):
        """PyMEL code should not be used inside the callback, only API and maya.cmds. """
        fn = pymel.api.MFnDependencyNode(obj)
        try:
            if fn.hasAttribute('_class'):
                plug = fn.findPlug('_class')
                if plug.asString() == '_TransformNode':
                    return True
                return False
        except:
            pass
        return False

    @classmethod
    def _preCreateVirtual(cls, **kwargs):
        """This is called before creation. python allowed."""
        return kwargs

    @classmethod
    def _postCreateVirtual(cls, newNode):
        print newNode
        """ This is called before creation, pymel/cmds allowed."""
        newNode.addAttr('_class', dt='string')
        newNode._class.set('_TransformNode')


class LimbNode(pymel.nodetypes.Network, BaseNode):
    """ this is an example of how to create your own subdivisions of existing nodes. """

    @classmethod
    def list(cls, *args, **kwargs):
        """ Returns all instances the node in the scene """

        kwargs['type'] = cls.__melnode__
        return [node for node in pymel.ls(*args, **kwargs) if isinstance(node, cls)]

    @classmethod
    def _isVirtual(cls, obj, name):
        """PyMEL code should not be used inside the callback, only API and maya.cmds. """
        fn = pymel.api.MFnDependencyNode(obj)
        try:
            if fn.hasAttribute('_class'):
                plug = fn.findPlug('_class')
                if plug.asString() == '_LimbNode':
                    return True
                return False
        except:
            pass
        return False

    @classmethod
    def _preCreateVirtual(cls, **kwargs):
        """This is called before creation. python allowed."""
        return kwargs

    @classmethod
    def _postCreateVirtual(cls, newNode):
        """ This is called before creation, pymel/cmds allowed."""
        newNode.addAttr('_class', dt='string')
        newNode._class.set('_LimbNode')
        newNode.addAttr('JOINTS', at='message', multi=True)
        newNode.addAttr('IK_JOINTS', at='message', multi=True)
        newNode.addAttr('FK_JOINTS', at='message', multi=True)
        newNode.addAttr('IK_CTRL', at='message', multi=True)
        newNode.addAttr('FK_CTRL', at='message', multi=True)
        newNode.addAttr('POLE', at='message', multi=True)
        newNode.addAttr('ANNO', at='message', multi=True)
        newNode.addAttr('SWITCH', at='message', multi=True)
        newNode.addAttr('ORIENTCONSTRAINT', at='message', multi=True)
        newNode.addAttr('POINTCONSTRAINT', at='message', multi=True)
        newNode.addAttr('IK_HANDLE', at='message', multi=True)


    #Overwritting BaseClass Method
    @property
    def network(self):
        return self

    @property
    def ik_handles(self):
        return self.IK_HANDLE.get()


# Classes need to be registered to exist in the scene.
pymel.factories.registerVirtualClass(JointNode, nameRequired=False)
pymel.factories.registerVirtualClass(LimbNode, nameRequired=False)
pymel.factories.registerVirtualClass(TransformNode, nameRequired=False)
