import pymel.core as pymel
import maya.OpenMaya as OpenMaya
from python.libs import consts
import math

info = {}
map = {'Pelvis': 'Hips',
       'Spine_A': 'Spine',
       'Spine_B': 'Spine1',
       'Chest': 'Spine2',
       'R_Hip': 'RightUpLeg',  # R LEG
       'R_Knee': 'RightLeg',
       'R_Ankle': 'RightFoot',
       'R_Ball': 'RightToeBase',
       'R_Toe': 'RightToe_End',
       'L_Hip': 'LeftUpLeg',  # L LEG
       'L_Knee': 'LeftLeg',
       'L_Ankle': 'LeftFoot',
       'L_Ball': 'LeftToeBase',
       'L_Toe': 'LeftToe_End',
       'R_Clavicle': 'RightShoulder',  # R ARM
       'R_Shoulder': 'RightArm',
       'R_Elbow': 'RightForeArm',
       'R_Wrist': 'RightHand',
       'L_Clavicle': 'LeftShoulder',  # L ARM
       'L_Shoulder': 'LeftArm',
       'L_Elbow': 'LeftForeArm',
       'L_Wrist': 'LeftHand',
       }

pynodes = {}

pymel.currentTime(0, edit=True)

for key, value in map.iteritems():
    pynodes[pymel.PyNode(key)] = [pymel.PyNode(value)]

for key, value in pynodes.iteritems():
    value[0].assumePreferredAngles()
    inverseMatrix = OpenMaya.MMatrix(value[0].worldInverseMatrix.get())
    worldMatrix = OpenMaya.MMatrix(key.worldMatrix.get())
    offsetMatrix = inverseMatrix * worldMatrix
    pynodes[key].append(offsetMatrix)

pymel.currentTime(1, edit=True)

for key, value in pynodes.iteritems():
    if key == 'L_Shoulder' or key == 'L_Clavicle' or key == 'L_Elbow':

        # children = key.getChildren()
        #
        # for child in children:
        #     child.setParent(None)

        transformMatrix = OpenMaya.MTransformationMatrix(value[0].worldMatrix.get() * value[1])

        eulerRot = transformMatrix.eulerRotation()
        eulerRot.reorderIt(key.rotateOrder.get())

        angles = [math.degrees(angle) for angle in (eulerRot.x, eulerRot.y, eulerRot.z)]

        key.setRotation(angles, worldSpace=True)
        print angles





    # key.setMatrix(value[0].worldMatrix.get() * value[1], worldSpace=True)
    #
    # for child in children:
    #     child.setParent(key)










