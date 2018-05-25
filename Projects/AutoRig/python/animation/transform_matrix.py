import pymel.core as pymel
import maya.OpenMaya as OpenMaya
import math

node = pymel.PyNode('pCube1')

transformMatrix = OpenMaya.MTransformationMatrix(node.worldMatrix.get())

eulerRot = transformMatrix.eulerRotation()
eulerRot.reorderIt(node.rotateOrder.get())

angles = [math.degrees(angle) for angle in (eulerRot.x, eulerRot.y, eulerRot.z)]

print angles