import maya.api.OpenMaya as om2
import sys


kPluginNodeTypeName = "spyTwistNode"
yTwistNodeId = om2.MTypeId(0x8702)


class yTwistNode(om2.MPxGeometryFilter):
    def __init__(self):
        om2.MPxGeometryData.__init__(self)

    # deform
    def compute(self, dataBlock, geomIter, matrix, multiIndex):
        #
        # get the angle from the datablock
        angleHandle = dataBlock.inputValue(self.angle)
        angleValue = angleHandle.asDouble()
        #
        # get the envelope
        envelopeHandle = dataBlock.inputValue(envelope)
        envelopeValue = envelopeHandle.asFloat()
        #
        # iterate over the object and change the angle
        while geomIter.isDone() == False:
            point = geomIter.position()
            ff = angleValue * point.y * envelopeValue
            if ff != 0.0:
                cct = math.cos(ff)
                cst = math.sin(ff)
                tt = point.x * cct - point.z * cst
                point.z = point.x * cst + point.z * cct
                point.x = tt
            geomIter.setPosition(point)
            geomIter.next()

    pass


def initializePlugin(mobject):
    mplugin = om2.MFnPlugin(mobject)
    try:
        mplugin.registerNode(kPluginNodeTypeName, yTwistNodeId, nodeCreator, nodeInitializer,
                             om2.MPxNode.kDeformerNode)
    except:
        sys.stderr.write("Failed to register node: %s\n" % kPluginNodeTypeName)


def nodeCreator():
    return yTwistNode()


# initializer
def nodeInitializer():
    # angle
    nAttr = om2.MFnNumericAttribute()
    yTwistNode.angle = nAttr.create("angle", "fa", om2.MFnNumericData.kDouble, 0.0)
    # nAttr.setDefault(0.0)
    nAttr.setKeyable(True)
    # add attribute
    try:
        yTwistNode.addAttribute(yTwistNode.angle)
        yTwistNode.attributeAffects(yTwistNode.angle, outputGeom)
    except:
        sys.stderr.write("Failed to create attributes of %s node\n", kPluginNodeTypeName)

# uninitialize the script plug-in
def uninitializePlugin(mobject):
    mplugin = om2.MFnPlugin(mobject)
    try:
        mplugin.deregisterNode(yTwistNodeId)
    except:
        sys.stderr.write("Failed to unregister node: %s\n" % kPluginNodeTypeName)
