""" Virtual Class Example """

import os
import pymel.all as pymel
import xml.etree.cElementTree as cetree


class MyVirtualNode(pymel.nt.Network):
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
            if fn.hasAttribute('myString'):
                plug = fn.findPlug('myString')
                if plug.asString() == 'virtualNode':
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
        newNode.addAttr('JOINTS', at='message', multi=True)

        newNode.addAttr('myName', dt='string')

        newNode.addAttr('myString', dt='string')
        newNode.myString.set('virtualNode')

        newNode.addAttr('myFloat', at='float')
        newNode.myFloat.set(.125)

        newNode.addAttr('myConnection', at='message')

    def get_joints(self):
        return self.JOINTS.connections()

    def toXML(self):
        xml = cetree.Element('MyVirtualNode')
        xml.set('Name', self.get_my_name())

        return xml


pymel.factories.registerVirtualClass(MyVirtualNode, nameRequired=False)
