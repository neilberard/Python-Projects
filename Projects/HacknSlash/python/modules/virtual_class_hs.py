import pymel.all as pymel
from python.libs import naming_utils
from python.libs import joint_utils
import logging

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


def attach_class(node, net):
    """
    Adds a string attribute to a PyNode set to the virtual class identifier. Example node._class = '_TransformNode'
    :param node: PyNode to add attribute to.
    :param net: Network to associate the PyNode with IE: 'L_Leg_Net'
    :return: PyNode as a virtual class
    """
    log.info([type(node), node])

    if node.hasAttr('_class'):
        node.deleteAttr('_class')

    if node.hasAttr('Network'):
        node.deleteAttr('Network')

    #Ensuring that node is a vanilla pynode
    node = pymel.PyNode(node)

    node.addAttr('Network', dataType='string')
    node.Network.set(net.name())

    if isinstance(node, pymel.nodetypes.Joint):
        node.addAttr('_class', dataType='string')
        node._class.set('_JointNode')
        return pymel.PyNode(node)

    if isinstance(node, pymel.nodetypes.Transform):
        node.addAttr('_class', dataType='string')
        node._class.set('_TransformNode')
        new_node = pymel.PyNode(node)
        assert isinstance(new_node, TransformNode)
        return new_node

    if isinstance(node, pymel.nodetypes.Network):
        node.addAttr('_class', dataType='string')
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
        if self.message.connections():
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

    def add_network_tag(self):
        self.add_tags({'Network': self.network.name()})

    def add_tags(self, tags):
        try:
            naming_utils.add_tags(self, tags)
        except Exception as ex:
            log.warning('Failed to add tags: {}, {}, {}'.format(self, tags, ex))

    def get_root(self):
        return joint_utils.get_root(self)

    @property
    def all_ctrl_nodes(self):
        """Return all control rig nodes, ignore skinning joints"""

        nodes = []

        for obj in pymel.ls():
            if obj.hasAttr('Network') and obj.Network.get() == self.network.name() and obj not in self.jnts:
                nodes.append(obj)
        return nodes


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

        pymel.addAttr(newNode, longName='_class', dataType='string')
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
        newNode.addAttr('_class', dataType='string')
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
        newNode.addAttr('_class', dataType='string')
        newNode._class.set('_LimbNode')
        newNode.addAttr('JOINTS', attributeType='message', multi=True)
        newNode.addAttr('IK_JOINTS', attributeType='message', multi=True)
        newNode.addAttr('FK_JOINTS', attributeType='message', multi=True)
        newNode.addAttr('IK_CTRL', attributeType='message', multi=True)
        newNode.addAttr('FK_CTRL', attributeType='message', multi=True)
        newNode.addAttr('POLE', attributeType='message', multi=True)
        newNode.addAttr('ANNO', attributeType='message', multi=True)
        newNode.addAttr('SWITCH', attributeType='message', multi=True)
        newNode.addAttr('ORIENTCONSTRAINT', attributeType='message', multi=True)
        newNode.addAttr('POINTCONSTRAINT', attributeType='message', multi=True)
        newNode.addAttr('IK_HANDLE', attributeType='message', multi=True)
        newNode.addAttr('IK_SNAP_LOC', attributeType='message', multi=True)


    #Overwritting BaseClass Method
    @property
    def network(self):
        return self

    @property
    def ik_jnts(self):
        return self.IK_JOINTS.connections()

    @property
    def fk_jnts(self):
        return self.FK_JOINTS.connections()

    @property
    def ik_handles(self):
        return self.IK_HANDLE.connections()

    @property
    def fk_ctrls(self):
        return self.FK_CTRL.connections()

    @property
    def ik_ctrls(self):
        return self.IK_CTRL.connections()

    @property
    def jnts(self):
        return self.JOINTS.connections()

    @property
    def ik_snap_loc(self):
        return self.IK_SNAP_LOC.connections()

    @property
    def all_nodes(self):
        nodes = []

        for obj in pymel.ls():
            if obj.hasAttr('Network') and obj.Network.get() == self.name():
                nodes.append(obj)
        return nodes

    @property
    def all_ctrl_nodes(self):
        """Return all control rig nodes, ignore skinning joints"""

        nodes = []

        for obj in pymel.ls():
            if obj.hasAttr('Network') and obj.Network.get() == self.name() and obj not in self.jnts:
                nodes.append(obj)
        return nodes



# Classes need to be registered to exist in the scene.
pymel.factories.registerVirtualClass(JointNode, nameRequired=False)
pymel.factories.registerVirtualClass(LimbNode, nameRequired=False)
pymel.factories.registerVirtualClass(TransformNode, nameRequired=False)
