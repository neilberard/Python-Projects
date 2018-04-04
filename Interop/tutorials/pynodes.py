import os
import maya.cmds
import pymel.core as pymel
import pymel.internal.factories
import xml.etree.cElementTree as cetree


class Controller(pymel.nodetypes.Transform):

    NODE_TYPE = "pcsController"

    @classmethod
    def list(cls, *args, **kwargs):
        kwargs['type'] = cls.melnode__
        return [node for node in pymel.ls(*args, **kwargs) if isinstance(node, cls)]


class MyVirtualNode(pymel.nodetypes.Network):

    @classmethod
    def list(cls, *args, **kwargs):
        kwargs['type'] = cls.__melnode__
        return [node for node in pymel.ls(*args, **kwargs) if isinstance(node, cls)]
