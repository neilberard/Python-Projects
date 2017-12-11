import pymel.core as pm
import maya.api.OpenMaya as om2

start_time = cmds.timerX()

mesh = om2.MFnMesh(path)


sel = om2.MGlobal.getActiveSelectionList()

path,comp = sel.getComponent(0)

iter = om2.MItMeshVertex(path,comp)

pointPos = om2.MPoint()

pointPosArray = mesh.getPoints()
normalArray = mesh.getNormals()
selectedNormalArray = om2.MVectorArray()

averageNormal = om2.MVector(0,0,0)
averagePosition = om2.MVector(0,0,0)



"""Get selection average"""

while not iter.isDone():

    averageNormal[0] += normalArray[iter.index()][0]
    averageNormal[1] += normalArray[iter.index()][1]
    averageNormal[2] += normalArray[iter.index()][2]
    
    averagePosition[0] += iter.position()[0]
    averagePosition[1] += iter.position()[1]
    averagePosition[2] += iter.position()[2]

    iter.next()

#mesh.setPoints(pointPosArray)
#print selectedNormalArray
pos = averagePosition/iter.count()
norm = averageNormal/iter.count()

pm.xform("locator1",t=norm*10,ws=True) 
pm.xform("locator2",t=pos,ws=True) 
    
print 'Duration = %f seconds' %cmds.timerX(st=start_time)