import pymel.all as pymel
from python.libs import naming_utils
from python.libs import joint_utils
from python.libs import shapes
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
    Subclass must also inherit leaf class with pymel.nodetype.dagnode as it's hierarchy. IE: 'pymel.nodetypes.Joint'
    This class contains some basic properties that are used for accessing other nodes
    """

    @property
    def network(self):
        if self.message.connections():
            return self.message.connections()[0]

    @property
    def main(self):
        return self.network.message.connections()[0]

    @property
    def mainAttr(self):
        return self.network.message.connections(plugs=True)[0]

    @property
    def jnts(self):
        if self.hasAttr('JOINTS'):
            return self.network.JOINTS.connections()
        else:
            return []

    @property
    def jntsAttr(self):
        return self.network.JOINTS

    @property
    def fk_jnts(self):
        return self.network.FK_JOINTS.connections()

    @property
    def fkJntsAttr(self):
        return self.network.FK_JOINTS

    @property
    def ik_jnts(self):
        return self.network.IK_JOINTS.connections()

    @property
    def ikJntsAttr(self):
        return self.network.IK_JOINTS

    @property
    def ik_ctrls(self):
        return self.network.IK_CTRLS.connections()

    @property
    def ikCtrlsAttr(self):
        return self.network.IK_CTRLS

    @property
    def fk_ctrls(self):
        return self.network.FK_CTRLS.connections()

    @property
    def pole_ctrls(self):
        return self.network.POLE.connections()

    @property
    def fkCtrlsAttr(self):
        return self.network.FK_CTRLS

    @property
    def ik_handles(self):
        return self.network.IK_HANDLE.connections()

    @property
    def ikHandlesAttr(self):
        return self.network.IK_HANDLE

    @property
    def name_info(self):
        return naming_utils.ItemInfo(self)

    @property
    def _class(self):
        return self._class.get()

    @property
    def side(self):
        return self.network.Side.get()

    @property
    def region(self):
        return self.network.Region.get()

    def add_network_tag(self):
        self.add_tags({'Network': self.network.name()})

    def add_tags(self, tags):
        try:
            naming_utils.add_tags(self, tags)
        except Exception as ex:
            log.warning('Failed to add tags: {}, {}, {}'.format(self, tags, ex))

    def getRoot(self):
        return joint_utils.get_root(self)

    def getCtrlRig(self):
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


class TransformNode(BaseNode, pymel.nodetypes.Transform):
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
        newNode.addAttr('IK_CTRLS', attributeType='message', multi=True)
        newNode.addAttr('FK_CTRLS', attributeType='message', multi=True)
        newNode.addAttr('CTRLS', attributeType='message', multi=True)
        newNode.addAttr('POLE', attributeType='message', multi=True)
        newNode.addAttr('SWITCH', attributeType='message', multi=True)
        newNode.addAttr('ORIENTCONSTRAINT', attributeType='message', multi=True)
        newNode.addAttr('POINTCONSTRAINT', attributeType='message', multi=True)
        newNode.addAttr('IK_HANDLE', attributeType='message', multi=True)
        newNode.addAttr('IK_SNAP_LOC', attributeType='message', multi=True)


    #Overwritting BaseClass Method
    @property
    def network(self):
        return self


class SplineIKNet(pymel.nodetypes.Network, BaseNode):
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
                if plug.asString() == '_SplineIKNet':
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
        newNode._class.set('_SplineIKNet')
        newNode.addAttr('JOINTS', attributeType='message', multi=True)
        newNode.addAttr('IK_HANDLE', attributeType='message', multi=True)
        newNode.addAttr('IK_CTRLS', attributeType='message', multi=True)
        newNode.addAttr('CLUSTER_HANDLE', attributeType='message', multi=True)
        newNode.addAttr('COG', attributeType='message', multi=True)

    @property
    def network(self):
        return self

    @property
    def clusters(self):
        return self.CLUSTER_HANDLE.connections()

    @property
    def cog(self):
        return self.COG.connections()

    @property
    def clustersAttr(self):
        return self.CLUSTER_HANDLE


class MainNode(pymel.nodetypes.Network, BaseNode):
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
                if plug.asString() == '_MainNode':
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
        newNode._class.set('_MainNode')
        newNode.addAttr('MAIN_CTRL', attributeType='message', multi=True)
        newNode.addAttr('ARMS', attributeType='message', multi=True)
        newNode.addAttr('CLAVICLES', attributeType='message', multi=True)
        newNode.addAttr('LEGS', attributeType='message', multi=True)
        newNode.addAttr('SPINE', attributeType='message', multi=True)
        newNode.addAttr('HEAD', attributeType='message', multi=True)

    @property
    def network(self):
        return self

    @property
    def main_ctrl(self):
        return self.MAIN_CTRL.connections()

    @property
    def arms(self):
        return self.ARMS.connections()

    @property
    def legs(self):
        return self.LEGS.connections()

    @property
    def clavicles(self):
        return self.CLAVICLES.connections()

    @property
    def spine(self):
        return self.SPINE.connections()

    @property
    def head(self):
        return self.HEAD.connections()



class CtrlNode(pymel.nodetypes.Transform, BaseNode):

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
                if plug.asString() == '_CtrlNode':
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
        newNode._class.set('_CtrlNode')
        newNode.addAttr('SHAPE', attributeType='message', multi=True)

    def freeze_transform(self):
        pymel.makeIdentity(self, a=True, t=1, r=1, s=1, n=0, pn=1)

    def set_shape(self, shape):
        pymel.delete(self.getShape())
        shapes.make_shape(shape_type=shape, transform=self)

    def set_axis(self, axis):
        if axis == 'x':
            self.setRotation((90, 0, 0))

        if axis == 'y':
            self.setRotation((0, 0, 0))

        if axis == 'z':
            self.setRotation((0, 0, 90))

    def create_offset(self):
        grp = pymel.group(empty=True)
        self.setParent(grp)
        return grp



# Classes need to be registered to exist in the scene.
pymel.factories.registerVirtualClass(JointNode, nameRequired=False)
pymel.factories.registerVirtualClass(LimbNode, nameRequired=False)
pymel.factories.registerVirtualClass(CtrlNode, nameRequired=False)
pymel.factories.registerVirtualClass(TransformNode, nameRequired=False)
pymel.factories.registerVirtualClass(SplineIKNet, nameRequired=False)
pymel.factories.registerVirtualClass(MainNode, nameRequired=False)

