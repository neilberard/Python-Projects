import maya.OpenMaya as OpenMaya
import pymel.core as pymel

node = pymel.PyNode('pPlane1')


fnMesh = node.getShape().__apimfn__()
points = OpenMaya.MPointArray()
fnMesh.getPoints(points)


OpenMaya.MPoint()
fnMesh.currentUVSetName()

util = OpenMaya.MScriptUtil()
util.createFromList([0.0, 0.0], 2)
uvPoint = util.asFloat2Ptr()

fnMesh.getUVAtPoint(points[3],uvPoint, OpenMaya.MSpace.kWorld)

u = OpenMaya.MScriptUtil.getFloat2ArrayItem(uvPoint, 0, 0)
v = OpenMaya.MScriptUtil.getFloat2ArrayItem(uvPoint, 0, 1)

print u, v