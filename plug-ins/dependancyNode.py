import sys
import maya.OpenMaya as OpenMaya
import maya.OpenMayaMPx as OpenMayaMpx

kPluginNodeName = 'ribbonMesh'
kPluginNodeId = OpenMaya.MTypeId(0x8700B)

class curveMesh(OpenMayaMpx.MPxNode):
    def __init__(self):
        OpenMayaMpx.MPxNode.__init__(self)

    def createMesh(self):
        pass

    def compute(self, plug, data):
        pass

def nodeCreator():
    return OpenMayaMpx.asMPxPtr(curveMesh())

def nodeInitializer():
    """
    Add attrs
    """
def initializePlugin(mobject):
    mplugin = OpenMayaMpx.MFnPlugin(mobject)

    try:
        mplugin.registerNode(kPluginNodeName, kPluginNodeId, nodeCreator, nodeInitializer)
    except Exception as ex:
        sys.stderr.write("Failed to register node {}: {}".format(kPluginNodeName, ex))
        raise

def uninitializePlugin(mobject):
    mplugin = OpenMayaMpx.MFnPlugin(mobject)
    try:
        mplugin.deregisterNode(kPluginNodeId)
    except Exception as ex:
        sys.stderr.write("Failed to derigister node {}: {}".format(kPluginNodeName, ex))
        raise
